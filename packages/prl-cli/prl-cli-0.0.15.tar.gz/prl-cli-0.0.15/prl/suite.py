import json
import os
import sys
from io import TextIOWrapper
from typing import Any, Dict

import click
import requests
from gql import gql
from jsonschema import ValidationError, validate
from prl.auth import get_auth_token
from prl.exceptions import PrlException

from .util import (
    SUITE_SCHEMA_PATH,
    be_host,
    display_error_and_exit,
    fe_host,
    get_client,
    list_test_suites,
    prompt_user_for_suite,
)

UNARY_OPERATORS = [
    "is_concise",
    "no_legal_advice",
    "valid_json",
    "valid_yaml",
    "list_format",
    "paragraph_format",
    "affirmative_answer",
    "negative_answer",
    "answers",
    "not_answers",
]


@click.group()
def suite():
    """
    Start, create, or view tests and test suites
    """
    pass


def parse_suite_interactive():
    title = click.prompt("Test Suite Title")
    while title == "":
        title = click.prompt("Title cannot be empty. Reenter")

    description = click.prompt("Test Suite Description")

    i = 1
    keep_generating_prompts = True
    tests = []
    while keep_generating_prompts:
        click.secho(f"---Test {i}---", bold=True)
        input_under_test = click.prompt("Input under test (e.g. the prompt)")

        keep_generating_criteria = True
        j = 1
        checks = []
        while keep_generating_criteria:
            operator = click.prompt(f"Operator {j}")
            criteria = click.prompt(f"Criteria {j}")
            checks.append({"criteria": criteria, "operator": operator})
            j += 1

            keep_generating_criteria = click.confirm("Keep Generating Checks?")

        i += 1

        tests.append({"input_under_test": input_under_test, "checks": checks})
        keep_generating_prompts = click.confirm("Keep generating tests?")

    return {"title": title, "description": description, "tests": tests}


def validate_checks(checks):
    for check in checks:
        operator = check["operator"]
        if operator not in UNARY_OPERATORS and "criteria" not in check:
            raise PrlException(
                f"'criteria' field must be specified for check with operator: '{operator}'"
            )


def parse_suite_file(file):
    # TODO: Validate file format
    try:
        parsed_json = json.load(file)
    except Exception as e:
        raise PrlException("The input file provided is not valid JSON")

    if not os.path.exists(SUITE_SCHEMA_PATH):
        raise PrlException(
            "Could not find schema file. The CLI tool is likely misconfigured."
        )

    # Use jsonschema to do most of our validation
    try:
        with open(SUITE_SCHEMA_PATH, "r") as schema_file:
            schema = json.load(schema_file)
            validate(instance=parsed_json, schema=schema)
    except ValidationError as e:
        raise PrlException(
            f"The file provided did not conform to the correct format. Validation Error: {e.message}. Look at the examples or the jsonschema to see the correct format."
        )

    if "global_checks" in parsed_json:
        validate_checks(parsed_json["global_checks"])

    # We need to do some custom validation that JSON schema doesn't support
    tests = parsed_json["tests"]
    for test in tests:
        if "input_under_test" not in test and "file_under_test" not in test:
            raise PrlException(
                "For all tests, either 'input_under_test' or 'file_under_test' must be provided"
            )
        if "input_under_test" in test and "file_under_test" in test:
            raise PrlException(
                "Both input_under_test and file_under_test were defined for a test. Only one should be specified."
            )

        if "file_under_test" in test:
            fp = test["file_under_test"]
            if not os.path.exists(fp):
                raise PrlException(f"File does not exist: {fp}")
            if not os.path.isfile(fp):
                raise PrlException(f"Path is a directory: {fp}")

        validate_checks(test["checks"])
    return parsed_json


def upload_file(suite_id: str, file_path: str) -> str:
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{be_host()}/upload_file/?test_suite_id={suite_id}",
            files={"file": f},
            headers={"Authorization": get_auth_token()},
        )
        if response.status_code != 200:
            raise Exception(f"Failed to upload file {file_path}")
        return response.json()["file_id"]


def upload_files(suite_id: str, data: Dict[str, Any]):
    # Map from file path to file id
    files = {}
    for test in data["tests"]:
        if "file_under_test" in test:
            file_path = test["file_under_test"]
            files[file_path] = upload_file(suite_id, file_path)
        if "file_fixed_output" in test:
            file_path = test["file_fixed_output"]
            files[file_path] = upload_file(suite_id, file_path)
    return files


def create_test_suite(data: Dict[str, Any]) -> str:
    query = gql(
        f"""
    mutation createTestSuite {{
        updateTestSuite(
            description: "{data['description']}",
            testSuiteId: "0",
            title: "{data['title']}"
        ) {{
            testSuite {{
            description
            id
            org
            title
            }}
        }}
    }}
    """
    )
    result = get_client().execute(query)
    suite_id = result["updateTestSuite"]["testSuite"]["id"]
    return suite_id


def add_global_checks(data, suite_id):
    if "global_checks" not in data:
        return

    query = gql(
        f"""
    mutation mutateGlobalChecks {{
        updateGlobalChecks (
            testSuiteId: "{suite_id}",
            checks: {json.dumps(json.dumps(data["global_checks"]))}
        ) {{
            success
        }}
    }}
    """
    )
    result = get_client().execute(query)


def add_tests(data, files, suite_id):
    test_ids = []
    for test in data["tests"]:
        # TODO: Escape chars better
        if "file_under_test" in test:
            file_path = test["file_under_test"]
            input_under_test = files[file_path]
            input_under_test_type = "file"
        else:
            input_under_test = test["input_under_test"]
            input_under_test_type = "raw"

        # TODO: avoid double json
        checks = json.dumps(json.dumps(test["checks"]))
        # TODO: Do this server side

        if "fixed_output" in test:
            fixed_output = test["fixed_output"]
            fixed_output_type = "raw"
        elif "file_fixed_output" in test:
            fixed_output = files[test["file_fixed_output"]]
            fixed_output_type = "file"
        else:
            fixed_output = ""
            fixed_output_type = "raw"

        query = gql(
            f"""
        mutation addUpdateTest {{
              updateTest(
                  sampleOutput: {json.dumps(fixed_output)},
                  sampleOutputType: "{fixed_output_type}",
                  checks: {checks}, 
                  inputUnderTest: {json.dumps(input_under_test)}, 
                  inputUnderTestType: "{input_under_test_type}",
                  testSuiteId: "{suite_id}") {{
                  test {{
                    testId
                  }}
                }}
            }}
            """
        )
        response = get_client().execute(query)
        test_ids.append(response["updateTest"]["test"]["testId"])

    test_id_list = ", ".join([f'"{test_id}"' for test_id in test_ids])
    query = gql(
        f"""
            mutation removeOldTests {{
              removeUnusedTests(
                  testSuiteId: "{suite_id}",
                  inUseTests: [{test_id_list}]
                ) {{
                    success
                }}
            }}
            """
    )
    response = get_client().execute(query)


def parse_suite(interactive: bool, file: TextIOWrapper) -> Dict[str, Any]:
    if not interactive and file is None:
        click.echo(
            "Either --interactive must be passed, or an input file should be specified"
        )
        sys.exit(1)

    if interactive:
        data = parse_suite_interactive()
    else:
        data = parse_suite_file(file)

    return data


@click.command()
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Enable interactive mode instead of reading from file",
)
@click.argument("file", type=click.File("r"), required=False)
def create(interactive: bool, file: str):
    """
    Creates a new test suite.

    There are two modes. In normal operation, inputs are read from a JSON file:

    \tprl suite create <filename>

    In interactive mode, the user is prompted for values:

    \tprl suite create --interactive

        Requires authentication to use.
    """
    # try:
    data = parse_suite(interactive, file)
    suite_id = create_test_suite(data)

    files = upload_files(suite_id, data)

    add_global_checks(data, suite_id)
    add_tests(data, files, suite_id)
    # Execute the query on the transport
    click.secho("Successfully created test suite.", fg="green")
    click.secho(f"{fe_host()}/view?test_suite_id={suite_id}", bold=True)


#  except Exception as e:
# click.secho("Suite Creation Failed. Error: " + str(e), fg="red")


def _update(suite_id: str, interactive: bool, file: str, quiet=False):
    data = parse_suite(interactive, file)

    files = upload_files(suite_id, data)

    add_tests(data, files, suite_id)
    add_global_checks(data, suite_id)

    # Execute the query on the transport
    if not quiet:
        click.secho("Successfully updated test suite.", fg="green")
        click.secho(f"{fe_host()}/view?test_suite_id={suite_id}", bold=True)


@click.command()
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Enable interactive mode instead of reading from file",
)
@click.argument("file", type=click.File("r"), required=False)
def update(interactive: bool, file: str):
    suite_id = prompt_user_for_suite()
    try:
        _update(suite_id, interactive, file)
    except PrlException as e:
        click.secho(e.message, fg="red")
    except Exception as e:
        click.secho("Suite Update Failed. Error:" + str(e), fg="red")


@click.command()
def list_():
    """
    List test suites associated with this organization
    """
    suites = list_test_suites()

    suite_text = "\n".join([f"{i}: {s['title']}" for i, s in enumerate(suites)])
    click.echo(suite_text)


def pull_(file: TextIOWrapper, suiteid: str, include_id=False):
    output = {}
    query = gql(
        f"""
        query getTestSuiteData {{
            testSuites(testSuiteId: "{suiteid}") {{
                description
                id
                org
                title
                created
                globalChecks
            }}
        }}
    """
    )

    response = get_client().execute(query)

    if len(response["testSuites"]) == 0:
        raise Exception(f"Unable to find test suite with id: {suiteid}")

    suite = response["testSuites"][0]
    output["title"] = suite["title"]
    output["description"] = suite["description"]

    query = gql(
        f"""
        query getTestData {{
            tests(testSuiteId: "{suiteid}") {{
                checks
                testId
                inputUnderTest
                inputUnderTestType
                sampleOutput
                sampleOutputType
            }}
        }}    
        """
    )
    response = get_client().execute(query)
    raw_tests = response["tests"]

    #  print(raw_tests[0])
    tests = []
    for raw_test in raw_tests:
        test = {}
        if include_id:
            test["id"] = raw_test["testId"]
        if raw_test["inputUnderTestType"] == "file":
            test["file_under_test"] = raw_test["inputUnderTest"]
        else:
            test["input_under_test"] = raw_test["inputUnderTest"]

        if raw_test["sampleOutput"] != "":
            if raw_test["sampleOutputType"] == "file":
                test["file_fixed_output"] = raw_test["sampleOutput"]
            else:
                test["fixed_output"] = raw_test["sampleOutput"]

        test["checks"] = json.loads(raw_test["checks"])
        tests.append(test)

    output["tests"] = tests

    file.write(json.dumps(output, indent=2))


@click.command()
@click.argument("file", type=click.File("w"), required=True)
def pull(file: TextIOWrapper):
    suiteid = prompt_user_for_suite()
    try:
        pull_(file, suiteid)
    except PrlException as e:
        display_error_and_exit(e.message)

    click.secho("Successfully pulled test suite.", fg="green")


suite.add_command(create)
suite.add_command(list_, "list")
suite.add_command(update)
suite.add_command(pull)
