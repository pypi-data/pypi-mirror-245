from enum import Enum
import typer
from typing_extensions import Annotated

from launch import constants
from launch.auth import flow as auth_flow
from launch.auth import cache
from launch.utils import get_server_address

app = typer.Typer()


class AuthProvider(Enum):
    GOOGLE = "google"
    GITHUB = "github"


@app.command(help="Authenticate with launchflow.")
def login(
    auth_provider: Annotated[
        AuthProvider,
        typer.Option(
            ...,
            help="Which provider you will authenticate with (Google or GitHub)",
            prompt="Please select an auth provider",
        ),
    ],
    launchflow_server_address: str = constants.LAUNCHFLOW_SERVER_ADDRESS_OPTION,
):
    launchflow_server_address = get_server_address(launchflow_server_address)
    auth_flow.auth_flow(auth_provider.value, launchflow_server_address)


@app.command(help="Logout from launchflow.")
def logout():
    cache.logout()
