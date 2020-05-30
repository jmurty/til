# Keep the message when amending files in the last commit

I often need to tweak my most recent commit to change its file content, but
I don't always want to adjust the commit message.

To quickly amend a commit with changes from the index without being prompted to
edit and confirm the message, use the `--no-edit` option:

```bash
git commit --amend --no-edit
```

Thanks to https://stackoverflow.com/a/10365442/4970
