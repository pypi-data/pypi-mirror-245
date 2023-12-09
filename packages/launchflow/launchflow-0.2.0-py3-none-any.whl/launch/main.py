import typer
import uvicorn

from launch import constants
from launch.accounts import account_commands
from launch.auth import auth_commands
from launch.config import config_commands
from launch.deployments import deployment_commands
from launch.environments import environment_commands
from launch.gen import gen_commands
from launch.projects import project_commands

app = typer.Typer(add_completion=False, rich_markup_mode="rich")
app.add_typer(
    auth_commands.app, name="auth", help="Commands for authenticating with LaunchFlow"
)
app.add_typer(
    account_commands.app, name="accounts", help="Account commands for managing accounts"
)
app.add_typer(
    config_commands.app, name="config", help="Commands for managing CLI configuration"
)
app.add_typer(
    gen_commands.app,
    name="gen",
    help="Commands for generating BuildFlow and LaunchFlow files.",
)
app.add_typer(
    deployment_commands.app,
    name="deployments",
    help="Commands for managing LaunchFlow deployments",
)
app.add_typer(
    project_commands.app,
    name="projects",
    help="Commands for managing LaunchFlow projects",
)
app.add_typer(
    environment_commands.app,
    name="environments",
    help="Commands for managing LaunchFlow environments",
)

app.command(
    name="deploy",
    short_help="Submit a new deployment to a LaunchFlow Cloud project.",
    help=constants.SUBMIT_HELP_TEMPLATE.format(command="deploy"),
)(deployment_commands.submit)


def _start_launch_server(relay_server_port: int, runtime_server_port: int):
    from launch.launch_server.server import app as server_app  # noqa

    server_app.state.relay_server_port = relay_server_port
    server_app.state.runtime_server_port = runtime_server_port

    uvicorn.run(server_app, port=relay_server_port)


# @app.command(
#     name="run",
#     help="Run your BuildFlow application locally and spin up a UI for interacting with it.",  # noqa
# )
# def run(
#     buildflow_app_dir: str = typer.Option(
#         default=".", help="Path to BuildFlow app. Defaults to current directory."
#     ),
# ):
#     with open(f"{buildflow_app_dir}/buildflow.yaml", "r") as f:
#         buildflow_yaml = yaml.safe_load(f)

#     buildflow_app_name = buildflow_yaml.get("name", "unknown")
#     buildflow_app = BuildFlowApp(app_dir=buildflow_app_dir, name=buildflow_app_name)
#     manager = LaunchManager(buildflow_app)
#     # NOTE: This is a blocking call. The LaunchManager will run the BuildFlow app and
#     # block until it exits.
#     manager.run()


def main():
    app()


if __name__ == "__main__":
    main()
