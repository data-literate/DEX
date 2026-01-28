# GitHub Actions Workflows

This folder contains CI/CD automation for DEX.

## Workflows

### `ci-cd.yaml` - Main CI/CD Pipeline
**Triggers**: Push to `main` or `develop`, Pull Requests

**Jobs**:
1. **lint-and-test**
   - Runs ruff linter
   - Runs mypy type checking
   - Runs pytest with coverage
   - Uploads coverage report

2. **build-and-push** (only on push to main/develop)
   - Builds Docker image with SHA tag (`sha-XXXXXXXX`)
   - Pushes to GitHub Container Registry (`ghcr.io`)
   - Tags: `sha-XXXXXXXX`, `latest` (main branch only)

3. **update-dev-manifest** (only on push to main)
   - Updates `infra/argocd/overlays/dev/kustomization.yaml` with new image tag
   - Commits changes back to repo (triggers ArgoCD sync)
   - Uses `[skip ci]` to avoid recursive builds

4. **security-scan**
   - Runs Trivy vulnerability scanner on built image
   - Uploads SARIF results to GitHub Security tab

### `pr-preview.yaml` - PR Preview Environments
**Triggers**: PR with `preview` label

**Jobs**:
1. **check-preview-label**
   - Checks if PR has `preview` label
   - Only deploys if label exists

2. **build-preview**
   - Builds Docker image with PR-specific tag
   - Tags: `sha-XXXXXXXX`, `pr-###`
   - Comments on PR with deployment details
   - ArgoCD automatically creates `dex-pr-###` namespace

## Required Secrets

### Repository Secrets
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions (no setup needed)

### Optional Secrets
- `SONAR_TOKEN` - For SonarCloud integration
- `SLACK_WEBHOOK_URL` - For deployment notifications

## Image Registry

All images are pushed to:
```
ghcr.io/data-literate/dex:TAG
```

### Image Tags
- `sha-XXXXXXXX` - Immutable SHA tag (8 characters)
- `latest` - Latest main branch build
- `pr-###` - PR-specific preview builds

## ArgoCD Integration

### Dev Environment Auto-Deployment
1. CI builds image: `ghcr.io/data-literate/dex:sha-abc12345`
2. CI updates `infra/argocd/overlays/dev/kustomization.yaml`:
   ```yaml
   images:
     - name: data-literate/dex
       newTag: sha-abc12345
   ```
3. CI commits change with `[skip ci]` message
4. ArgoCD detects git change → syncs dev environment

### PR Preview Auto-Deployment
1. Add `preview` label to PR
2. CI builds image: `ghcr.io/data-literate/dex:sha-xyz67890`
3. ArgoCD ApplicationSet (PR generator) detects PR
4. ArgoCD creates `dex-pr-42` Application
5. Deploys to `dex-pr-42` namespace
6. Auto-cleanup when PR closes

## Usage

### Enable PR Preview
```bash
# Add preview label via GitHub UI or:
gh pr edit <pr-number> --add-label preview
```

### Manual Promotion (Stage/Prod)
```bash
# After dev deployment succeeds, promote to stage:
IMAGE_TAG="sha-abc12345"

# Update stage overlay
sed -i "s|newTag:.*|newTag: $IMAGE_TAG|g" infra/argocd/overlays/stage/kustomization.yaml

# Create promotion PR
git checkout -b promote-stage-$IMAGE_TAG
git add infra/argocd/overlays/stage/kustomization.yaml
git commit -m "chore: promote $IMAGE_TAG to stage"
git push origin promote-stage-$IMAGE_TAG

# Create PR for review → merge → ArgoCD syncs stage

# Same process for prod (requires manual ArgoCD sync)
```

## Troubleshooting

### Image not updating in dev
- Check workflow run: `gh run list --workflow ci-cd.yaml`
- Verify commit exists: `git log infra/argocd/overlays/dev/kustomization.yaml`
- Verify image in registry: `docker pull ghcr.io/data-literate/dex:sha-XXXXXXXX`

### PR preview not deploying
- Verify `preview` label exists on PR
- Check ArgoCD ApplicationSet: `kubectl get applicationset -n argocd`
- Check PR generator events: `argocd appset get dex-pr-preview -n argocd`

### Permission errors
- Verify `GITHUB_TOKEN` has `packages: write` permission
- Check GitHub Actions settings → Workflow permissions → Read and write

## Local Testing

### Test Docker build
```bash
docker build -t dex:local .
docker run -p 8000:8000 dex:local
```

### Test kustomize updates
```bash
# Preview changes
kustomize build infra/argocd/overlays/dev

# Apply locally
kubectl apply -k infra/argocd/overlays/dev
```

### Test CI workflow locally (act)
```bash
# Install act: https://github.com/nektos/act
act push --workflows .github/workflows/ci-cd.yaml
```

## Best Practices

1. **Always use SHA tags** - Immutable, traceable, promotable
2. **Use `[skip ci]` in manifest updates** - Avoid recursive builds
3. **Add `preview` label selectively** - Preview envs cost resources
4. **Clean up old images** - Use GHCR retention policies (30 days)
5. **Review security scan results** - Check GitHub Security tab regularly

## Future Enhancements

- [ ] SonarCloud quality gates
- [ ] Slack/Discord deployment notifications
- [ ] Automated rollback on failed health checks
- [ ] Canary deployments for prod
- [ ] E2E smoke tests before promotion
