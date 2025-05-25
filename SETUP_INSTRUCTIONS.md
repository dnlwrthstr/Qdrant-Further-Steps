# Repository Setup Instructions

According to the junie.md file, the following steps are needed to complete the repository setup:

## Steps Already Completed
1. Git repository has been initialized
2. .gitignore file has been created with the required content

## Resolving Git Lock File Issue
Before proceeding, you need to resolve the Git lock file issue:
```bash
rm -f .git/index.lock
```

## Steps to Complete
1. Make the initial commit with the .gitignore file:
   ```bash
   git add .gitignore
   git commit -m "Initial commit: project setup with .gitignore"
   ```

2. Create a new repository on GitHub (e.g., 'qdrant-evaluation')

3. Connect your local repository to the remote repository using:
   ```bash
   git remote add origin git@github.com:<your-username>/qdrant-evaluation.git
   ```

4. Push your local repository to GitHub:
   ```bash
   git push -u origin main
   ```

This will complete the initial setup as described in junie.md.

## Working with Features/Changes
Once the repository is set up, follow these steps for each new feature or fix:

1. Create a new branch:
   ```bash
   git checkout -b feature/short-description
   ```

2. Make your changes in code, notebook, scripts, etc.

3. Test it locally

4. Commit the changes:
   ```bash
   git add .
   git commit -m "Add/fix: clear message about the change"
   ```

5. Merge back to `main`:
   ```bash
   git checkout main
   git pull origin main  # get latest
   git merge feature/short-description
   ```

6. Push the updated main:
   ```bash
   git push origin main
   ```

7. Delete the feature branch (locally and remotely):
   ```bash
   git branch -d feature/short-description
   git push origin --delete feature/short-description
   ```
