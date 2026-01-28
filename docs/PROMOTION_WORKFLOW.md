# GitOps Promotion Workflow

This document describes the image promotion process for DEX using GitOps and ArgoCD.

## Overview

**Gold-Standard Pattern**: Build once, promote same artifact across environments
- **Build**: CI builds immutable SHA-tagged image
- **Deploy**: Image deployed to dev automatically
- **Promote**: Same image SHA promoted through stage → prod
- **Audit**: Git commits provide full promotion history

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                          │
│                                                               │
│  infra/argocd/overlays/                                      │
│  ├── dev/kustomization.yaml    (newTag: sha-abc12345)       │
│  ├── stage/kustomization.yaml  (newTag: sha-abc12345) ←PR   │
│  └── prod/kustomization.yaml   (newTag: sha-xyz67890) ←PR   │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ Git Poll (3 min) or Webhook
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      ArgoCD Controller                        │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ dex-dev  │  │dex-stage │  │   dex    │                  │
│  │  Auto    │  │  Auto    │  │  Manual  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ dex-dev NS  │  │dex-stage NS │  │  dex NS     │
│ 2 replicas  │  │ 2 replicas  │  │  3 replicas │
│ DEBUG log   │  │ INFO log    │  │  WARN log   │
└─────────────┘  └─────────────┘  └─────────────┘
```

## Promotion Flow

### 1. Build & Deploy to Dev (Automated)

**Trigger**: Push to `main` branch

```
Developer                GitHub Actions              ArgoCD
    │                           │                       │
    ├─ git push main ─────────►│                       │
    │                           ├─ Run CI (lint/test)  │
    │                           ├─ Build image:        │
    │                           │  sha-abc12345        │
    │                           ├─ Push to ghcr.io     │
    │                           ├─ Update dev overlay  │
    │                           ├─ Commit + Push       │
    │                           │  [skip ci]           │
    │                           │                       │
    │                           │  ◄────────────────────┤ Poll git
    │                           │                       ├─ Detect change
    │                           │                       ├─ Sync dex-dev
    │                           │                       └─ Deploy
    │  ◄─────── Dev deployed with sha-abc12345 ─────────┘
```

### 2. Promote Dev → Stage (Manual PR)

**Prerequisites**:
- ✅ Dev deployment stable
- ✅ All tests passing
- ✅ No critical errors in logs

**Steps**:
```powershell
# 1. Check current tags
.\scripts\get-tags.ps1

# 2. Run promotion script
.\scripts\promote.ps1 -FromEnv dev -ToEnv stage

# Script does:
# - Creates branch: promote-stage-sha-abc12345
# - Updates infra/argocd/overlays/stage/kustomization.yaml
# - Commits: "chore: promote sha-abc12345 to stage"
# - Pushes branch
# - Creates PR with checklist
```

**PR Review Checklist**:
- [ ] Verify image tag matches dev
- [ ] Check dev environment is stable
- [ ] Review kustomization changes
- [ ] Confirm no unrelated changes

**Post-Merge**:
- ArgoCD detects git change (~3 minutes)
- ArgoCD auto-syncs `dex-stage`
- Stage deployment updated with new image

### 3. Promote Stage → Prod (Manual PR + Approval)

**Prerequisites**:
- ✅ Stage deployment stable (>24 hours)
- ✅ Integration tests passing
- ✅ Performance metrics acceptable
- ✅ Security scans passed (Trivy)

**Steps**:
```powershell
# 1. Verify stage is stable
kubectl rollout status deployment/dex -n dex-stage
kubectl get pods -n dex-stage

# 2. Run promotion script
.\scripts\promote.ps1 -FromEnv stage -ToEnv prod

# Script creates PR with production checklist
```

**PR Review Checklist (Production)**:
- [ ] Verify image tag matches stage
- [ ] Stage environment stable for 24+ hours
- [ ] All integration tests passed
- [ ] Security scan (Trivy) results reviewed
- [ ] Performance benchmarks acceptable
- [ ] Rollback plan documented
- [ ] Notify team of deployment
- [ ] Schedule deployment window (if required)

**Post-Merge**:
- ArgoCD detects git change
- **Manual sync required**: `argocd app sync dex` (prod has auto-sync disabled)
- Monitor deployment:
  ```powershell
  kubectl rollout status deployment/dex -n dex
  kubectl get pods -n dex
  kubectl logs -f deployment/dex -n dex
  ```

## Rollback Procedures

### Option 1: Git Revert (Recommended)

```powershell
# 1. Find promotion commit
git log --oneline infra/argocd/overlays/prod/kustomization.yaml

# 2. Revert the promotion
git revert <commit-sha>

# 3. Push revert
git push origin main

# 4. Sync ArgoCD (prod)
argocd app sync dex

# 5. Verify rollback
kubectl rollout status deployment/dex -n dex
```

**Advantages**:
- ✅ Full audit trail in git
- ✅ Revert of revert = re-deploy
- ✅ Works across all environments

### Option 2: ArgoCD Rollback

```powershell
# 1. View deployment history
argocd app history dex

# Example output:
# ID  DATE                TAG                SOURCE
# 10  2026-01-28 10:30    sha-abc12345      main (HEAD)
# 9   2026-01-27 15:20    sha-xyz67890      main
# 8   2026-01-26 09:45    sha-def45678      main

# 2. Rollback to previous revision
argocd app rollback dex 9

# 3. Verify rollback
kubectl get pods -n dex
```

**Advantages**:
- ✅ Fast rollback (no git commit)
- ✅ Works when git is unavailable

**Disadvantages**:
- ❌ Out-of-band change (not in git)
- ❌ Manual re-sync required
- ❌ Must update git to match

### Option 3: Manual Promotion to Previous Tag

```powershell
# 1. Identify previous stable tag
.\scripts\get-tags.ps1

# 2. Promote previous tag
.\scripts\promote.ps1 -FromEnv stage -ToEnv prod -ImageTag sha-xyz67890

# 3. Merge PR
# 4. Manual sync
argocd app sync dex
```

**Use When**:
- Need formal PR approval for rollback
- Want audit trail in git
- Previous version is still in stage

## Image Tag Strategy

### SHA Tags (Recommended)
```
Format: sha-<8-char-git-sha>
Example: sha-abc12345

Benefits:
✅ Immutable (never changes)
✅ Traceable to source code commit
✅ No tag collisions
✅ Easy to identify builds
```

### Semantic Versioning
```
Format: vMAJOR.MINOR.PATCH
Example: v1.2.3

Benefits:
✅ Human-readable
✅ Conveys compatibility
✅ Standard practice

Challenges:
❌ Must update in kustomization
❌ Risk of tag reuse
```

### Latest Tag (Not Recommended)
```
Format: latest

Challenges:
❌ Mutable (changes frequently)
❌ Not traceable
❌ Can't promote (always latest)
❌ Breaks gold-standard workflow
```

## Environment Configuration

### Dev Environment
- **Replicas**: 2
- **Image Tag**: Latest SHA from `main` branch
- **Logging**: DEBUG
- **Resources**: Minimal (50m CPU, 64Mi memory)
- **Auto-Sync**: ✅ Enabled (immediate deployment)
- **Purpose**: Rapid testing of new features

### Stage Environment
- **Replicas**: 2
- **Image Tag**: Promoted from dev
- **Logging**: INFO
- **Resources**: Standard (100m CPU, 128Mi memory)
- **Auto-Sync**: ✅ Enabled (after PR merge)
- **Purpose**: Integration testing, pre-production validation

### Production Environment
- **Replicas**: 3
- **Image Tag**: Promoted from stage
- **Logging**: WARN (minimal)
- **Resources**: High (200m CPU, 1Gi memory)
- **Auto-Sync**: ❌ Disabled (manual approval required)
- **Purpose**: Live user traffic

## Monitoring Deployments

### Health Checks

```powershell
# Deployment status
kubectl rollout status deployment/dex -n dex-stage

# Pod health
kubectl get pods -n dex-stage

# Events
kubectl get events -n dex-stage --sort-by='.lastTimestamp'

# Logs
kubectl logs -f deployment/dex -n dex-stage

# ArgoCD sync status
argocd app get dex-stage
```

### Verification Tests

```powershell
# Port forward
kubectl port-forward -n dex-stage svc/dex 8000:8000

# Health endpoint
curl http://localhost:8000/health

# Readiness endpoint
curl http://localhost:8000/ready

# API docs (Swagger)
Start-Process http://localhost:8000/docs
```

## Automation Opportunities

### Future Enhancements

**Automated Stage Promotion**:
```yaml
# .github/workflows/auto-promote-stage.yml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  promote-if-stable:
    runs-on: ubuntu-latest
    steps:
      - name: Check dev health
        run: |
          # Run health checks against dev
          # If stable for >2 hours, promote
      - name: Promote to stage
        run: pwsh scripts/promote.ps1 -FromEnv dev -ToEnv stage -AutoMerge
```

**Smoke Tests Before Promotion**:
```yaml
# .github/workflows/pre-promotion-tests.yml
on:
  pull_request:
    paths:
      - 'infra/argocd/overlays/prod/**'

jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run smoke tests against stage
        run: |
          pytest tests/smoke/ --env stage
```

**Deployment Notifications**:
```yaml
# .github/workflows/notify-deployment.yml
on:
  push:
    paths:
      - 'infra/argocd/overlays/prod/**'

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Slack notification
        run: |
          curl -X POST $SLACK_WEBHOOK \
            -d '{"text":"Production deployment in progress: $IMAGE_TAG"}'
```

## Security Considerations

### Image Scanning
- ✅ Trivy scan on every build (CI)
- ✅ SARIF results uploaded to GitHub Security
- ✅ Critical vulnerabilities block promotion

### Access Control
- ✅ PR reviews required for stage/prod promotions
- ✅ CODEOWNERS file enforces approvals
- ✅ Branch protection on `main`
- ✅ ArgoCD RBAC restricts manual syncs

### Secrets Management
- ✅ No secrets in kustomization.yaml
- 🔜 TODO: Sealed Secrets or External Secrets Operator
- 🔜 TODO: Rotate secrets regularly

## Troubleshooting

### ArgoCD won't sync
```powershell
# Force refresh
argocd app refresh dex-stage

# Check sync status
argocd app get dex-stage

# View sync errors
argocd app logs dex-stage
```

### Image not found
```powershell
# Verify image exists in registry
docker pull ghcr.io/data-literate/dex:sha-abc12345

# Check imagePullSecrets
kubectl get secret -n dex-stage
```

### Deployment fails health checks
```powershell
# Check pod describe
kubectl describe pod <pod-name> -n dex-stage

# Check logs
kubectl logs <pod-name> -n dex-stage

# Check resource limits
kubectl top pods -n dex-stage
```

## References

- [Promotion Scripts](../scripts/README.md)
- [ArgoCD Sync Waves](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)
- [Kustomize Overlays](https://kubectl.docs.kubernetes.io/references/kustomize/overlays/)
- [12-Factor App: Build, Release, Run](https://12factor.net/build-release-run)
