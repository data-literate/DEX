#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Get current deployed image tags across all environments

.DESCRIPTION
    Reads kustomization.yaml from all overlays and displays current image tags

.EXAMPLE
    .\get-tags.ps1
    Shows current image tags for dev, stage, and prod
#>

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$environments = @("dev", "stage", "prod")

Write-Host "`n🏷️  Current Image Tags" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Gray

foreach ($env in $environments) {
    $kustomization = Join-Path $repoRoot "infra/argocd/overlays/$env/kustomization.yaml"
    
    if (Test-Path $kustomization) {
        $content = Get-Content $kustomization -Raw
        
        if ($content -match 'newTag:\s*(.+)') {
            $tag = $matches[1].Trim()
            
            # Color based on tag type
            $color = switch -Regex ($tag) {
                '^sha-' { "Yellow" }
                '^v\d+\.\d+\.\d+' { "Green" }
                'latest' { "Red" }
                default { "White" }
            }
            
            Write-Host "  $($env.PadRight(10)) " -NoNewline -ForegroundColor White
            Write-Host $tag -ForegroundColor $color
        } else {
            Write-Host "  $($env.PadRight(10)) " -NoNewline -ForegroundColor White
            Write-Host "No tag found" -ForegroundColor Red
        }
    } else {
        Write-Host "  $($env.PadRight(10)) " -NoNewline -ForegroundColor White
        Write-Host "Kustomization not found" -ForegroundColor Red
    }
}

Write-Host ("=" * 60) -ForegroundColor Gray

# Check for image drift (different tags across environments)
$tags = @{}
foreach ($env in $environments) {
    $kustomization = Join-Path $repoRoot "infra/argocd/overlays/$env/kustomization.yaml"
    if (Test-Path $kustomization) {
        $content = Get-Content $kustomization -Raw
        if ($content -match 'newTag:\s*(.+)') {
            $tags[$env] = $matches[1].Trim()
        }
    }
}

if ($tags.Count -eq 3) {
    $devTag = $tags["dev"]
    $stageTag = $tags["stage"]
    $prodTag = $tags["prod"]
    
    Write-Host "`n📊 Environment Status:" -ForegroundColor Cyan
    
    if ($devTag -ne $stageTag) {
        Write-Host "  ⚠️  Dev and Stage are out of sync" -ForegroundColor Yellow
        Write-Host "     Run: .\scripts\promote.ps1 -FromEnv dev -ToEnv stage"
    } else {
        Write-Host "  ✅ Dev and Stage are in sync" -ForegroundColor Green
    }
    
    if ($stageTag -ne $prodTag) {
        Write-Host "  ⚠️  Stage and Prod are out of sync" -ForegroundColor Yellow
        Write-Host "     Run: .\scripts\promote.ps1 -FromEnv stage -ToEnv prod"
    } else {
        Write-Host "  ✅ Stage and Prod are in sync" -ForegroundColor Green
    }
}

Write-Host ""
