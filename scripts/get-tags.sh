#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
environments=(dev prod)

echo ""
echo "Current Image Tags"
echo "============================================================"

for env in "${environments[@]}"; do
  kustomization="${repo_root}/infra/argocd/overlays/${env}/kustomization.yaml"
  if [[ -f "$kustomization" ]]; then
    tag=$(grep -E 'newTag:' "$kustomization" | head -n 1 | sed 's/.*newTag:[[:space:]]*//' | sed 's/[[:space:]]*#.*//')
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
      -f "${repo_root}/infra/argocd/overlays/prod/kustomization.yaml" ]]; then
  dev_tag=$(grep -E 'newTag:' "${repo_root}/infra/argocd/overlays/dev/kustomization.yaml" | head -n 1 | sed 's/.*newTag:[[:space:]]*//')
  prod_tag=$(grep -E 'newTag:' "${repo_root}/infra/argocd/overlays/prod/kustomization.yaml" | head -n 1 | sed 's/.*newTag:[[:space:]]*//')

  echo ""
  echo "Environment Status:"

  if [[ "$dev_tag" != "$prod_tag" ]]; then
    echo "  Dev and Prod are out of sync"
    echo "    Run: ./scripts/promote.sh"
  else
    echo "  Dev and Prod are in sync"
  fi
fi
