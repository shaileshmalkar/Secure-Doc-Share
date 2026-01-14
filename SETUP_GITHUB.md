# Setting up GitHub Repository

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `Secure-Doc-Share`
3. Description: "Secure document sharing application with encryption, S3 support, and responsive UI"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands:

```bash
cd C:\Shailesh\secure-doc-share

# Add remote (replace with your actual GitHub username if different)
git remote add origin https://github.com/shaileshmalkar/Secure-Doc-Share.git

# Or if using SSH:
# git remote add origin git@github.com:shaileshmalkar/Secure-Doc-Share.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify

Check your repository at:
https://github.com/shaileshmalkar/Secure-Doc-Share

## Authentication

If you get authentication errors:

### Option 1: Personal Access Token (Recommended)
1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Generate new token with `repo` permissions
3. Use token as password when pushing

### Option 2: SSH Keys
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add to GitHub: Settings > SSH and GPG keys > New SSH key
3. Use SSH URL for remote

## Quick Commands Reference

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your commit message"

# Push
git push

# Pull latest
git pull
```
