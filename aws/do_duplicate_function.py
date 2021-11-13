"""
This is a Python 3 utility function that creates a duplicate copy of another
function in this AWS account with the same configuration settings, environment
variables, etc.

In short, this does the job that should be handled by a "Duplicate" feature
that is missing from the AWS console and CLI.


Usage in AWS
------------

To use this function, configure a test event in the AWS console or otherwise
invoke the function with event data containing at least:


    {
        "SourceFunctionName": "function_name_to_copy",
        "FunctionName": "function_name_to_create"
    }

Where `SourceFunctionName` is the name of a function to be duplicated, and
`FunctionName` is the name of the function to create.

You can override configuration settings of the new function copy by including
extra optional variables in the event data like `Description`, `Timeout`,
`MemorySize`, etc to have your provided values override the values of the
source function's configuration.

See the parameters for the boto3 `create_function()` method for details:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.create_function


Usage locally
-------------

You can run this function locally without needing to deploy it to AWS Lambda at
all provided you meet these requirements:

- run it within a python3 virtualenv with `boto3` installed
- set up an AWS profile and credentials as for the AWS CLI tool, with
  sufficient permissions to do the work.

Once you have these in place, run the function like this:

    AWS_PROFILE=your-aws-profile \
        python3 do_duplicate_function.py \
        '{"SourceFunctionName": "fn_to_copy", "FunctionName": "fn_to_create"}'


Deployment to AWS
-----------------

Deploy this function with the Python 3.8 runtime (it might work on earlier
versions of Python 3 but hasn't been tested).

This function must have sufficient permissions to fetch and create Lambda
functions and to pass copy roles to the new function. To permit this, apply
something like the following permissions policy document to the deployed
function:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:CreateFunction",
                    "lambda:ListFunctions",
                    "lambda:GetFunction",
                    "iam:GetRole",
                    "iam:PassRole"
                ],
                "Resource": "*"
            }
        ]
    }

Author: James Murty (https://github.com/jmurty) License: MIT
"""
import os
import json
import sys

import boto3
import urllib3


def lambda_handler(event, context):
    # Optional envvar, only used to run functions locally
    aws_profile = os.environ.get("AWS_PROFILE")
    if aws_profile:
        session = boto3.Session(profile_name=aws_profile)
        lambda_client = session.client("lambda")
    else:
        lambda_client = boto3.client("lambda")

    # Fetch source function metadata
    function_data = lambda_client.get_function(
        FunctionName=event.pop("SourceFunctionName"),
        Qualifier=event.pop("SourceFunctionVersion", "$LATEST"),
    )
    function_data.pop("ResponseMetadata")

    # Download function code from temporary URL
    code_url = function_data.pop("Code")["Location"]
    http = urllib3.PoolManager()
    response = http.request("GET", code_url)
    if not 200 <= response.status < 300:
        raise Exception(f"Failed to download function code: {response}")
    function_code = response.data

    # Build metadata for new function based on original function's
    new_function_data = {
        n: v
        for n, v in function_data["Configuration"].items()
        if n in (
            "Runtime",
            "Role",
            "Handler",
            "Description",
            "Timeout",
            "MemorySize",
            "Publish",
            "Environment",
            "VpcConfig"
        )
    }
    if 'VpcConfig' in new_function_data:
        # Remove VpcId, because this parameter can't be used to create a new lambda function
        new_function_data['VpcConfig'].pop('VpcId', None)
    # Override function metadata values with those provided in event
    new_function_data.update(event)
    # Provide function code zip data
    new_function_data["Code"] = {"ZipFile": function_code}

    # Create a new function
    return lambda_client.create_function(**new_function_data)


# Support running this function locally
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <EVENT_JSON_TEXT_OR_FILE>")
        sys.exit(1)

    # Parse event data from JSON file path, or literal JSON
    try:
        with open(sys.argv[1], "rt") as f:
            event = json.load(f)
    except Exception:
        event = json.loads(sys.argv[1])

    context = None

    print(lambda_handler(event, context))
