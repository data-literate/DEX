# Deployment Runbook

This runbook describes how to release and rollback DEX using the `dev` → `main` promotion flow.

## Environments

- **dev**: Deploys from `dev` branch via GitOps (auto-sync)
- **stage/prod**: Deploys from `main` branch via GitOps (auto-sync)

## Pre‑Deploy Checklist

- CI is green on the target branch (`dev` or `main`).
- Image exists in registry: `ghcr.io/data-literate/dex:sha-XXXXXXXX`.
- No open critical alerts in monitoring.
- For production release, approval recorded in PR.

## Deploy to Dev

**Trigger**: Merge PR into `dev` branch.

**Expected Outcome**:
- CD updates `infra/argocd/overlays/dev/kustomization.yaml` in `dev`.
- ArgoCD syncs `dex-dev` to the new SHA.

**Verify**:
```bash
kubectl get pods -n dex-dev
argocd app get dex-dev
```

## Deploy to Stage/Prod

**Trigger**: Merge release PR from `dev` → `main`.

**Expected Outcome**:
- CD updates `infra/argocd/overlays/stage/kustomization.yaml` and `infra/argocd/overlays/prod/kustomization.yaml` in `main`.
- ArgoCD syncs `dex-stage` and `dex-prod` to the new SHA.

**Verify**:
```bash
kubectl get pods -n dex-stage
kubectl get pods -n dex-prod
argocd app get dex-stage
argocd app get dex-prod
```

## Rollback

### Rollback Dev

```bash
git log --oneline infra/argocd/overlays/dev/kustomization.yaml
git revert <commit-sha>
git push origin dev
```

ArgoCD will sync `dex-dev` back to the previous image.

### Rollback Stage/Prod

```bash
git log --oneline infra/argocd/overlays/stage/kustomization.yaml
git revert <commit-sha>
git push origin main
```

ArgoCD will sync `dex-stage` and `dex-prod` back to the previous image.

## Emergency Rollback (Kubernetes)

If ArgoCD is unavailable, roll back directly:

```bash
kubectl rollout undo deployment/dex -n dex-stage
kubectl rollout undo deployment/dex -n dex-prod
```

Record the rollback by reverting the manifest in git once ArgoCD is available.

## Contacts

- On-call: add team contact
- Incident channel: add channel
