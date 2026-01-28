# Promotion Scripts

PowerShell scripts for managing GitOps image promotion workflow.

## Scripts

### `promote.ps1`
Promotes container images between environments by updating kustomization.yaml and creating PRs.

**Usage:**
```powershell
# Promote from dev to stage (auto-detects current dev image)
.\scripts\promote.ps1 -FromEnv dev -ToEnv stage

# Promote specific image from stage to prod
.\scripts\promote.ps1 -FromEnv stage -ToEnv prod -ImageTag sha-abc12345

# Promote with auto-merge (requires permissions)
.\scripts\promote.ps1 -FromEnv dev -ToEnv stage -AutoMerge
```

**Features:**
- Reads current image tag from source environment
- Creates feature branch: `promote-{env}-{tag}`
- Updates target environment kustomization.yaml
- Commits with detailed message
- Creates GitHub PR with checklist (requires `gh` CLI)
- Supports auto-merge with `-AutoMerge` flag

**Prerequisites:**
- GitHub CLI (`gh`) installed and authenticated
- Git configured with push access to repository
- On `main` branch with no uncommitted changes

### `get-tags.ps1`
Displays current deployed image tags across all environments.

**Usage:**
```powershell
.\scripts\get-tags.ps1
```

**Output Example:**
```
🏷️  Current Image Tags
============================================================
  dev         sha-abc12345
  stage       sha-xyz67890
  prod        v1.2.3
============================================================

📊 Environment Status:
  ⚠️  Dev and Stage are out of sync
     Run: .\scripts\promote.ps1 -FromEnv dev -ToEnv stage
  ✅ Stage and Prod are in sync
```

## Promotion Workflow

### Standard Flow: Dev → Stage → Prod

```powershell
# 1. Check current tags
.\scripts\get-tags.ps1

# 2. Promote dev → stage
.\scripts\promote.ps1 -FromEnv dev -ToEnv stage

# 3. Wait for PR review + merge
# 4. ArgoCD auto-syncs stage (~3 minutes)

# 5. Verify stage deployment
kubectl rollout status deployment/dex -n dex-stage
kubectl get pods -n dex-stage

# 6. Promote stage → prod
.\scripts\promote.ps1 -FromEnv stage -ToEnv prod

# 7. Wait for PR review + merge
# 8. Manually sync prod in ArgoCD
argocd app sync dex

# 9. Verify prod deployment
kubectl rollout status deployment/dex -n dex
kubectl get pods -n dex
```

### Emergency Hotfix: Direct to Prod

```powershell
# NOT RECOMMENDED - breaks gold-standard workflow
# Only for critical security patches

# 1. Get tested SHA from stage
$hotfixTag = "sha-emergency"

# 2. Promote directly to prod
.\scripts\promote.ps1 -FromEnv stage -ToEnv prod -ImageTag $hotfixTag

# 3. Fast-track PR approval
# 4. Manual ArgoCD sync
argocd app sync dex --force
```

### Rollback

```powershell
# Option 1: Git revert (recommended)
git log infra/argocd/overlays/prod/kustomization.yaml
git revert <commit-sha>
git push origin main

# Option 2: ArgoCD rollback
argocd app history dex
argocd app rollback dex <revision>

# Option 3: Manual promotion to previous tag
.\scripts\promote.ps1 -FromEnv stage -ToEnv prod -ImageTag sha-previous123
```

## Integration with CI/CD

### Automated Dev Deployment
GitHub Actions automatically updates dev overlay on `main` branch push:
```yaml
# .github/workflows/cd.yml
- name: Update dev kustomization.yaml
  run: |
    sed -i "s|newTag:.*|newTag: sha-$SHORT_SHA|g" infra/argocd/overlays/dev/kustomization.yaml
    git commit -m "chore: update dev image to sha-$SHORT_SHA [skip ci]"
    git push origin main
```

### Manual Stage/Prod Promotion
Use promotion scripts for controlled stage/prod deployments:
```powershell
# After dev is stable
.\scripts\promote.ps1 -FromEnv dev -ToEnv stage

# After stage validation
.\scripts\promote.ps1 -FromEnv stage -ToEnv prod
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
      - uses: actions/checkout@v4
      - name: Promote to stage
        run: pwsh scripts/promote.ps1 -FromEnv dev -ToEnv stage -AutoMerge
```

## Troubleshooting

### "Could not find image tag"
```powershell
# Check kustomization.yaml format
cat infra/argocd/overlays/dev/kustomization.yaml

# Should contain:
# images:
#   - name: data-literate/dex
#     newTag: sha-XXXXXXXX
```

### "You have uncommitted changes"
```powershell
# Stash changes
git stash

# Run promotion
.\scripts\promote.ps1 -FromEnv dev -ToEnv stage

# Restore changes
git stash pop
```

### "gh: command not found"
```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Or download from: https://cli.github.com/

# Authenticate
gh auth login
```

### PR creation fails
```powershell
# Check gh auth status
gh auth status

# Check repository permissions
gh repo view data-literate/DEX

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
6. **Keep environments in sync**: Regularly check with `get-tags.ps1`
7. **Use SHA tags**: Immutable, traceable, promotable
8. **Never skip stage**: Even for hotfixes, validate in stage first

## References

- [Promotion Workflow Documentation](../docs/PROMOTION_WORKFLOW.md)
- [ArgoCD Sync Documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/)
- [Kustomize Documentation](https://kustomize.io/)
