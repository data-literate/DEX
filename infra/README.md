# Infrastructure-as-Code (IaC) Guide

This folder contains all infrastructure configuration for DEX using **Kustomize** and **ArgoCD**.

## Folder Structure

```
infra/
├── README.md                 # This file
├── application.yaml          # ArgoCD Application, ApplicationSet, AppProject definitions
└── argocd/
    ├── base/                 # Base Kubernetes manifests (shared across all environments)
    │   ├── kustomization.yaml
    │   ├── deployment.yaml
    │   └── service.yaml
    └── overlays/             # Environment-specific patches
        ├── dev/              # Development (1 replica, latest image, debug logging)
        ├── stage/            # Staging (2 replicas, v1.0.0 image, info logging)
        ├── prod/             # Production (3 replicas, v1.0.0 image, warn logging)
        └── preview/          # PR Preview (2 replicas, ephemeral namespaces, debug logging)
```

## Kustomize Overlays

### Base (`argocd/base/`)
- **deployment.yaml**: 2 replicas, http port 8000, liveness/readiness probes
- **service.yaml**: ClusterIP service on port 8000
- **kustomization.yaml**: Image tag v1.0.0 (overridden by overlays)

### Development (`argocd/overlays/dev/`)
- **Replicas**: 1 (testing)
- **Image Tag**: `latest` (from main branch)
- **Logging**: `DEBUG`
- **Resources**: 50m CPU / 64Mi memory
- **Namespace**: `dex-dev`
- **Auto-sync**: Enabled (immediate ArgoCD sync on git commit)

### Staging (`argocd/overlays/stage/`)
- **Replicas**: 2 (HA testing)
- **Image Tag**: `v1.0.0` (pinned version for promotion)
- **Logging**: `INFO`
- **Resources**: 100m CPU / 128Mi memory
- **Namespace**: `dex-stage`
- **Auto-sync**: Enabled

### Production (`argocd/overlays/prod/`)
- **Replicas**: 3 (high availability)
- **Image Tag**: `v1.0.0` (pinned version for promotion)
- **Logging**: `WARN` (minimal)
- **Resources**: 200m CPU / 1Gi memory
- **Namespace**: `dex` (default prod namespace)
- **Auto-sync**: **Disabled** (manual approval required)

### PR Preview (`argocd/overlays/preview/`)
- **Replicas**: 2
- **Image Tag**: SHA from PR commit (set by ApplicationSet template)
- **Logging**: `DEBUG`
- **Resources**: 50m CPU / 64Mi memory (same as dev)
- **Namespace**: `dex-pr-{{pr_number}}` (ephemeral, auto-cleanup on PR close)
- **Auto-sync**: Enabled

## ArgoCD Resources

### Application
Basic deployment resource pointing to base kustomization. Used as fallback/example.

### ApplicationSet - Multi-Environment
Generates 3 Applications from single template:
- `dex-dev` → `infra/argocd/overlays/dev`
- `dex-stage` → `infra/argocd/overlays/stage`
- `dex` (prod) → `infra/argocd/overlays/prod`

**Gold-Standard Workflow**: All environments use same immutable image tag (e.g., `v1.0.0`). CI/CD updates this tag in git, ArgoCD syncs automatically (or manually for prod).

### ApplicationSet - PR Preview
Generates ephemeral Applications per PR (with `preview` label):
- Namespace: `dex-pr-{{pr_number}}`
- Image: `data-literate/dex:sha-{{commit_short_sha}}`
- Auto-deletes when PR closes

### AppProject
RBAC and source/destination restrictions:
- **Allowed Repos**: `https://github.com/data-literate/DEX` (co-located config + code)
- **Allowed Namespaces**: `dex-*`, `dex-pr-*`, `default`
- **Server**: `https://kubernetes.default.svc` (local cluster)

## Promotion Workflow

### Build Phase (GitHub Actions CI)
1. Lint/test code
2. Build Docker image: `data-literate/dex:sha-XXXXXXXX` (8-char commit SHA)
3. Push to registry: `ghcr.io/data-literate/dex:sha-XXXXXXXX`
4. **Commit 1**: Update `infra/argocd/overlays/dev/kustomization.yaml`
   ```yaml
   images:
     - name: data-literate/dex
       newTag: sha-XXXXXXXX
   ```
   ArgoCD auto-syncs dev environment

### Promote to Staging
1. Create PR: Update `infra/argocd/overlays/stage/kustomization.yaml` with same SHA
2. Review + merge PR (audit trail in git)
3. ArgoCD auto-syncs stage with same image

### Promote to Production
1. Create PR: Update `infra/argocd/overlays/prod/kustomization.yaml` with same SHA
2. Review + approve PR (manual gate)
3. Merge PR
4. **Manual**: `argocd app sync dex` in prod cluster (requires approval)
5. Rollback: `git revert` → ArgoCD syncs to previous version

## Local Testing on Docker Desktop

### 1. Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Access ArgoCD UI
```bash
kubectl port-forward -n argocd svc/argocd-server 8080:443
# Login: admin / <generated password from kubectl>
```

### 3. Deploy Application
```bash
kubectl apply -f infra/application.yaml
```

### 4. Test Sync
```bash
argocd app list
argocd app get dex-dev
argocd app sync dex-dev
```

### 5. View Application
```bash
kubectl port-forward -n dex-dev svc/dex 8000:8000
# Visit http://localhost:8000
```

## Image Registry

Currently configured for:
```
ghcr.io/data-literate/dex:TAG
```

Update `infra/argocd/base/kustomization.yaml` for different registry:
```yaml
images:
  - name: data-literate/dex
    newName: <your-registry>/dex
    newTag: v1.0.0
```

## Kustomize Commands

### Preview overlay
```bash
cd infra/argocd
kustomize build overlays/dev
kustomize build overlays/stage
kustomize build overlays/prod
kustomize build overlays/preview
```

### Apply overlay (ArgoCD does this automatically)
```bash
kubectl apply -k infra/argocd/overlays/dev
```

## Secrets Management

### Current Setup (TODO)
- [ ] Set up `sealed-secrets` or `External Secrets Operator`
- [ ] Store DB credentials, API keys in vault
- [ ] Reference secrets in deployment.yaml via `secretKeyRef`

### Future: GitOps-Friendly Secrets
```yaml
# After sealed-secrets setup:
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: dex-secrets
spec:
  encryptedData:
    DB_PASSWORD: AgBvxQ...
    GITHUB_TOKEN: AgCx2k...
```

## Troubleshooting

### ArgoCD won't sync
```bash
argocd app get dex-dev
argocd app logs dex-dev
kubectl describe application dex-dev -n argocd
```

### Kustomize build error
```bash
cd infra/argocd
kustomize build overlays/dev
# Check for invalid image tags, base path errors
```

### Image not updating
- Verify CI pushed image: `docker pull ghcr.io/data-literate/dex:sha-XXXXXXXX`
- Verify git commit updated kustomization.yaml: `git log infra/argocd/overlays/dev/kustomization.yaml`
- Force ArgoCD refresh: `argocd app refresh dex-dev`

## References

- [Kustomize Documentation](https://kustomize.io/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [12-Factor App](https://12factor.net/) - Environment-specific config patterns

---

## Future: Infrastructure Modules

When expanding beyond Kubernetes:
- `infra/terraform/` — Cloud infrastructure (AWS/GCP/Azure)
- `infra/helm/` — Helm charts for complex deployments
- `infra/scripts/` — Setup and operational scripts

Do not store sensitive secrets in the repo. Use cloud secret manager, Vault, or sealed-secrets.
