# Pull (fast forward) another branch

Pull upstream contents into a branch you are not currently on with:
```shell
git fetch <remote> otherbranch:otherbranch
```

For example, if you are on branch `feature-a` but your local `master` and
`staging` branches have fallen behind:

```shell
git fetch origin master:master staging:staging
```

As a bonus tab-complete often works very well for this.

Courtesy of https://stackoverflow.com/a/55144971/4970
