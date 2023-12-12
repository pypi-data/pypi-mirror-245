import json
import os
import sys
import time

import boto3
import click

PRL_PATH = os.path.expanduser("~/.prl")
CREDS_PATH = os.path.join(PRL_PATH, "creds.json")
PLAYGROUND_ENV = os.getenv("PLAYGROUND_ENV")


def get_client_id(in_europe: bool):
    if in_europe:
        return "4asi3qr1jga1l1kvc6cqpqdsad"
    elif PLAYGROUND_ENV in ["LOCAL", "DEV"]:
        return "59blf1klr2lejsd3uanpk3b0r4"
    else:
        # Normal Prod user pool
        return "7r5tn1kic6i262mv86g6etn3oj"


@click.command()
def login():
    """
    Authenticate with PlaygroundRL CLI
    """
    in_eu = click.confirm("Are you located in Europe?")
    region = "eu-north-1" if in_eu else "us-east-1"
    username = click.prompt("email")
    password = click.prompt("password", hide_input=True)

    client_id = get_client_id(in_eu)

    client = boto3.client("cognito-idp", region_name=region)

    # TODO: Error handling
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
        ClientId=client_id,
    )

    auth_dict = {
        "refresh_token": response["AuthenticationResult"]["RefreshToken"],
        "access_token": response["AuthenticationResult"]["AccessToken"],
        "id_token": response["AuthenticationResult"]["IdToken"],
        "client_id": client_id,
        "region": region,
        "access_expiry": int(
            time.time() + response["AuthenticationResult"]["ExpiresIn"] - 10
        ),
    }
    auth_json = json.dumps(auth_dict, indent="\t")

    if not os.path.exists(PRL_PATH):
        os.makedirs(PRL_PATH)

    with open(CREDS_PATH, "w") as f:
        f.write(auth_json)


def get_region():
    if not os.path.exists(CREDS_PATH):
        click.echo("Not authenticated. Run the command: prl login.")

    with open(CREDS_PATH, "r") as f:
        auth_dict = json.load(f)

    return auth_dict["region"]


def get_auth_token():
    if not os.path.exists(CREDS_PATH):
        click.echo("Not authenticated. Run the command: prl login.")

    with open(CREDS_PATH, "r") as f:
        auth_dict = json.load(f)

    client = boto3.client("cognito-idp", region_name=auth_dict["region"])

    if time.time() > auth_dict["access_expiry"]:
        # If enough time has elapsed, we need to refresh the token
        try:
            response = client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={"REFRESH_TOKEN": auth_dict["refresh_token"]},
                ClientId=auth_dict["client_id"],
            )
        except:
            click.echo("Your session has expired. Please run the command: prl login.")
            sys.exit()

        auth_dict = {
            **auth_dict,
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
            "access_expiry": int(
                time.time() + response["AuthenticationResult"]["ExpiresIn"] - 10
            ),
        }
        auth_json = json.dumps(auth_dict, indent="\t")
        # Store the new access token
        with open(CREDS_PATH, "w") as f:
            f.write(auth_json)

    return auth_dict["access_token"]
