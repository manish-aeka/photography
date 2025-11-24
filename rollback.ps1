# Git Rollback Script
# This PowerShell script rolls back to the previous commit

Write-Host "================================" -ForegroundColor Blue
Write-Host "  Git Rollback Script" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue
Write-Host ""

# Get current branch
$branch = git branch --show-current
Write-Host "Current branch: $branch" -ForegroundColor Blue
Write-Host ""

# Show last 5 commits
Write-Host "Last 5 commits:" -ForegroundColor Yellow
git log --oneline -5
Write-Host ""

# Confirm rollback
Write-Host "WARNING: This will undo the last commit and push to remote!" -ForegroundColor Red
$confirmation = Read-Host "Are you sure you want to rollback? (yes/no)"

if ($confirmation -ne "yes") {
    Write-Host "Rollback cancelled." -ForegroundColor Yellow
    exit 0
}
Write-Host ""

# Reset to previous commit (keep changes in working directory)
Write-Host "Rolling back to previous commit..." -ForegroundColor Blue
git reset --soft HEAD~1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Reset to previous commit successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to reset" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Force push to remote
Write-Host "Force pushing to origin/$branch..." -ForegroundColor Blue
git push origin $branch --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Rollback pushed successfully to origin/$branch" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to push rollback" -ForegroundColor Red
    Write-Host "You may need to manually resolve this." -ForegroundColor Yellow
    exit 1
}
Write-Host ""

Write-Host "================================" -ForegroundColor Green
Write-Host "  Rollback Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Note: Your changes are still in the working directory." -ForegroundColor Cyan
Write-Host "Use 'git status' to see the uncommitted changes." -ForegroundColor Cyan
