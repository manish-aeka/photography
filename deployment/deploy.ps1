# Auto Git Deploy Script
# This PowerShell script automatically adds, commits, and pushes changes to the repository

# ================================
# CONFIGURATION
# ================================
# Branch name (will use current branch if empty)
$TARGET_BRANCH = ""

# Specific files/folders to include in deployment (relative to repository root)
$INCLUDE_FILES = @(
    "data/*.json"
)

Write-Host "================================" -ForegroundColor Blue
Write-Host "  Auto Git Deploy Script" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue
Write-Host ""

# Change to repository root
Set-Location "$PSScriptRoot\.."
Write-Host "Working directory: $(Get-Location)" -ForegroundColor Blue
Write-Host ""

# Check if data folder exists
if (-not (Test-Path "data")) {
    Write-Host "[ERROR] data/ folder not found in root directory" -ForegroundColor Red
    exit 1
}

# Check if any JSON files exist in data folder
$jsonFiles = Get-ChildItem "data\*.json" -ErrorAction SilentlyContinue
if (-not $jsonFiles) {
    Write-Host "[ERROR] No .json files found in data/ folder" -ForegroundColor Red
    exit 1
}

# Check if there are any changes to JSON files in data folder
$dataJsonChanges = git status --short data/*.json 2>$null
if ([string]::IsNullOrWhiteSpace($dataJsonChanges)) {
    Write-Host "No changes to .json files in data/ folder." -ForegroundColor Green
    Write-Host "Working directory clean for deployment files." -ForegroundColor Blue
    exit 0
}

# Show current status of data JSON files
Write-Host "Changes in data/ folder:" -ForegroundColor Blue
git status --short data/*.json
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

# Determine target branch
if ([string]::IsNullOrWhiteSpace($TARGET_BRANCH)) {
    $branch = git branch --show-current
    Write-Host "Using current branch: $branch" -ForegroundColor Blue
} else {
    $branch = $TARGET_BRANCH
    Write-Host "Using configured branch: $branch" -ForegroundColor Blue
    
    # Switch to target branch if not already on it
    $currentBranch = git branch --show-current
    if ($currentBranch -ne $branch) {
        Write-Host "Switching to branch: $branch" -ForegroundColor Blue
        git checkout $branch
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to switch to branch $branch" -ForegroundColor Red
            exit 1
        }
        Write-Host "[OK] Switched to $branch" -ForegroundColor Green
    }
}
Write-Host ""

# Add .json files from data/ folder
Write-Host "Adding .json files from data/ folder..." -ForegroundColor Blue

$addedCount = 0
foreach ($file in $INCLUDE_FILES) {
    $matchingFiles = Get-ChildItem $file -ErrorAction SilentlyContinue
    if ($matchingFiles) {
        Write-Host "  Including: $file" -ForegroundColor Green
        git add $file
        if ($LASTEXITCODE -eq 0) {
            $addedCount++
        } else {
            Write-Host "[ERROR] Failed to add $file" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "  Warning: No files matching $file" -ForegroundColor Red
    }
}

if ($addedCount -eq 0) {
    Write-Host "[ERROR] No files were added" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Successfully added $addedCount file(s)" -ForegroundColor Green
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
