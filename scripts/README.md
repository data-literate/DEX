# Promotion Scripts

Ubuntu-friendly workflow for managing GitOps image promotion using bash scripts.

## Scripts

### `promote.sh`
Promotes container images between environments by updating kustomization.yaml and creating PRs.

**Usage (Ubuntu):**
```bash
# Promote from dev to stage (auto-detects current dev image)
./scripts/promote.sh --from-env dev --to-env stage

# Promote specific image from stage to prod
./scripts/promote.sh --from-env stage --to-env prod --image-tag sha-abc12345

# Promote with auto-merge (requires permissions)
./scripts/promote.sh --from-env dev --to-env stage --auto-merge
```

**Features:**
- Reads current image tag from source environment
- Creates feature branch: `promote-{env}-{tag}`
- Updates target environment kustomization.yaml
- Commits with detailed message
- Creates GitHub PR with checklist (requires `gh` CLI)
- Supports auto-merge with `--auto-merge` flag

**Prerequisites (Ubuntu):**
- bash
- GitHub CLI (`gh`) installed and authenticated
- Git configured with push access to repository
- On `main` branch with no uncommitted changes

Make the scripts executable once:
```bash
chmod +x ./scripts/*.sh
```

### `get-tags.sh`
Displays current deployed image tags across all environments.

**Usage (Ubuntu):**
```bash
./scripts/get-tags.sh
```

**Output Example:**
```
🏷️  Current Image Tags
============================================================
  dev         sha-abc12345
  stage       sha-xyz67890
  prod        sha-xyz67890
============================================================

📊 Environment Status:
  ⚠️  Dev and Stage are out of sync
    Run: ./scripts/promote.sh --from-env dev --to-env stage
  ✅ Stage and Prod are in sync
```

## Promotion Workflow

### Standard Flow: Dev → Stage → Prod

```bash
# 1. Check current tags
./scripts/get-tags.sh

# 2. Promote dev → stage
./scripts/promote.sh --from-env dev --to-env stage

# 3. Wait for PR review + merge
# 4. ArgoCD auto-syncs stage (~3 minutes)

# 5. Verify stage deployment
kubectl rollout status deployment/dex -n dex-stage
kubectl get pods -n dex-stage

# 6. Promote stage → prod
./scripts/promote.sh --from-env stage --to-env prod

# 7. Wait for PR review + merge
# 8. Manually sync prod in ArgoCD
argocd app sync dex-prod

# 9. Verify prod deployment
kubectl rollout status deployment/dex -n dex-prod
kubectl get pods -n dex-prod
```

### Emergency Hotfix: Direct to Prod

```bash
# NOT RECOMMENDED - breaks gold-standard workflow
# Only for critical security patches

# 1. Get tested SHA from stage
hotfixTag="sha-emergency"

# 2. Promote directly to prod
./scripts/promote.sh --from-env stage --to-env prod --image-tag "$hotfixTag"

# 3. Fast-track PR approval
# 4. Manual ArgoCD sync
argocd app sync dex-prod --force
```

### Rollback

```bash
# Option 1: Git revert (recommended)
git log infra/argocd/overlays/prod/kustomization.yaml
git revert <commit-sha>
git push origin main

# Option 2: ArgoCD rollback
argocd app history dex-prod
argocd app rollback dex-prod <revision>

# Option 3: Manual promotion to previous tag
./scripts/promote.sh --from-env stage --to-env prod --image-tag sha-previous123
```

## Integration with CI/CD

### Automated Dev Deployment
GitHub Actions automatically updates GitOps overlays based on branch:
- `dev` branch CI success → updates `infra/argocd/overlays/dev/kustomization.yaml`
- `main` branch CI success → updates `infra/argocd/overlays/stage/kustomization.yaml` and `infra/argocd/overlays/prod/kustomization.yaml`

Example from CD workflow:
```yaml
# .github/workflows/cd.yml
- name: Update overlay image tags
  run: |
    # dev branch updates dev overlay
    # main branch updates stage/prod overlays
    git commit -m "chore: update ${BRANCH} image to sha-$SHORT_SHA [skip ci]"
    git push origin "HEAD:${BRANCH}"
```

### Manual Stage/Prod Promotion
Use promotion scripts for controlled stage/prod deployments:
```bash
# After dev is stable
./scripts/promote.sh --from-env dev --to-env stage

# After stage validation
./scripts/promote.sh --from-env stage --to-env prod
```

### Future: Automated Stage Promotion (Optional)
```yaml
# .github/workflows/promote-stage.yml
name: Auto-Promote to Stage

on:
  workflow_dispatch:  # Manual trigger only

jobs:
  promote:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Promote to stage
        run: ./scripts/promote.sh --from-env dev --to-env stage --auto-merge
```

## Troubleshooting

### "Could not find image tag"
```bash
# Check kustomization.yaml format
cat infra/argocd/overlays/dev/kustomization.yaml

# Should contain:
# images:
#   - name: thedataenginex/dex
#     newTag: sha-XXXXXXXX
```

### "You have uncommitted changes"
```bash
# Stash changes
git stash

# Run promotion
./scripts/promote.sh --from-env dev --to-env stage

# Restore changes
git stash pop
```

### "gh: command not found"
```bash
# Install GitHub CLI (Ubuntu)
sudo apt-get update
sudo apt-get install -y gh

# Authenticate
gh auth login
```

### PR creation fails
```bash
# Check gh auth status
gh auth status

# Check repository permissions
gh repo view TheDataEngineX/DEX

# Manual PR creation
git push origin promote-stage-sha-abc12345
# Then create PR via GitHub UI
```

## Best Practices

1. **Always promote sequentially**: dev → stage → prod
2. **Use PR reviews**: Require approvals before merging
3. **Monitor deployments**: Check logs and metrics after promotion
4. **Test in stage**: Run integration tests before prod promotion
5. **Document promotions**: Use PR descriptions for audit trail
6. **Keep environments in sync**: Regularly check with `get-tags.sh`
7. **Use SHA tags**: Immutable, traceable, promotable
8. **Never skip stage**: Even for hotfixes, validate in stage first

## References

- [Infrastructure Promotion Workflow](../docs/DEPLOY_RUNBOOK.md)
- [ArgoCD Sync Documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/)
- [Kustomize Documentation](https://kustomize.io/)
