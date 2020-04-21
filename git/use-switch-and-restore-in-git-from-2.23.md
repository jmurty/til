# Use `switch` and `restore` commands in Git from 2.23

Since version 2.23 Git supports two new subcommands intended to replace the
overly-powerful and confusing `checkout`.

There's a great discussion of these commands with examples here:
https://github.blog/2019-08-16-highlights-from-git-2-23/

`git switch` examples:

- `git switch branchname` to switch to (checkout) a branch
- `git switch -c branchname` to create and switch to a branch (like `checkout -b`)
- `git switch -c branchname starting-point` to create and switch to a branch based on `starting-point`

`git restore` examples:

- `git restore path/to/file` to reset a file in your working copy, leaving the index intact
- `git restore --source=master --staged path/to/file` to put the version of a file from `master` into your index
  - specify the `--worktree` option as well or instead to also put the `master` version in your local copy

Full documentation for [git switch](https://git-scm.com/docs/git-switch/2.23.0)
and [git restore](https://git-scm.com/docs/git-restore/2.23.0)
