from dataclasses import dataclass
from typing import Dict, List, Optional

import requests
import typer

from launch import constants
from launch.utils import get_project_id, print_response, get_server_address
from launch.auth import cache

app = typer.Typer()

DEPLOYMENT_KEY_WARNINGS = """\
-------------------------------------
|                                   |
|   IMPORTANT NOTICE                |
|                                   |
|   You will only be able to see    |
|   your Deployment key ONCE.       |
|                                   |
|   Please copy and save it in a    |
|   secure location.                |
|                                   |
-------------------------------------
"""


@app.command(help="List environments for a project")
def list(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    response = requests.get(
        f"{launchflow_server_address}/environments/list?project_id={project_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to list environments: {response.content.decode()}")
        raise typer.Exit(1)

    response_json = response.json()

    print_response("Environments", response_json)


@dataclass
class EnvironmentVariable:
    name: str
    value: str

    @classmethod
    def from_string(cls, string: str):
        split = string.split("=", 1)
        if len(split) != 2:
            typer.echo(
                f"Environment variables must be of the format NAME=VALUE. Got: {string}"
            )
            raise typer.Exit(1)
        return cls(split[0], split[1])


def env_var_to_dict(environment_variables: List[EnvironmentVariable]) -> Dict[str, str]:
    env_vars = {}
    for ev in environment_variables:
        if ev.name in env_vars:
            typer.echo(f"Duplicate environment variable: {ev.name}")
            raise typer.Exit(1)
        env_vars[ev.name] = ev.value
    return env_vars


@app.command(help="Create an environment in a project")
def create(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    name: str = typer.Option(
        ..., help="Name of the environment this must be unique within the project"
    ),
    environment_variables: List[EnvironmentVariable] = typer.Option(
        None,
        "--environment-variable",
        "-e",
        help=(
            "A map of environment variables to set on the environment. "
            "Should be of the format --environment-variable NAME=VALUE "
            "--environment-variable NAME2=VALUE2. NOTE: you can use -e for "
            "shorthand (e.g. -e NAME=VALUE -e NAME2=VALUE2))"
        ),
        parser=EnvironmentVariable.from_string,
    ),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    env_vars = env_var_to_dict(environment_variables)
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    response = requests.post(
        f"{launchflow_server_address}/environments/create",
        json={
            "project_id": project_id,
            "name": name,
            "environment_variables": env_vars,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to create environment: {response.content.decode()}")
        raise typer.Exit(1)

    print(DEPLOYMENT_KEY_WARNINGS)
    print_response("Environment", response.json())


@app.command(
    help="Set environment variables on an environment. "
    "This will overwrite any existing environment variables"
)
def set_env_vars(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    name: str = typer.Option(..., help="Name of the environment."),
    environment_variables: List[EnvironmentVariable] = typer.Option(
        None,
        "--environment-variable",
        "-e",
        help=(
            "A map of environment variables to set on the environment. "
            "Should be of the format --environment-variable NAME=VALUE "
            "--environment-variable NAME2=VALUE2. NOTE: you can use -e for "
            "shorthand (e.g. -e NAME=VALUE -e NAME2=VALUE2))"
        ),
        parser=EnvironmentVariable.from_string,
    ),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    env_vars = env_var_to_dict(environment_variables)
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    response = requests.post(
        f"{launchflow_server_address}/environments/update",
        json={
            "project_id": project_id,
            "name": name,
            "environment_variables": env_vars,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to set environment variables: {response.content.decode()}")
        raise typer.Exit(1)

    print_response("Environment", response.json())


@app.command(help="Update or add environment variables to an environment.")
def update_env_vars(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    name: str = typer.Option(..., help="Name of the environment."),
    environment_variables: List[EnvironmentVariable] = typer.Option(
        None,
        "--environment-variable",
        "-e",
        help=(
            "A map of environment variables to update or add to the environment. "
            "Should be of the format --environment-variable NAME=VALUE "
            "--environment-variable NAME2=VALUE2. NOTE: you can use -e for "
            "shorthand (e.g. -e NAME=VALUE -e NAME2=VALUE2))"
        ),
        parser=EnvironmentVariable.from_string,
    ),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    env_vars = env_var_to_dict(environment_variables)
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    env_response = requests.get(
        f"{launchflow_server_address}/environments/get?project_id={project_id}&name={name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if env_response.status_code != 200:
        typer.echo(f"Failed to get environment: {env_response.content.decode()}")
        raise typer.Exit(1)

    to_send_env_vars = env_response.json()["environment_variables"]
    to_send_env_vars.update(env_vars)

    response = requests.post(
        f"{launchflow_server_address}/environments/update",
        json={
            "project_id": project_id,
            "name": name,
            "environment_variables": to_send_env_vars,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(
            f"Failed to update environment variables: {response.content.decode()}"
        )
        raise typer.Exit(1)

    print_response("Environment", response.json())


@app.command(help="Clear environment variables in an environment.")
def clear_env_vars(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    name: str = typer.Option(..., help="Name of the environment."),
    environment_variable_names: List[str] = typer.Option(
        None,
        "--environment-variable-name",
        "-e",
        help=(
            "Environment variable names that should be removed from the environment."
            " Multiple can be provided with -e NAME1 -e NAME2"
        ),
    ),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    env_response = requests.get(
        f"{launchflow_server_address}/environments/get?project_id={project_id}&name={name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if env_response.status_code != 200:
        typer.echo(f"Failed to get environment: {env_response.content.decode()}")
        raise typer.Exit(1)

    to_send_env_vars = env_response.json()["environment_variables"]
    for env_name in environment_variable_names:
        if env_name not in to_send_env_vars:
            typer.echo(f"Environment variable `{env_name}` not found in environment.")
            raise typer.Exit(1)
        del to_send_env_vars[env_name]

    response = requests.post(
        f"{launchflow_server_address}/environments/update",
        json={
            "project_id": project_id,
            "name": name,
            "environment_variables": to_send_env_vars,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(
            f"Failed to clear environment variables: {response.content.decode()}"
        )
        raise typer.Exit(1)

    print_response("Environment", response.json())


@app.command(help="Delete an environment.")
def delete(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    name: str = typer.Option(
        ..., help="Name of the environment this must be unique within the project"
    ),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    response = requests.post(
        f"{launchflow_server_address}/environments/delete",
        json={
            "project_id": project_id,
            "name": name,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to delete environment: {response.content.decode()}")
        raise typer.Exit(1)

    print("Environment successfully deleted.")


@app.command(help="Update an environment.")
def update(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    name: str = typer.Option(
        ..., help="Name of the environment this must be unique within the project"
    ),
    num_cpus: Optional[int] = typer.Option(
        None,
        help="Number of CPUs to allocate to each worker in the environment. If not set this will not be updated in the environment.",  # noqa
    ),
    max_workers: Optional[int] = typer.Option(
        None,
        help="Maximum number of workers a deployment is allowed to scale up to. If not set this will not be updated in the environment.",  # noqa
    ),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    response = requests.post(
        f"{launchflow_server_address}/environments/update",
        json={
            "project_id": project_id,
            "name": name,
            "num_cpus": num_cpus,
            "max_workers": max_workers,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to set environment variables: {response.content.decode()}")
        raise typer.Exit(1)

    print_response("Environment", response.json())


@app.command(help="Regenerate a deployment key for an environment.")
def regen_deployment_key(
    project_id: Optional[str] = constants.PROJECT_OPTION,
    name: str = typer.Option(
        ..., help="Name of the environment this must be unique within the project"
    ),
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    access_token = cache.get_access_token(launchflow_server_address)
    project_id = get_project_id(project_id)
    response = requests.post(
        f"{launchflow_server_address}/environments/regen_key",
        json={
            "project_id": project_id,
            "name": name,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to set environment variables: {response.content.decode()}")
        raise typer.Exit(1)

    print(DEPLOYMENT_KEY_WARNINGS)
    print_response("Deployment Key", response.json())


if __name__ == "__main__":
    app()
