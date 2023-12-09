import yaml
from typing import Any, Dict, Optional

import typer

from launch import constants
from launch.config import LaunchFlowConfig


def _get_help_str(endpoint: str):
    # If the endpoint starts with a vowel we want it to say:
    #    an {endpoint}
    if endpoint.lower()[0] in "aeiou":
        return f"n {endpoint}"
    else:
        return f" {endpoint}"


def get_name_arg(endpoint: str):
    return typer.Argument(
        ..., help=constants.NAME_HELP_TEXT.format(endpoint), show_default=False
    )


def get_add_reader_help(endpoint: str):
    return constants.ADD_READER_HELP_TEXT.format(_get_help_str(endpoint))


def get_remove_reader_help(endpoint: str):
    return constants.REMOVE_READER_HELP_TEXT.format(_get_help_str(endpoint))


def get_add_writer_help(endpoint: str):
    return constants.ADD_WRITER_HELP_TEXT.format(_get_help_str(endpoint))


def get_remove_writer_help(endpoint: str):
    return constants.REMOVE_WRITER_HELP_TEXT.format(_get_help_str(endpoint))


def get_help_text(endpoint: str):
    return constants.GET_HELP_TEXT.format(_get_help_str(endpoint))


def create_help_text(endpoint: str):
    return constants.CREATE_HELP_TEXT.format(_get_help_str(endpoint))


def get_account_id(account_id: Optional[int]):
    if account_id is None:
        config = LaunchFlowConfig.load()
        account_id = config.default_account_id
        if account_id is None:
            raise ValueError(
                "No account ID provided. Please either provide an account id "
                "with the `--account-id` option or set it as your default with"
                " `launch config set-default-account $ACCOUNT_ID`"
            )
        typer.echo(f"Using default account: {account_id}\n")
    return account_id


def get_project_id(project_id: Optional[int]):
    if project_id is None:
        config = LaunchFlowConfig.load()
        project_id = config.default_project_id
        if project_id is None:
            raise ValueError(
                "No project ID provided. Please either provide a project id "
                "with the `--project-id` option or set it as your default with"
                " `launch config set-default-project $ACCOUNT_ID`"
            )
        typer.echo(f"Using default project: {project_id}\n")
    return project_id


def get_server_address(server_address: Optional[str]):
    if server_address is None:
        config = LaunchFlowConfig.load()
        server_address = config.launchflow_server_address
        if server_address is None:
            server_address = constants.DEFAULT_LAUNCHFLOW_SERVER
    if server_address != constants.DEFAULT_LAUNCHFLOW_SERVER:
        print(f"\n\nUsing server address: {server_address}\n\n")
    return server_address


def print_response(header: str, response: Dict[str, Any]):
    print(header)
    print("-" * len(header))
    print(json_to_yaml(response))


def json_to_yaml(json_dict: Dict[str, Any]) -> str:
    return yaml.dump(json_dict, default_flow_style=False, sort_keys=False, indent=4)
