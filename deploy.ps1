# Auto Git Deploy Script
# This PowerShell script automatically adds, commits, and pushes changes to the repository

Write-Host "================================" -ForegroundColor Blue
Write-Host "  Auto Git Deploy Script" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue
Write-Host ""

# Check if there are any changes
$status = git status --short
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No changes to commit. Working directory clean." -ForegroundColor Green
    exit 0
}

# Show current status
Write-Host "Current Status:" -ForegroundColor Blue
git status --short
Write-Host ""

# Get commit message from parameter or use default
if ($args.Count -eq 0) {
    $commitMsg = "Auto commit: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host "Using default commit message: $commitMsg" -ForegroundColor Blue
} else {
    $commitMsg = $args -join " "
    Write-Host "Commit message: $commitMsg" -ForegroundColor Blue
}
Write-Host ""

# Get current branch
$branch = git branch --show-current
Write-Host "Current branch: $branch" -ForegroundColor Blue
Write-Host ""

# Add all changes
Write-Host "Adding all changes..." -ForegroundColor Blue
git add .

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Files added successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to add files" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Blue
git commit -m $commitMsg

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Committed successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to commit" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Push to remote
Write-Host "Pushing to origin/$branch..." -ForegroundColor Blue
git push origin $branch

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Pushed successfully to origin/$branch" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to push" -ForegroundColor Red
    Write-Host "Trying to set upstream..." -ForegroundColor Blue
    git push -u origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Pushed successfully with upstream set" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to push" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

Write-Host "================================" -ForegroundColor Green
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
