# PowerShell script to push to GitHub
# Run this after creating the repository on GitHub

Write-Host "Connecting to GitHub repository..." -ForegroundColor Cyan

# Add remote (if not already added)
$remoteExists = git remote get-url origin 2>$null
if (-not $remoteExists) {
    Write-Host "Adding remote repository..." -ForegroundColor Yellow
    git remote add origin https://github.com/shaileshmalkar/Secure-Doc-Share.git
} else {
    Write-Host "Remote already exists: $remoteExists" -ForegroundColor Green
}

# Check current branch
$currentBranch = git branch --show-current
Write-Host "Current branch: $currentBranch" -ForegroundColor Cyan

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repository URL: https://github.com/shaileshmalkar/Secure-Doc-Share" -ForegroundColor Cyan
} else {
    Write-Host "`n✗ Push failed. Common issues:" -ForegroundColor Red
    Write-Host "  1. Repository doesn't exist on GitHub yet" -ForegroundColor Yellow
    Write-Host "  2. Authentication required (use Personal Access Token)" -ForegroundColor Yellow
    Write-Host "  3. Check SETUP_GITHUB.md for detailed instructions" -ForegroundColor Yellow
}
