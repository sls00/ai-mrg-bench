# Nested git worktrees

Keep parallel checkouts **inside this repo**, not as siblings under `portfolio/`.

```bash
mkdir -p .worktrees
git fetch origin
git worktree add .worktrees/<short-name> -b <branch> origin/main
git worktree remove .worktrees/<short-name>
```

Existing agent worktrees may live under `.claude/worktrees/` — same idea (nested). Prefer `.worktrees/` for new manual/agent parallel checkouts going forward.

Do **not** create `../ai-mrg-bench-wt-*` directories in the portfolio root.
