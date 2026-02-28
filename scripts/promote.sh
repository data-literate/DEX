#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# promote.sh — Branch-based promotion: dev → prod (main)
#
# Creates a PR to merge the dev branch into main, which triggers
# CD to build + deploy to the prod environment (dex namespace)
# via ArgoCD.
#
# Optionally promotes a specific image tag by updating the prod
# overlay kustomization.yaml directly.
# ---------------------------------------------------------------

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/promote.sh [--image-tag <tag>] [--auto-merge]

Promotes dev → prod by creating a merge PR from dev into main.
If --image-tag is provided, updates prod overlay with that specific tag instead.

Examples:
  ./scripts/promote.sh                          # PR: dev → main
  ./scripts/promote.sh --auto-merge             # PR: dev → main (auto-merge)
  ./scripts/promote.sh --image-tag sha-abc12345 # Update prod overlay directly
USAGE
}

image_tag=""
auto_merge="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image-tag|-i)
      image_tag="$2"
      shift 2
      ;;
    --auto-merge)
      auto_merge="true"
      shift 1
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Warning: you have uncommitted changes"
  git status --porcelain
  read -r -p "Continue anyway? (y/N) " continue_choice
  if [[ "$continue_choice" != "y" ]]; then
    exit 1
  fi
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ---------------------------------------------------------------
# Mode 1: Direct image tag promotion (override prod overlay)
# ---------------------------------------------------------------
if [[ -n "$image_tag" ]]; then
  if [[ ! "$image_tag" =~ ^(sha-[a-f0-9]{8}|v[0-9]+\.[0-9]+\.[0-9]+|latest)$ ]]; then
    echo "Warning: image tag '${image_tag}' does not match expected format"
    read -r -p "Continue anyway? (y/N) " continue_choice
    if [[ "$continue_choice" != "y" ]]; then
      exit 1
    fi
  fi

  prod_kustomization="${repo_root}/infra/argocd/overlays/prod/kustomization.yaml"
  echo "Promoting image ${image_tag} to prod overlay"

  git checkout main
  git pull origin main

  branch_name="promote-prod-${image_tag}"
  echo "Creating branch: ${branch_name}"
  git checkout -b "$branch_name"

  sed -i "s|newTag:.*|newTag: ${image_tag}|g" "$prod_kustomization"

  echo "Changes:"
  git diff "$prod_kustomization"

  git add "$prod_kustomization"
  git commit \
    -m "chore: promote ${image_tag} to prod" \
    -m "Image tag: ${image_tag}" \
    -m "Created via promote.sh script." \
    -m "ArgoCD will sync prod environment (dex namespace) after PR is merged."

  git push origin "$branch_name"

  if command -v gh >/dev/null 2>&1; then
    pr_title="Promote ${image_tag} to prod"
    pr_body=$(cat <<EOF
## Image Promotion to Production

**Image Tag**: \`${image_tag}\`

### Checklist
- [ ] Verify image tag is correct
- [ ] Check dev environment is stable with this image
- [ ] Notify team of production deployment
- [ ] Verify rollback plan

### Post-Merge
1. CD pipeline will build and deploy to prod
2. ArgoCD will sync dex (~3 minutes)
3. Monitor: \`kubectl get pods -n dex\`
4. Verify: \`kubectl rollout status deployment/dex -n dex\`

### Rollback
\`\`\`bash
git revert HEAD
git push origin main
# Or: argocd app rollback dex
\`\`\`

---
Automated promotion via promote.sh
EOF
)

    gh pr create --title "$pr_title" --body "$pr_body" --base main --head "$branch_name" --label "promotion" --label "prod"

    if [[ "$auto_merge" == "true" ]]; then
      gh pr merge "$branch_name" --auto --squash
      echo "PR will auto-merge after checks pass"
    else
      gh pr view --web
    fi
  else
    echo "GitHub CLI (gh) not found. Create a PR manually:"
    echo "  Branch: ${branch_name}"
    echo "  Title: Promote ${image_tag} to prod"
  fi

  git checkout main
  echo "Promotion complete"
  exit 0
fi

# ---------------------------------------------------------------
# Mode 2: Branch promotion (dev → main)
# ---------------------------------------------------------------
echo "Promoting dev → main (prod)"
echo "This creates a PR to merge the dev branch into main."

git fetch origin dev main

# Check dev is ahead of main
dev_ahead=$(git rev-list --count origin/main..origin/dev 2>/dev/null || echo "0")
if [[ "$dev_ahead" == "0" ]]; then
  echo "dev is not ahead of main — nothing to promote."
  exit 0
fi
echo "dev is ${dev_ahead} commit(s) ahead of main"

if command -v gh >/dev/null 2>&1; then
  # Check if a promotion PR already exists
  existing_pr=$(gh pr list --base main --head dev --json number --jq '.[0].number' 2>/dev/null || echo "")
  if [[ -n "$existing_pr" ]]; then
    echo "Promotion PR #${existing_pr} already exists: dev → main"
    gh pr view "$existing_pr" --web
    exit 0
  fi

  dev_sha=$(git rev-parse --short=8 origin/dev)
  pr_title="chore: promote dev to prod (${dev_sha})"
  pr_body=$(cat <<EOF
## Branch Promotion: dev → prod

**Source**: \`dev\` (${dev_sha})
**Target**: \`main\` (prod)
**Commits**: ${dev_ahead} commit(s) ahead

### Checklist
- [ ] Dev environment is stable
- [ ] All CI checks pass
- [ ] Notify team of production deployment
- [ ] Verify rollback plan

### Post-Merge
1. CD pipeline builds image and updates prod overlay
2. ArgoCD syncs dex (~3 minutes)
3. Monitor: \`kubectl get pods -n dex\`
4. Verify: \`kubectl rollout status deployment/dex -n dex\`

### Rollback
\`\`\`bash
git revert HEAD
git push origin main
# Or: argocd app rollback dex
\`\`\`

---
Automated promotion via promote.sh
EOF
)

  gh pr create --title "$pr_title" --body "$pr_body" --base main --head dev --label "promotion" --label "prod"

  if [[ "$auto_merge" == "true" ]]; then
    gh pr merge dev --auto --squash
    echo "PR will auto-merge after checks pass"
  else
    gh pr view --web
  fi
else
  echo "GitHub CLI (gh) not found. Create a PR manually:"
  echo "  Base: main"
  echo "  Head: dev"
  echo "  Title: Promote dev to prod"
fi

echo "Promotion complete"
