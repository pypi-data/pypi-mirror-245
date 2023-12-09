from typing import Optional

import requests
import typer

from launch import constants
from launch.utils import get_account_id, print_response, get_server_address
from launch.auth import cache
from launch.projects import project_helper

app = typer.Typer()

EXPAND_HELP = "Show all resources below projects (deployments)"


@app.command(help="List projects for an account")
def list(
    account_id: Optional[str] = constants.ACCOUNT_OPTION,
    expand: bool = typer.Option(False, "--expand", "-e", help=EXPAND_HELP),
    active: bool = constants.EXPAND_ACTIVE_OPTION,
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    account_id = get_account_id(account_id)
    response = project_helper.list_projects(
        account_id=account_id,
        launchflow_server_address=launchflow_server_address,
        access_token=access_token,
        active=active,
        expand=expand,
    )

    print_response("Projects", response)


@app.command(help="Create a project for an account")
def create(
    account_id: Optional[str] = constants.ACCOUNT_OPTION,
    display_name: str = typer.Argument(..., help="Display name of the project"),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    account_id = get_account_id(account_id)
    response = requests.post(
        f"{launchflow_server_address}/projects/create",
        json={"account_id": account_id, "display_name": display_name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to create project: {response.content.decode()}")
        raise typer.Exit(1)

    print_response("Project", response.json())


@app.command(help="Update a project")
def update(
    project_id: str = typer.Argument(..., help="The project ID to update"),
    display_name: str = typer.Option(..., help="The new display name of the project"),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    response = requests.post(
        f"{launchflow_server_address}/projects/update",
        json={"project_id": project_id, "display_name": display_name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to update project: {response.content.decode()}")
        raise typer.Exit(1)

    print_response("Project", response.json())


@app.command(help="Delete a project")
def delete(
    project_id: str = typer.Argument(..., help="The project ID to delete"),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    response = requests.post(
        f"{launchflow_server_address}/projects/delete",
        json={"project_id": project_id},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to delete project: {response.content.decode()}")
        raise typer.Exit(1)

    typer.echo(f"Project {project_id} successfully deleted")


if __name__ == "__main__":
    app()
