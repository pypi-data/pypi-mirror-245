import dataclasses

import typer

from launch import constants
from launch.config.config import LaunchFlowConfig
from launch.utils import print_response

app = typer.Typer()


@app.command(
    help="Set the default account that should be used for commands that require "
    "nn account ID. If set to an empty string we will clear it from the config."
)
def set_default_account(
    account_id: str = typer.Argument(..., help="The account ID to set as default"),
    server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    if not account_id:
        account_id = None
    config = LaunchFlowConfig.load(server_address)
    config.default_account_id = account_id
    config.write()


@app.command(
    help="Set the default project that should be used for commands the require "
    "a project ID. If set to an empty string we will clear it from the config."
)
def set_default_project(
    project_id: str = typer.Argument(..., help="The proejct ID to set as default"),
    server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    if not project_id:
        project_id = None
    config = LaunchFlowConfig.load(server_address)
    config.default_project_id = project_id
    config.write()


@app.command(hidden=True)
def set_server_address(
    launchflow_server_address: str = typer.Argument(
        ..., help="The server address to use"
    ),
):
    if not launchflow_server_address:
        launchflow_server_address = None
    config = LaunchFlowConfig.load()
    config.launchflow_server_address = launchflow_server_address
    config.write()


@app.command(help="Print the current config")
def get():
    config = LaunchFlowConfig.load()
    dict_to_print = dataclasses.asdict(config)
    if not config.launchflow_server_address:
        del dict_to_print["launchflow_server_address"]
    print_response("Launchflow Config", dict_to_print)
