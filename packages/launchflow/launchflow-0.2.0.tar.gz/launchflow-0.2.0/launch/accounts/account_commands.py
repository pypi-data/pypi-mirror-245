from typing import Optional

import requests
import typer
from launch import constants
from launch.auth import cache
from launch.projects import project_helper
from launch.utils import get_account_id, get_server_address, print_response
from rich.prompt import Prompt

app = typer.Typer()


UPGRADE_HELP = "Upgrade your launchflow acount."


@app.command(help=UPGRADE_HELP)
def upgrade(
    account_id: Optional[str] = constants.ACCOUNT_OPTION,
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    account_id = get_account_id(account_id)
    response = requests.post(
        f"{launchflow_server_address}/account/subscription/upgrade",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"account_id": account_id},
    )
    if response.status_code == 401 and response.json().get("detail").startswith(
        "Access to LaunchFlow Cloud"
    ):
        response = Prompt.ask(
            "Upgrading your account is currently invite only. "
            "Would you like to request access? [y/n]",
            choices=["y", "n"],
        )
        if response.lower() == "y":
            response = requests.post(
                f"{launchflow_server_address}/support/upgrade",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code != 200:
                typer.echo(
                    "Failed to request account upgrade. Please try again, and reach "
                    f"out to founders@launchflow.com if the issue persists. "
                    f"Error: {response.content}"
                )
            else:
                typer.echo(
                    "Successfully requested account upgrade. "
                    "We'll reach out to you shortly!"
                )
        else:
            typer.echo("Upgrade account flow canceled.")
        return

    if response.status_code != 200:
        typer.echo(
            "Failed to upgrade account. Please try again, and reach out to "
            f"founders@launchflow.com the issue persists. Error: {response.content}"
        )
        raise typer.Exit(1)

    json_response = response.json()
    checkout_url = json_response["checkout_link"]

    typer.echo(
        f"\nPlease visit the following link to upgrade:\n\n    {checkout_url}\n\n"
    )


EXPAND_HELP = "Show all projects and deployments in an account."
LIST_HELP = "List all accounts you have access to."


@app.command(help=LIST_HELP)
def list(
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
    expand: bool = typer.Option(False, "--expand", "-e", help=EXPAND_HELP),
    active: bool = constants.EXPAND_ACTIVE_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    response = requests.get(
        f"{launchflow_server_address}/account/list",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to list accounts: {response.content.decode()}")
        raise typer.Exit(1)

    response_json = response.json()
    if expand:
        expanded_response = []
        accounts = response_json["accounts"]
        for account in accounts:
            projects = project_helper.list_projects(
                account_id=account["id"],
                launchflow_server_address=launchflow_server_address,
                expand=expand,
                active=active,
                access_token=access_token,
            )
            account["projects"] = projects["projects"]
            expanded_response.append(account)
        response_json = {"accounts": expanded_response}

    print_response("Accounts", response_json)
