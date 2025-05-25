# 🧠 `junie.md`: Git Project Setup & Workflow Guide

## 📁 Initial Setup

1. **Initialize a Git repository**

```bash
cd "Qdrant Further Steps"
git init -b main
```

2. **Create `.gitignore`**

Create a file called `.gitignore` in the root of the project:

```bash
touch .gitignore
```

Add the following content:

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
*.egg
*.pyo
*.pyd
.Python
env/
venv/
.venv/
*.sqlite3

# Jupyter
.ipynb_checkpoints/

# MacOS
.DS_Store

# Environment Variables
.env

# VSCode or PyCharm
.vscode/
.idea/

# Output
*.log
*.out
*.tmp
```

3. **Add and commit files**

```bash
git add .
git commit -m "Initial commit: project setup with .gitignore"
```

4. **Create remote repository and push**

Go to GitHub and create a new repository, e.g., `qdrant-evaluation`.

Then run:

```bash
git remote add origin git@github.com:<your-username>/qdrant-evaluation.git
git push -u origin main
```

---

## 🔁 Working with Features/Changes

### For *each* new feature or fix:

1. **Create a new branch**

```bash
git checkout -b feature/short-description
```

2. **Make your changes** in code, notebook, scripts, etc.

3. **Test it locally**  
For example, run your script or notebook to verify that everything works.

4. **Commit the changes**

```bash
git add .
git commit -m "Add/fix: clear message about the change"
```

5. **Merge back to `main`**

```bash
git checkout main
git pull origin main  # get latest
git merge feature/short-description
```

6. **Push the updated main**

```bash
git push origin main
```

7. **Delete the feature branch (locally and remotely)**

```bash
git branch -d feature/short-description
git push origin --delete feature/short-description
```

---

## 🧪 Tips

- Always pull the latest main before starting a new branch.
- Keep branches focused on single concerns.
- Use `git status` often to verify what’s staged and what’s not.
