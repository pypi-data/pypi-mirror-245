from typing import Any, Dict

import requests
import typer

from launch.deployments import deployments_helper


def list_projects(
    account_id: str,
    launchflow_server_address: str,
    expand: bool,
    active: bool,
    access_token: str,
) -> Dict[str, Any]:
    response = requests.get(
        f"{launchflow_server_address}/projects/list?account_id={account_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to list projects: {response.content.decode()}")
        raise typer.Exit(1)

    response_json = response.json()
    if expand:
        expanded_response = []
        projects = response_json["projects"]
        for project in projects:
            deployments = deployments_helper.list_deployments(
                account_id=account_id,
                launchflow_server_address=launchflow_server_address,
                access_token=access_token,
                active=active,
                projects=[project["name"]],
            )
            project["deployments"] = deployments
            expanded_response.append(project)
        response_json = {"projects": expanded_response}
    return response_json
