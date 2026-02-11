#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
environments=(dev stage prod)

echo ""
echo "Current Image Tags"
echo "============================================================"

for env in "${environments[@]}"; do
  kustomization="${repo_root}/infra/argocd/overlays/${env}/kustomization.yaml"
  if [[ -f "$kustomization" ]]; then
    tag=$(grep -E 'newTag:' "$kustomization" | head -n 1 | sed 's/.*newTag:[[:space:]]*//')
    if [[ -n "$tag" ]]; then
      printf "  %-10s %s\n" "$env" "$tag"
    else
      printf "  %-10s %s\n" "$env" "No tag found"
    fi
  else
    printf "  %-10s %s\n" "$env" "Kustomization not found"
  fi
done

echo "============================================================"

# Drift detection
if [[ -f "${repo_root}/infra/argocd/overlays/dev/kustomization.yaml" && \
      -f "${repo_root}/infra/argocd/overlays/stage/kustomization.yaml" && \
      -f "${repo_root}/infra/argocd/overlays/prod/kustomization.yaml" ]]; then
  dev_tag=$(grep -E 'newTag:' "${repo_root}/infra/argocd/overlays/dev/kustomization.yaml" | head -n 1 | sed 's/.*newTag:[[:space:]]*//')
  stage_tag=$(grep -E 'newTag:' "${repo_root}/infra/argocd/overlays/stage/kustomization.yaml" | head -n 1 | sed 's/.*newTag:[[:space:]]*//')
  prod_tag=$(grep -E 'newTag:' "${repo_root}/infra/argocd/overlays/prod/kustomization.yaml" | head -n 1 | sed 's/.*newTag:[[:space:]]*//')

  echo ""
  echo "Environment Status:"

  if [[ "$dev_tag" != "$stage_tag" ]]; then
    echo "  Dev and Stage are out of sync"
    echo "    Run: ./scripts/promote.sh --from-env dev --to-env stage"
  else
    echo "  Dev and Stage are in sync"
  fi

  if [[ "$stage_tag" != "$prod_tag" ]]; then
    echo "  Stage and Prod are out of sync"
    echo "    Run: ./scripts/promote.sh --from-env stage --to-env prod"
  else
    echo "  Stage and Prod are in sync"
  fi
fi
