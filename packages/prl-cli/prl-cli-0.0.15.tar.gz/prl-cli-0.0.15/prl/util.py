import os
import sys

import click
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from .auth import get_auth_token, get_region

PLAYGROUND_ENV = os.getenv("PLAYGROUND_ENV")
client_ = None


def be_host():
    region = get_region()
    if region == "eu-north-1":
        return "https://europebe.playgroundrl.com"
    if PLAYGROUND_ENV == "LOCAL":
        return "http://localhost:8000"
    if PLAYGROUND_ENV == "DEV":
        return "https://devbe.playgroundrl.com"

    return "https://prodbe.playgroundrl.com"


def fe_host():
    region = get_region()
    if region == "eu-north-1":
        return "https://eu.playgroundrl.com"
    if PLAYGROUND_ENV == "LOCAL":
        return "http://localhost:3000"
    if PLAYGROUND_ENV == "DEV":
        return "https://dev.playgroundrl.com"

    return "https://playgroundrl.com"


SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "jsonschemas")
SUITE_SCHEMA_PATH = os.path.join(SCHEMA_PATH, "suiteschema.json")
RUN_SCHEMA_PATH = os.path.join(SCHEMA_PATH, "run_params_schema.json")


def display_error_and_exit(error_msg: str):
    click.secho("ERROR: " + error_msg, fg="red")
    sys.exit(1)


def get_client():
    global client_
    if client_ is None:
        transport = AIOHTTPTransport(
            url=f"{be_host()}/graphql/",
            headers={"Authorization": get_auth_token()},
            ssl=PLAYGROUND_ENV != "LOCAL",
        )
        client_ = Client(transport=transport, fetch_schema_from_transport=True)
    return client_


def list_test_suites():
    query = gql(
        f"""
        query getTestSuites {{
            testSuites {{
            description
            id
            org
            title
            created
            creator
            }}
            }}
        """
    )
    response = get_client().execute(query)

    # TODO: Error check
    return response["testSuites"]


def prompt_user_for_suite():
    suites = list_test_suites()
    click.echo("Test Suites:")
    click.echo("\n".join([f"{i}: {s['title']}" for i, s in enumerate(suites)]))

    idx = click.prompt("Enter the number of the test suite to run", type=int)
    while not 0 <= idx <= len(suites):
        idx = click.prompt("Invalid choice. Retry", type=int)
    suiteid = suites[idx]["id"]
    return suiteid
