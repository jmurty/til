# Show patch diff for merge commits in `git log`

The `--patch` / `-p` option for `git log` prints a diff of changes made by each
commit, but this ignores merge commits by default and only shows the merge
message not its diff.

Use the `-m` option to also print merge diffs:

```bash
git log -p -m
```

From [the
manual](https://git-scm.com/docs/git-log#Documentation/git-log.txt--m):

> This flag makes the merge commits show the full diff like regular commits;
> for each merge parent, a separate log entry and diff is generated. An
> exception is that only diff against the first parent is shown when
> `--first-parent` option is given; in that case, the output represents the
> changes the merge brought **into** the then-current branch.
