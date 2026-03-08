# GitHub Repository Setup Guide

Follow these steps to push your Object Tracking project to GitHub.

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click **"+"** → **"New repository"**
3. Fill in details:
   - **Repository name**: `object-tracking`
   - **Description**: `Real-time multi-object tracking using YOLOv8 and DeepSORT`
   - **Visibility**: Public (if you want others to see it)
   - **Initialize repository**: Leave unchecked (we'll push existing files)
4. Click **"Create repository"**
5. Copy the repository URL (e.g., `https://github.com/yourusername/object-tracking.git`)

## Step 2: Initialize Local Git Repository

Open PowerShell in your project directory and run:

```powershell
# Navigate to project
cd "d:\New folder (3)"

# Initialize git
git init

# Add your name and email
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Step 3: Add Remote and Push

```powershell
# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/object-tracking.git

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Object tracking with YOLOv8 and DeepSORT"

# Push to GitHub (you'll need to authenticate)
git branch -M main
git push -u origin main
```

## Step 4: Authentication

GitHub requires authentication. Choose one:

### Option A: Personal Access Token (Recommended)
1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens**
2. Click **"Generate new token"**
3. Select scopes: `repo`, `read:user`
4. Generate and copy the token
5. When prompted for password, paste the token

### Option B: SSH Key
1. Generate SSH key:
   ```powershell
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```
2. Add to GitHub: **Settings** → **SSH and GPG keys** → **New SSH key**
3. (Then use SSH URL instead of HTTPS)

## Step 5: Verify Repository

Check on GitHub that all files are present:
- ✅ tracker.py
- ✅ config.py
- ✅ requirements.txt
- ✅ README.md
- ✅ QUICKSTART.md
- ✅ CONTRIBUTING.md
- ✅ LICENSE
- ✅ setup.py
- ✅ .gitignore

## Step 6: Update README

Edit the README.md to replace placeholder URLs:

```markdown
# Replace:
git clone https://github.com/yourusername/object-tracking.git

# Replace:
https://github.com/yourusername/object-tracking
```

## Step 7: Add Demo Files

Create a `/demos` folder and add:
1. **demo_output.mp4** - Your recorded tracking video
2. **demo_config.txt** - Configuration used for demo
3. **demo_results.txt** - Performance metrics

```powershell
mkdir demos
# Add your demo files here
git add demos/
git commit -m "Add demo video and configuration"
git push
```

## Updating Your Repository

After making changes:

```powershell
# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push
```

## Adding Contributors

Ask other contributors to:
1. Fork your repository
2. Clone their fork
3. Make changes on a feature branch
4. Submit a Pull Request

You can then review and merge their changes!

## Repository Badges

Add to top of README.md:

```markdown
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Stars](https://img.shields.io/github/stars/yourusername/object-tracking?style=social)
![Forks](https://img.shields.io/github/forks/yourusername/object-tracking?style=social)
```

## Advanced: GitHub Actions CI/CD

The `.github/workflows/python-package.yml` file automatically:
- Tests on Python 3.8, 3.9, 3.10, 3.11
- Runs linting checks
- Validates imports

View results in **Actions** tab on GitHub.

## Next Steps

1. ✅ Push to GitHub
2. ✅ Add demo video
3. ✅ Create releases
4. ✅ Set up GitHub Pages (optional)
5. ✅ Add more documentation

---

**Need Help?**
- GitHub Help: https://docs.github.com
- Git Tutorial: https://git-scm.com/book
- GitHub CLI: https://cli.github.com
