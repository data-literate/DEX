Deployment runbook (quick)

Pre-deploy checks:
- Ensure CI passed on the target commit
- Confirm the artifact (image or wheel) exists in registry/artifacts

Rollback steps:
- If using Kubernetes, rollback the deployment to previous image tag:
  `kubectl rollout undo deployment/<name>`
- If using cloud run, deploy previous revision.

Contacts:
- On-call / Pager (add team contacts here)
