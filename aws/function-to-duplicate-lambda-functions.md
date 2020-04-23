# Use a Lambda function to duplicate other functions

Unfortunately neither the AWS web console nor the command line tools have a
feature to duplicate a function in the service.

This is a glaring oversight that makes it difficult to do seemingly simple
things, like create new functions from a "template" function or rename a
function (which is also not possible directly) by creating a copy with a
different name.

The easiest way I have found to do this job is to create a Lambda function that
duplicates *other* functions.

This **[do_duplicate_function.py](do_duplicate_function.py)** Python 3 function
code can be deployed to Lambda, or be run locally, to duplicate a function in
your AWS account.

To use it, configure a test event in the AWS console or otherwise invoke the
function with event data containing at least:

```json
{
    "SourceFunctionName": "function_name_to_copy",
    "FunctionName": "function_name_to_create"
}
```

Where `SourceFunctionName` is the name of a function to be duplicated, and
`FunctionName` is the name of the function to create.

There is more documentation at the top of the function code itself about how to
use it and deploy it, see the code for details.
