from typing import Any, Dict, List

import requests
import typer


def list_deployments(
    account_id: str,
    launchflow_server_address: str,
    access_token: str,
    active: bool,
    projects: List[str] = [],
) -> Dict[str, Any]:
    response = requests.post(
        f"{launchflow_server_address}/deployments/list",
        json={"account_id": account_id, "active": active, "projects": projects},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        typer.echo(f"Failed to list deployments: {response.content.decode()}")
        raise typer.Exit(1)
    return response.json()
