#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Promote container image between environments in GitOps workflow

.DESCRIPTION
    Updates kustomization.yaml with new image tag and creates promotion PR
    Supports: dev → stage → prod promotion flow

.PARAMETER FromEnv
    Source environment (dev, stage)

.PARAMETER ToEnv
    Target environment (stage, prod)

.PARAMETER ImageTag
    Image tag to promote (e.g., sha-abc12345)
    If not specified, reads from source environment

.PARAMETER AutoMerge
    Automatically merge PR (requires permissions)

.EXAMPLE
    .\promote.ps1 -FromEnv dev -ToEnv stage
    Promotes current dev image tag to stage

.EXAMPLE
    .\promote.ps1 -FromEnv stage -ToEnv prod -ImageTag sha-abc12345
    Promotes specific image tag to production

.EXAMPLE
    .\promote.ps1 -FromEnv dev -ToEnv stage -AutoMerge
    Promotes and auto-merges PR (requires permissions)
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "stage")]
    [string]$FromEnv,

    [Parameter(Mandatory=$true)]
    [ValidateSet("stage", "prod")]
    [string]$ToEnv,

    [Parameter(Mandatory=$false)]
    [string]$ImageTag,

    [Parameter(Mandatory=$false)]
    [switch]$AutoMerge
)

# Validation
if ($FromEnv -eq "stage" -and $ToEnv -ne "prod") {
    Write-Error "Can only promote from stage to prod"
    exit 1
}

if ($FromEnv -eq "dev" -and $ToEnv -ne "stage") {
    Write-Error "Can only promote from dev to stage"
    exit 1
}

$ErrorActionPreference = "Stop"

# Paths
$repoRoot = Split-Path -Parent $PSScriptRoot
$fromKustomization = Join-Path $repoRoot "infra/argocd/overlays/$FromEnv/kustomization.yaml"
$toKustomization = Join-Path $repoRoot "infra/argocd/overlays/$ToEnv/kustomization.yaml"

Write-Host "🚀 Promoting from $FromEnv to $ToEnv" -ForegroundColor Cyan

# Get current image tag from source environment if not specified
if (-not $ImageTag) {
    Write-Host "📖 Reading image tag from $FromEnv environment..." -ForegroundColor Yellow
    
    $fromContent = Get-Content $fromKustomization -Raw
    if ($fromContent -match 'newTag:\s*(.+)') {
        $ImageTag = $matches[1].Trim()
        Write-Host "✅ Found image tag: $ImageTag" -ForegroundColor Green
    } else {
        Write-Error "Could not find image tag in $fromKustomization"
        exit 1
    }
}

# Verify image exists (optional - requires docker/registry access)
Write-Host "🔍 Verifying image tag format..." -ForegroundColor Yellow
if ($ImageTag -notmatch '^(sha-[a-f0-9]{8}|v\d+\.\d+\.\d+|latest)$') {
    Write-Warning "Image tag '$ImageTag' doesn't match expected format (sha-XXXXXXXX, vX.Y.Z, or latest)"
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y") {
        exit 1
    }
}

# Check for uncommitted changes
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Warning "You have uncommitted changes:"
    Write-Host $gitStatus
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y") {
        exit 1
    }
}

# Ensure we're on main branch
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "📌 Switching to main branch..." -ForegroundColor Yellow
    git checkout main
    git pull origin main
}

# Create promotion branch
$branchName = "promote-$ToEnv-$ImageTag"
Write-Host "🌿 Creating branch: $branchName" -ForegroundColor Yellow
git checkout -b $branchName

# Update target environment kustomization
Write-Host "📝 Updating $ToEnv kustomization.yaml..." -ForegroundColor Yellow
$toContent = Get-Content $toKustomization -Raw
$updatedContent = $toContent -replace '(newTag:\s*)(.+)', "`$1$ImageTag"
Set-Content -Path $toKustomization -Value $updatedContent -NoNewline

# Show diff
Write-Host "`n📊 Changes:" -ForegroundColor Cyan
git diff $toKustomization

# Commit changes
Write-Host "`n💾 Committing changes..." -ForegroundColor Yellow
git add $toKustomization
git commit -m "chore: promote $ImageTag to $ToEnv

Promoted from: $FromEnv
Image tag: $ImageTag
Environment: $ToEnv

This promotion was created via promote.ps1 script.
ArgoCD will sync $ToEnv environment after PR is merged."

# Push branch
Write-Host "📤 Pushing branch to remote..." -ForegroundColor Yellow
git push origin $branchName

# Create PR (requires gh CLI)
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "`n🔀 Creating pull request..." -ForegroundColor Cyan
    
    $prTitle = "Promote $ImageTag to $ToEnv"
    $prBody = @"
## Image Promotion

**From**: $FromEnv
**To**: $ToEnv
**Image Tag**: ``$ImageTag``

### Checklist
- [ ] Verify image tag is correct
- [ ] Check $FromEnv environment is stable
- [ ] Review deployment changes
$(if ($ToEnv -eq "prod") {
"- [ ] Notify team of production deployment
- [ ] Verify rollback plan
- [ ] Schedule deployment window (if required)"
})

### Post-Merge
After merging this PR:
1. ArgoCD will detect the change
$(if ($ToEnv -eq "prod") {
"2. **Manual sync required**: Run ``argocd app sync dex`` in ArgoCD UI"
} else {
"2. ArgoCD will auto-sync $ToEnv environment (~3 minutes)"
})
3. Monitor deployment: ``kubectl get pods -n dex-$ToEnv``
4. Verify health: ``kubectl rollout status deployment/dex -n dex-$ToEnv``

### Rollback
If issues occur:
````powershell
# Revert this commit
git revert HEAD
git push origin main

# Or use ArgoCD rollback
argocd app rollback dex-$ToEnv
````

---
*Automated promotion via promote.ps1*
"@

    if ($AutoMerge) {
        gh pr create --title $prTitle --body $prBody --base main --head $branchName --label "promotion" --label $ToEnv
        Write-Host "`n⏳ Waiting for CI checks..." -ForegroundColor Yellow
        gh pr merge $branchName --auto --squash
        Write-Host "✅ PR will auto-merge after checks pass" -ForegroundColor Green
    } else {
        gh pr create --title $prTitle --body $prBody --base main --head $branchName --label "promotion" --label $ToEnv
        Write-Host "✅ Pull request created!" -ForegroundColor Green
        Write-Host "Review and merge: $(gh pr view --web)" -ForegroundColor Cyan
    }
} else {
    Write-Warning "GitHub CLI (gh) not found. Please create PR manually:"
    Write-Host "  Branch: $branchName" -ForegroundColor Yellow
    Write-Host "  Title: Promote $ImageTag to $ToEnv" -ForegroundColor Yellow
}

# Switch back to main
Write-Host "`n🔄 Switching back to main branch..." -ForegroundColor Yellow
git checkout main

Write-Host "`n✨ Promotion complete!" -ForegroundColor Green
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "  • Image: $ImageTag" -ForegroundColor White
Write-Host "  • From: $FromEnv → To: $ToEnv" -ForegroundColor White
Write-Host "  • Branch: $branchName" -ForegroundColor White
Write-Host "`n⏭️  Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review and approve PR"
Write-Host "  2. Merge PR"
if ($ToEnv -eq "prod") {
    Write-Host "  3. Manually sync in ArgoCD: argocd app sync dex" -ForegroundColor Yellow
} else {
    Write-Host "  3. Wait for ArgoCD auto-sync (~3 minutes)"
}
Write-Host "  4. Verify deployment: kubectl get pods -n dex-$ToEnv"
