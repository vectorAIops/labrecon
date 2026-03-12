# Git & Cursor Quick Reference for Beginners

**Useful links:**
[Next.js Docs](https://nextjs.org/docs) · [Tailwind Docs](https://tailwindcss.com/docs) · [Git Cheat Sheet (GitHub)](https://education.github.com/git-cheat-sheet-education.pdf) · [Cursor Docs](https://docs.cursor.com) · [Vercel Docs](https://vercel.com/docs)

---

## Cursor Keybinds

All keybinds show Windows/Linux first, Mac in parentheses.

| What it does | Keybind |
|---|---|
| Open/close terminal | `Ctrl + backtick` (`Cmd + backtick`) |
| Open command palette (search any action) | `Ctrl + Shift + P` (`Cmd + Shift + P`) |
| Quick open a file by name | `Ctrl + P` (`Cmd + P`) |
| Open AI chat (Claude Code panel) | `Ctrl + L` (`Cmd + L`) |
| Inline AI edit (edit code in place) | `Ctrl + K` (`Cmd + K`) |
| Toggle sidebar (file explorer) | `Ctrl + B` (`Cmd + B`) |
| Save file | `Ctrl + S` (`Cmd + S`) |
| Undo | `Ctrl + Z` (`Cmd + Z`) |
| Redo | `Ctrl + Shift + Z` (`Cmd + Shift + Z`) |
| Find in current file | `Ctrl + F` (`Cmd + F`) |
| Find across all files | `Ctrl + Shift + F` (`Cmd + Shift + F`) |
| Close current tab | `Ctrl + W` (`Cmd + W`) |
| Split editor (side by side) | `Ctrl + \` (`Cmd + \`) |
| Go to a specific line number | `Ctrl + G` (`Cmd + G`) |
| Comment/uncomment a line | `Ctrl + /` (`Cmd + /`) |
| Move a line up/down | `Alt + Up/Down` (`Option + Up/Down`) |
| Duplicate a line | `Shift + Alt + Down` (`Shift + Option + Down`) |
| Select the same word elsewhere | `Ctrl + D` (`Cmd + D`) — press repeatedly to select more |
| Pin a tab (keeps it open) | Right-click the tab → "Pin Tab" |

**The 5 you'll use most:** Open terminal, Quick open file, Find across files, Save, and Open AI chat.

---

## Terminal / Console Commands

These are typed into the terminal (the black panel at the bottom of Cursor).

| What you want to do | Command |
|---|---|
| Run dev server (see site locally) | `npm run dev` |
| Build the site (check for errors) | `npm run build` |
| Install dependencies | `npm install` |
| Stop a running process | `Ctrl + C` |
| Clear the terminal | `clear` |
| List files in current folder | `ls` |
| Move into a folder | `cd folder-name` |
| Go up one folder | `cd ..` |
| See where you are | `pwd` |
| Create a new folder | `mkdir folder-name` |
| Create nested folders | `mkdir -p path/to/folder` |
| Delete a file | `rm filename` |
| Delete a folder and everything in it | `rm -rf folder-name` (careful — no undo) |
| Copy a file | `cp source destination` |
| Move or rename a file | `mv old-name new-name` |

---

## Cursor Sidebar — What the Colors Mean

When you look at the file explorer on the left side of Cursor, you'll see colored letters next to some files. These tell you the Git status of that file — what's changed since your last commit.

| Color / Letter | What it means |
|---|---|
| **M** (orange/yellow) | **Modified** — you changed this file since the last commit |
| **U** (green) | **Untracked** — this is a brand new file Git hasn't seen before |
| **D** (red) | **Deleted** — this file was removed |
| **A** (green) | **Added** — new file that's been staged (marked for commit) |
| **C** (blue/teal) | **Conflict** — two changes overlap and Git doesn't know which to keep |
| Gray/dimmed filename | The file is in `.gitignore` — Git is ignoring it on purpose |
| No color/letter | Clean — nothing has changed since the last commit |

**The dot (●) next to folders** means something inside that folder has changed. You don't need to hunt — just look for the colored letters on individual files.

**Unsaved file indicator:** A dot on the file's tab (at the top) means you have unsaved changes. `Ctrl + S` to save.

---

## Cursor Interface — The Main Panels

```
┌──────────────┬────────────────────────────────┐
│              │                                │
│   Sidebar    │         Editor                 │
│  (files)     │    (where you write code)      │
│              │                                │
│  Ctrl+B to   │                                │
│  toggle      │                                │
│              ├────────────────────────────────│
│              │         Terminal                │
│              │    (where you run commands)     │
│              │                                │
│              │  Ctrl+backtick to toggle        │
└──────────────┴────────────────────────────────┘
```

**Source Control panel:** Click the branch icon in the left sidebar (looks like a Y-shaped fork). Shows all your changed files. You can stage, commit, and see diffs from here without using the terminal.

**Search panel:** Click the magnifying glass in the left sidebar (or `Ctrl + Shift + F`). Search across every file in your project.

---

## Git Commands

### How It All Connects

```
Your Computer (local)  →  GitHub (remote)  →  Vercel (live site)
       ↑                       ↑                     ↑
  git commit              git push            auto-deploys from main
  (save point)         (send to GitHub)       (you don't control this)
```

Nothing goes live until changes reach the `main` branch on GitHub.

### Branches

A branch is a copy of your code you can experiment on without affecting the real site. Think of it like a "draft" — you can throw it away or merge it in when you're happy.

| What you want to do | Command |
|---|---|
| Create new branch and switch to it | `git checkout -b fix/my-description` |
| See what branch you're on | `git branch` |
| Switch back to main | `git checkout main` |
| Switch to existing branch | `git checkout branch-name` |
| Delete a branch (local) | `git branch -d branch-name` |

**Naming convention:** `fix/` for fixes, `feat/` for new features, `chore/` for cleanup.

### Saving Work (Commits)

A commit is a save point. Like a checkpoint in a video game — you can always go back to it.

| What you want to do | Command |
|---|---|
| See what changed | `git status` |
| See changes line by line | `git diff` |
| Stage all changes | `git add -A` |
| Stage one file | `git add path/to/file.ts` |
| Commit with message | `git commit -m "short description"` |
| Undo last commit (keep files) | `git reset --soft HEAD~1` |

**Commit message examples:**
- `fix: corrected CBC price for Quest`
- `feat: add individual test pages`
- `chore: update gitignore`

### Push / Pull

**Push** = send your local commits to GitHub.
**Pull** = download the latest changes from GitHub to your computer.

| What you want to do | Command |
|---|---|
| Push branch to GitHub | `git push origin branch-name` |
| Push main | `git push origin main` |
| Pull latest from GitHub | `git pull origin main` |
| First push of new branch | `git push -u origin branch-name` |

### The Safe Workflow (Use for Every Structural Change)

```
1.  git checkout main                   ← start from main
2.  git pull origin main                ← get latest
3.  git checkout -b feat/my-feature     ← create branch
4.  ... make changes ...
5.  git add -A                          ← stage
6.  git commit -m "feat: description"   ← save checkpoint
7.  git push -u origin feat/my-feature  ← send to GitHub
8.  Open Pull Request on GitHub         ← review changes
9.  Merge on GitHub                     ← this makes it live
10. git checkout main                   ← back to main locally
11. git pull origin main                ← sync
```

### Emergency Commands

| Situation | Command |
|---|---|
| Undo everything uncommitted | `git checkout -- .` |
| Undo last commit (not pushed) | `git reset --soft HEAD~1` |
| See recent history | `git log --oneline -10` |
| Throw away a branch | `git checkout main` then `git branch -D branch-name` |
| Pushed but haven't merged | Delete the branch in GitHub's UI (safer) |

---

## Common Beginner Questions

**"What does `npm run dev` actually do?"**
It starts a local web server on your computer (usually at `localhost:3000`). You can open that in your browser to see your site as you work on it. Changes show up almost instantly. It only runs while the terminal is open. Your live site is unaffected.

**"What's the difference between `npm run dev` and `npm run build`?"**
`dev` is for working — it runs a fast, live-updating version of your site locally. `build` compiles your entire site for production and catches errors. If `build` passes, your site will work on Vercel. If it fails, something's broken. Always run `build` before pushing structural changes.

**"What's `localhost:3000`?"**
A web address that only exists on your computer. When you run `npm run dev`, open your browser to `http://localhost:3000` to see your site. Nobody else can see it.

**"I see `node_modules/` — what is it?"**
A huge folder containing every library your project depends on. Created by `npm install`. Never edit it. It's in `.gitignore` so it doesn't go to GitHub. If it gets messed up, delete it and run `npm install` again.

**"What does 'stage' mean?"**
Staging is putting items in a box before shipping. `git add` puts changes in the box. `git commit` seals the box. `git push` ships it. You can put specific files in (`git add filename`) or everything (`git add -A`).

**"What's a Pull Request?"**
When you push a branch to GitHub, you can open a "Pull Request" (PR) — a proposal that says "here are my changes, review them before merging into main." GitHub shows a side-by-side diff of everything that changed. Review it, then merge when satisfied. It's a safety net.

**"Why does Cursor keep showing unsaved dots?"**
Cursor doesn't auto-save by default. The dot on a tab means unsaved changes. Hit `Ctrl + S` often. For auto-save: File → Preferences → Settings → search "auto save" → set to "afterDelay."

**"I ran a command and nothing happened."**
Some commands produce no output when they succeed. That's normal in terminals — no news is good news. If something went wrong, you'd see an error message. Run `git status` to check where things stand.

**"The terminal says 'permission denied'."**
Usually means you're trying to modify something you don't have access to. Don't use `sudo` unless you understand exactly why. Ask Claude Code what the error means before trying to force past it.

---

## Working with Claude Code in Cursor

**Always tell Claude Code at the start of structural tasks:**
- "Create a new branch called [name] before making changes"
- "Commit but do NOT push"
- "If the build fails, stop and report the error"

**Good to delegate to Claude Code:**
- Moving/renaming multiple files
- Adding boilerplate (sitemap, robots.txt, page templates)
- Searching for patterns across the repo
- Bulk find-and-replace
- Writing repetitive code

**Do these yourself (good practice):**
- Writing commit messages (helps you understand what changed)
- Reviewing diffs before committing (`git diff` or Source Control panel)
- Merging pull requests on GitHub (you should review first)
- Deciding when to push

**If Claude Code generates something you don't understand:**
Ask it to explain. Don't blindly commit code you can't read. Understanding what it does is how you learn.

---

## Rules of Thumb

1. One branch per task. Don't mix unrelated changes.
2. Commit often. Small commits are easier to undo.
3. Never `git push --force` unless you fully understand it.
4. Pull before you branch. Always start from latest main.
5. Read the diff on GitHub before clicking merge.
6. `npm run build` before pushing. If build fails, don't push.
7. When in doubt, make a branch. You can always throw it away.
8. Save your files before running terminal commands.
9. If something breaks — `git status` first, then `git diff`.
10. Don't be afraid to ask Claude to explain a command before running it.
