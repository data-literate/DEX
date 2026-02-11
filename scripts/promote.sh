#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/promote.sh --from-env <dev|stage> --to-env <stage|prod> [--image-tag <tag>] [--auto-merge]

Examples:
  ./scripts/promote.sh --from-env dev --to-env stage
  ./scripts/promote.sh --from-env stage --to-env prod --image-tag sha-abc12345
  ./scripts/promote.sh --from-env dev --to-env stage --auto-merge
USAGE
}

from_env=""
to_env=""
image_tag=""
auto_merge="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from-env|-f)
      from_env="$2"
      shift 2
      ;;
    --to-env|-t)
      to_env="$2"
      shift 2
      ;;
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

if [[ -z "$from_env" || -z "$to_env" ]]; then
  usage
  exit 1
fi

if [[ "$from_env" == "stage" && "$to_env" != "prod" ]]; then
  echo "Can only promote from stage to prod"
  exit 1
fi

if [[ "$from_env" == "dev" && "$to_env" != "stage" ]]; then
  echo "Can only promote from dev to stage"
  exit 1
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
from_kustomization="${repo_root}/infra/argocd/overlays/${from_env}/kustomization.yaml"
to_kustomization="${repo_root}/infra/argocd/overlays/${to_env}/kustomization.yaml"

echo "Promoting from ${from_env} to ${to_env}"

if [[ -z "$image_tag" ]]; then
  echo "Reading image tag from ${from_env} environment"
  if [[ ! -f "$from_kustomization" ]]; then
    echo "Missing kustomization: ${from_kustomization}"
    exit 1
  fi
  image_tag=$(grep -E 'newTag:' "$from_kustomization" | head -n 1 | sed 's/.*newTag:[[:space:]]*//')
  if [[ -z "$image_tag" ]]; then
    echo "Could not find image tag in ${from_kustomization}"
    exit 1
  fi
  echo "Found image tag: ${image_tag}"
fi

if [[ ! "$image_tag" =~ ^(sha-[a-f0-9]{8}|v[0-9]+\.[0-9]+\.[0-9]+|latest)$ ]]; then
  echo "Warning: image tag '${image_tag}' does not match expected format"
  read -r -p "Continue anyway? (y/N) " continue_choice
  if [[ "$continue_choice" != "y" ]]; then
    exit 1
  fi
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Warning: you have uncommitted changes"
  git status --porcelain
  read -r -p "Continue anyway? (y/N) " continue_choice
  if [[ "$continue_choice" != "y" ]]; then
    exit 1
  fi
fi

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$current_branch" != "main" ]]; then
  echo "Switching to main branch"
  git checkout main
  git pull origin main
fi

branch_name="promote-${to_env}-${image_tag}"
echo "Creating branch: ${branch_name}"
git checkout -b "$branch_name"

echo "Updating ${to_env} kustomization.yaml"
sed -i "s|newTag:.*|newTag: ${image_tag}|g" "$to_kustomization"

echo "Changes:"
git diff "$to_kustomization"

echo "Committing changes"
git add "$to_kustomization"
git commit \
  -m "chore: promote ${image_tag} to ${to_env}" \
  -m "Promoted from: ${from_env}" \
  -m "Image tag: ${image_tag}" \
  -m "Environment: ${to_env}" \
  -m "Created via promote.sh script." \
  -m "ArgoCD will sync ${to_env} environment after PR is merged."

echo "Pushing branch"
git push origin "$branch_name"

if command -v gh >/dev/null 2>&1; then
  pr_title="Promote ${image_tag} to ${to_env}"
  pr_body=$(cat <<EOF
## Image Promotion

**From**: ${from_env}
**To**: ${to_env}
**Image Tag**: \\`${image_tag}\\`

### Checklist
- [ ] Verify image tag is correct
- [ ] Check ${from_env} environment is stable
- [ ] Review deployment changes
$(if [[ "$to_env" == "prod" ]]; then echo "- [ ] Notify team of production deployment
- [ ] Verify rollback plan
- [ ] Schedule deployment window (if required)"; fi)

### Post-Merge
After merging this PR:
1. ArgoCD will detect the change
$(if [[ "$to_env" == "prod" ]]; then echo "2. Manual sync required: run \\`argocd app sync dex\\` in ArgoCD UI"; else echo "2. ArgoCD will auto-sync ${to_env} environment (~3 minutes)"; fi)
3. Monitor deployment: \\`kubectl get pods -n dex-${to_env}\\`
4. Verify health: \\`kubectl rollout status deployment/dex -n dex-${to_env}\\`

### Rollback
If issues occur:

```bash
# Revert this commit
git revert HEAD
git push origin main

# Or use ArgoCD rollback
argocd app rollback dex-${to_env}
```

---
Automated promotion via promote.sh
EOF
)

  gh pr create --title "$pr_title" --body "$pr_body" --base main --head "$branch_name" --label "promotion" --label "$to_env"

  if [[ "$auto_merge" == "true" ]]; then
    gh pr merge "$branch_name" --auto --squash
    echo "PR will auto-merge after checks pass"
  else
    gh pr view --web
  fi
else
  echo "GitHub CLI (gh) not found. Create a PR manually:"
  echo "  Branch: ${branch_name}"
  echo "  Title: Promote ${image_tag} to ${to_env}"
fi

echo "Switching back to main"
git checkout main

echo "Promotion complete"
