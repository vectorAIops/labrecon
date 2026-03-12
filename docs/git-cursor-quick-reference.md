# Git & Cursor Quick Reference for Beginners

## The Mental Model

```
Your Computer (local)  →  GitHub (remote)  →  Vercel (live site)
       ↑                       ↑                     ↑
  git commit              git push            auto-deploys from main
  (save point)         (send to GitHub)       (you don't control this)
```

Nothing goes live until changes reach the `main` branch on GitHub.

---

## Branches

| What you want to do                        | Command                                      |
|--------------------------------------------|----------------------------------------------|
| Create a new branch and switch to it       | `git checkout -b fix/my-description`         |
| See what branch you're on                  | `git branch`                                 |
| Switch back to main                        | `git checkout main`                          |
| Switch to an existing branch               | `git checkout branch-name`                   |
| Delete a branch you're done with (local)   | `git branch -d branch-name`                  |

**Branch naming convention:**
- `fix/description` — fixing something broken
- `feat/description` — adding something new
- `chore/description` — cleanup, organizing, no user-facing change

---

## Saving Your Work (Commits)

| What you want to do                        | Command                                      |
|--------------------------------------------|----------------------------------------------|
| See what files you changed                 | `git status`                                 |
| See the actual changes line by line        | `git diff`                                   |
| Stage all changes for commit               | `git add -A`                                 |
| Stage one specific file                    | `git add path/to/file.ts`                    |
| Commit with a message                      | `git commit -m "short description of change"`|
| Undo the last commit (keep the files)      | `git reset --soft HEAD~1`                    |

**Commit message format — keep it simple:**
- `fix: corrected CBC price for Quest`
- `feat: add individual test pages`
- `chore: update gitignore`

---

## Sending to GitHub (Push/Pull)

| What you want to do                        | Command                                      |
|--------------------------------------------|----------------------------------------------|
| Push your branch to GitHub                 | `git push origin branch-name`                |
| Push main to GitHub                        | `git push origin main`                       |
| Pull latest changes from GitHub            | `git pull origin main`                       |
| First time pushing a new branch            | `git push -u origin branch-name`             |

---

## The Safe Workflow (Use for Every Structural Change)

```
Step 1:  git checkout main                  ← start from main
Step 2:  git pull origin main               ← make sure you have latest
Step 3:  git checkout -b feat/my-feature    ← create your branch
Step 4:  ... make changes ...               ← work on your code
Step 5:  git add -A                         ← stage changes
Step 6:  git commit -m "feat: description"  ← save checkpoint
Step 7:  git push -u origin feat/my-feature ← send to GitHub
Step 8:  Go to GitHub → open Pull Request   ← review your changes
Step 9:  Merge on GitHub                    ← this makes it live
Step 10: git checkout main                  ← go back to main locally
Step 11: git pull origin main               ← sync with what you just merged
```

---

## Emergency Commands

| Situation                                 | Command                                       |
|-------------------------------------------|-----------------------------------------------|
| I want to undo everything I haven't committed | `git checkout -- .`                       |
| I committed but haven't pushed — undo it  | `git reset --soft HEAD~1`                     |
| I want to see what happened               | `git log --oneline -10`                       |
| I want to throw away this branch entirely | `git checkout main` then `git branch -D branch-name` |
| I pushed but haven't merged — just delete the branch on GitHub | Do it in GitHub's UI (safer) |

---

## Cursor / Terminal Basics

| What you want to do                        | Command                                      |
|--------------------------------------------|----------------------------------------------|
| Open terminal in Cursor                    | Ctrl + ` (backtick) or Cmd + ` on Mac        |
| Run the dev server (see your site locally) | `npm run dev`                                |
| Build the site (check for errors)          | `npm run build`                              |
| Install dependencies after cloning         | `npm install`                                |
| Stop a running process                     | Ctrl + C                                     |
| Clear the terminal                         | `clear` or Ctrl + L                          |
| See what's in a folder                     | `ls`                                         |
| Move into a folder                         | `cd folder-name`                             |
| Go up one folder                           | `cd ..`                                      |
| See where you are                          | `pwd`                                        |

---

## When to Use Claude Code vs Do It Yourself

**Tell Claude Code to do it:**
- Moving/renaming multiple files
- Adding boilerplate (sitemap, robots.txt, new page templates)
- Searching for patterns across the repo
- Bulk find-and-replace

**Do it yourself (good practice):**
- Writing commit messages
- Reviewing diffs before committing (`git diff`)
- Merging pull requests on GitHub
- Deciding when to push

**Always tell Claude Code:**
- "Create a new branch called [name] before making changes"
- "Commit but do NOT push"
- "If the build fails, stop and report the error"

---

## Rules of Thumb

1. One branch per task. Don't mix unrelated changes.
2. Commit often. Small commits are easier to undo than big ones.
3. Never force push (`git push --force`) unless you fully understand it.
4. Pull before you branch. Always start from the latest main.
5. Read before you merge. Look at the diff on GitHub before clicking merge.
