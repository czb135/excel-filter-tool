# How to Push This Project to GitHub

## Step 1: Configure Git (if not already done)

First, set your Git identity (replace with your actual name and email):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Or if you only want to set it for this repository:

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Step 2: Make Your First Commit

The repository is already initialized. Now commit your files:

```bash
git add .gitignore app.py filter_excel.py templates/ README.md
git commit -m "Initial commit: Excel filter web application with multiple filter types"
```

## Step 3: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., "excel-filter-tool")
5. **Don't** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 4: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these (replace `YOUR_USERNAME` and `REPO_NAME`):

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 5: Verify

Go to your GitHub repository page and you should see all your files!

## Future Updates

When you make changes, use these commands:

```bash
git add .
git commit -m "Description of your changes"
git push
```

## What's Included in the Repository

- `app.py` - Flask backend server
- `templates/index.html` - Web interface
- `filter_excel.py` - Standalone script version
- `README.md` - Project documentation
- `.gitignore` - Excludes Excel files, uploads, and Python cache

## What's Excluded (via .gitignore)

- Excel files (*.xlsx, *.xls)
- Uploads folder
- Python cache files
- IDE settings
- Environment files

