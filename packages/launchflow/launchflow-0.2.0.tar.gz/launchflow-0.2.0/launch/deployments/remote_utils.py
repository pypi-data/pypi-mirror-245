import asyncio
from datetime import datetime
import json
import os
import time
import pytz
from typing import Optional, List

import httpx
import requests
from rich.progress import Progress
import typer
import urwid
import websockets

from launch.auth import cache
from launch.utils import print_response
from launch.deployments import console_ui

RAY_CLUSTER_ADDRESS = "http://127.0.0.1:8265"


def zipdir(path, ziph, requirements_path: str):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            full_file_path = os.path.join(root, file)
            if full_file_path == requirements_path:
                # No need to add requirements file we will do this below.
                continue
            if ".buildflow/_pulumi" in full_file_path:
                # Don't include pulumi info
                continue
            ziph.write(
                full_file_path, os.path.relpath(full_file_path, os.path.join(path, "."))
            )


def send_update_environment_request(
    server_address: str,
    project_id: str,
    environment: str,
    build_file: str,
    bearer_token: str,
    python_version: str,
    ray_version: str,
) -> str:
    files = {
        "build_file": ("working_dir.zip", open(build_file, "rb"), "application/zip")
    }
    data = {
        "project_id": project_id,
        "environment_to_update": environment,
        "ray_version": ray_version,
        "python_version": python_version,
    }
    client = httpx.Client(timeout=600)
    response = client.post(
        f"{server_address}/deployments/update-environment",
        headers={"Authorization": f"Bearer {bearer_token}"},
        files=files,
        data=data,
        timeout=600,
    )
    if response.status_code != 200:
        content = response.content.decode()
        raise ValueError(content)
    output = response.json()
    deployment_id = output["id"]
    return deployment_id


def send_promote_environment_request(
    server_address: str,
    project_id: str,
    from_environment: str,
    to_environment: str,
    bearer_token: str,
) -> str:
    data = {
        "project_id": project_id,
        "to_environment": to_environment,
        "from_environment": from_environment,
    }
    client = httpx.Client(timeout=600)
    response = client.post(
        f"{server_address}/deployments/promote-environment",
        headers={"Authorization": f"Bearer {bearer_token}"},
        data=data,
        timeout=600,
    )
    if response.status_code != 200:
        content = response.content.decode()
        raise ValueError(content)
    output = response.json()
    deployment_id = output["id"]
    return deployment_id


def send_update_deployment_request(
    server_address: str,
    build_file: str,
    bearer_token: str,
    python_version: str,
    ray_version: str,
    deployment_to_update: str,
    num_cpus: Optional[int] = None,
    machine_type: Optional[str] = None,
    max_workers: Optional[int] = None,
) -> str:
    files = {
        "build_file": ("working_dir.zip", open(build_file, "rb"), "application/zip")
    }
    data = {
        "num_cpus": num_cpus,
        "machine_type": machine_type,
        "max_workers": max_workers,
        "ray_version": ray_version,
        "python_version": python_version,
        "deployment_id_to_update": deployment_to_update,
    }
    client = httpx.Client(timeout=600)
    response = client.post(
        f"{server_address}/deployments/update-deployment",
        headers={"Authorization": f"Bearer {bearer_token}"},
        files=files,
        data=data,
        timeout=600,
    )
    if response.status_code != 200:
        content = response.content.decode()
        raise ValueError(content)
    output = response.json()
    deployment_id = output["id"]
    return deployment_id


def send_deploy_request(
    server_address: str,
    build_file: str,
    project_id: str,
    environment: Optional[str],
    bearer_token: str,
    python_version: str,
    ray_version: str,
    num_cpus: Optional[int] = None,
    machine_type: Optional[str] = None,
    max_workers: Optional[int] = None,
) -> str:
    files = {
        "build_file": ("working_dir.zip", open(build_file, "rb"), "application/zip")
    }
    data = {
        "num_cpus": num_cpus,
        "machine_type": machine_type,
        "max_workers": max_workers,
        "project_id": project_id,
        "environment": environment,
        "ray_version": ray_version,
        "python_version": python_version,
    }
    client = httpx.Client(timeout=600)
    response = client.post(
        f"{server_address}/deployments/create",
        headers={"Authorization": f"Bearer {bearer_token}"},
        files=files,
        data=data,
        timeout=600,
    )
    if response.status_code != 200:
        content = response.content.decode()
        raise ValueError(content)
    output = response.json()
    deployment_id = output["id"]
    return deployment_id


async def stream_deployment_info(
    deployment_id: str,
    launchflow_server_address: str,
    bearer_token: Optional[str],
    extension_server_address: str,
):
    if bearer_token is None:
        bearer_token = cache.get_access_token(launchflow_server_address)

    ws_endpoint = launchflow_server_address.replace("http://", "ws://").replace(
        "https://", "wss://"
    )
    if ws_endpoint.endswith("/"):
        ws_endpoint = ws_endpoint[:-1]
    try:
        async for ws in websockets.connect(
            f"{ws_endpoint}/deployments/info?deployment_id={deployment_id}",  # noqa
            open_timeout=1,
            extra_headers={"Authorization": f"Bearer {bearer_token}"},
        ):
            while True:
                data = await ws.recv()
                deployment_info = json.loads(data)
                deployment_info["runtime"] = "REMOTE"
                requests.post(extension_server_address, json=deployment_info)
    except Exception as e:
        typer.echo(str(e))
        raise typer.Exit(1)


async def stream_deployment_logs(
    deployment_id: str,
    launchflow_server_address: str,
    bearer_token: Optional[str],
    extension_server_address: str,
):
    if bearer_token is None:
        bearer_token = cache.get_access_token(launchflow_server_address)

    ws_endpoint = launchflow_server_address.replace("http://", "ws://").replace(
        "https://", "wss://"
    )
    if ws_endpoint.endswith("/"):
        ws_endpoint = ws_endpoint[:-1]
    try:
        async for ws in websockets.connect(
            f"{ws_endpoint}/deployments/tail_logs?deployment_id={deployment_id}",  # noqa
            open_timeout=1,
            extra_headers={"Authorization": f"Bearer {bearer_token}"},
        ):
            while True:
                data = await ws.recv()
                print(data)
                # requests.post(extension_server_address, json=data)
    except Exception as e:
        typer.echo(str(e))
        raise typer.Exit(1)


def _stop_deployment(
    deployment_id: str, server_address: str, bearer_token: Optional[str] = None
):
    if not bearer_token:
        bearer_token = cache.get_access_token(server_address)
    response = requests.post(
        f"{server_address}/deployments/stop",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json={"deployment_id": deployment_id},
    )
    return response


def stop_deployment_cli(
    deployment_id: str, server_address: str, bearer_token: Optional[str] = None
):
    response = _stop_deployment(deployment_id, server_address, bearer_token)
    if response.status_code != 200:
        print(f"Failed to stop deployment error: {response.content.decode()}")
        return
    print("Deployment is now stopping.")


def stop_deployment_urwid(deployment_id: str, server_address: str, button):
    response = _stop_deployment(deployment_id, server_address)
    if response.status_code != 200:
        try:
            json_error = response.json()
            console_ui.status_message_widget.set_text(json_error["detail"])
        except json.JSONDecodeError:
            console_ui.status_message_widget.set_text(
                f"Stop failed: {response.content}"
            )


def _drain_deployment(
    deployment_id: str, server_address: str, bearer_token: Optional[str] = None
):
    if not bearer_token:
        bearer_token = cache.get_access_token(server_address)
    response = requests.post(
        f"{server_address}/deployments/drain",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json={"deployment_id": deployment_id},
    )
    return response


def drain_deployment_cli(
    deployment_id: str, server_address: str, bearer_token: Optional[str] = None
):
    response = _drain_deployment(deployment_id, server_address, bearer_token)
    if response.status_code != 200:
        print(f"Failed to drain deployment error: {response.content.decode()}")
        return
    print("Deployment is now draining.")


def drain_deployment_urwid(deployment_id: str, server_address: str, button):
    response = _drain_deployment(deployment_id, server_address)
    if response.status_code != 200:
        try:
            json_error = response.json()
            console_ui.status_message_widget.set_text(json_error["detail"])
        except json.JSONDecodeError:
            console_ui.status_message_widget.set_text(
                f"Drain failed: {response.content}"
            )


async def run_console_ui(deployment_id: int, server_address: str):
    aloop = asyncio.get_event_loop()
    import nest_asyncio

    nest_asyncio.apply(aloop)
    ev_loop = urwid.AsyncioEventLoop(loop=aloop)
    loop = urwid.MainLoop(
        console_ui.get_main_frame(deployment_id),
        palette=console_ui.PALETTE,
        event_loop=ev_loop,
    )

    update_deployment_fd = loop.watch_pipe(console_ui.update_deployment_info)
    aloop.create_task(
        console_ui.get_deployment_info(
            update_deployment_fd, deployment_id, server_address
        )
    )
    aloop.create_task(console_ui.get_logs(deployment_id, server_address))

    urwid.connect_signal(
        obj=console_ui.drain_button,
        name="click",
        callback=drain_deployment_urwid,
        user_args=[deployment_id, server_address],
    )
    urwid.connect_signal(
        obj=console_ui.stop_button,
        name="click",
        callback=stop_deployment_urwid,
        user_args=[deployment_id, server_address],
    )

    loop.run()


def get_logs(
    deployment_id: str,
    server_address: str,
    start_timestamp: Optional[datetime],
    end_timestamp: Optional[datetime],
    page_token: Optional[str],
    bearer_token: str,
):
    if not bearer_token:
        bearer_token = cache.get_access_token(server_address)
    json_request = {
        "deployment_id": deployment_id,
    }
    if start_timestamp is not None:
        start_timestamp = start_timestamp.astimezone()
        json_request["start_timestamp"] = start_timestamp.isoformat()
    if end_timestamp is not None:
        end_timestamp = end_timestamp.astimezone()
        json_request["end_timestamp"] = end_timestamp.isoformat()
    if page_token is not None:
        json_request["page_token"] = page_token
    response = requests.post(
        f"{server_address}/deployments/get_logs",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json=json_request,
    )
    if response.status_code != 200:
        typer.echo(f"Failed to get logs: {response.content.decode()}")
        raise typer.Exit(1)
    json_response = response.json()

    for log_entry in reversed(json_response["logs"]):
        entry = log_entry["entry"]
        timestamp = datetime.fromtimestamp(
            log_entry["unix_timestamp_secs"], tz=pytz.UTC
        )
        print(f"\033[92m[{timestamp.astimezone()}]\033[0m {entry}")

    if (
        "next_page_token" in json_response
        and json_response["next_page_token"] is not None
    ):
        next_page_command = (
            f"launch deployments logs {deployment_id} "
            f"--page-token={json_response['next_page_token']}"
        )
        print(
            "\n\nReached max logs per page. "
            f"To continue reading run:\n\n{next_page_command}",
        )


def ping_deployment_info(
    deployment_ids: List[str], server_address: int, bearer_token: str
):
    if not bearer_token:
        bearer_token = cache.get_access_token(server_address)
    ping_requests = [{"deployment_id": id_} for id_ in deployment_ids]

    response = requests.post(
        f"{server_address}/deployments/ping_batch",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json={"requests": ping_requests},
    )
    print_response("Deployments", response.json())


def poll_deployment_info(
    deployment_id: str,
    server_address: int,
    bearer_token: str,
    progress: Progress,
):
    if not bearer_token:
        bearer_token = cache.get_access_token(server_address)
    request = {"deployment_id": deployment_id}
    status = "DEPLOYING"
    details = ""
    deploy_task = progress.add_task(f"[cyan]{status.capitalize()}...", total=None)
    while status in ["DEPLOYING", "PENDING"]:
        time.sleep(15)
        response = requests.post(
            f"{server_address}/deployments/ping",
            headers={"Authorization": f"Bearer {bearer_token}"},
            json=request,
        )
        if response.status_code != 200:
            continue
        response_json = response.json()
        new_status: str = response_json.get("deployment_status")
        new_details: str = response_json.get("deployment_details")
        if new_status != status or new_details != details:
            new_task = progress.add_task(
                description=f"[cyan]{new_status.capitalize()}...\n  {new_details}",
                total=None,
                start=False,
            )
            progress.advance(deploy_task)
            progress.remove_task(deploy_task)
            deploy_task = new_task
            progress.start_task(deploy_task)
            status = new_status
            details = new_details
    progress.advance(deploy_task)
    progress.remove_task(deploy_task)
    if status == "RUNNING":
        progress.console.print("[green]✓[/green] Deployment running")
    else:
        progress.console.print(f"[red]✗[/red] Deployment failed: {details}")
        raise typer.Exit(1)
