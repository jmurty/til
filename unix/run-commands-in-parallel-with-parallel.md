# Run commands in parallel with GNU `parallel`

GNU [parallel](https://www.gnu.org/software/parallel/) is:

> a shell tool for executing jobs in parallel using one or more computers.

It can be used as a drop-in replacement for `xargs`: many (maybe all) of the
`xargs` parameters work the same way.

But `parallel` is much better than `xargs` for handling tricky input data, such
as lines of JSON data or anything with special quote or other characters which
tend to [break or require ugly workarounds with `xargs`][so-xargs-hacks].

Install it on MacOS with `brew install parallel`

## Example usage

Given *data.jsonl* that contains JSON objects separated by newlines, send each
object to an AWS SQS queue with no more than 50 simultaneous commands at a time:

```sh
export SQS_URL="https://sqs.amazonaws.com/1234567890/my-sqs-queue"

<data.jsonl parallel -P 50 -I % \
  aws sqs send-message --queue-url "$SQS_URL" --message-body %
```

NOTE: This example is very inefficient since it spawns a whole new command run
for every object, but is a nice demo of getting something done even if it's in
a quick and dirty way.

[so-xargs-hacks]: https://unix.stackexchange.com/questions/38148/why-does-xargs-strip-quotes-from-input
