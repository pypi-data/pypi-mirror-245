"""Cache for oauth credentials."""

from dataclasses import dataclass
import datetime
import json
import os

import requests
import typer

from launch import constants

_DEFAULT_FILE = "launchflow_google_creds.json"
_CREDS_PATH = os.path.join(constants.CONFIG_DIR, _DEFAULT_FILE)


@dataclass
class Credentials:
    access_token: str
    refresh_token: str
    email: str
    expires_at: float


class CredsCache:
    def save(self, json_creds):
        os.makedirs(constants.CONFIG_DIR, exist_ok=True)
        with open(_CREDS_PATH, "w") as f:
            json.dump(json_creds, f)

    def load(self, auth_end_point: str):
        if not os.path.exists(_CREDS_PATH):
            typer.echo("No credentials found. Please run: `launch auth login`")
            raise typer.Exit(1)
        with open(_CREDS_PATH, "r") as f:
            credentials_json = json.load(f)
            creds = Credentials(**credentials_json)

        expires_at = datetime.datetime.fromtimestamp(creds.expires_at)
        # If the creds are expiring in the next 2 minutes, refresh them.
        if expires_at - datetime.timedelta(minutes=5) > datetime.datetime.now():
            return creds
        response = requests.post(
            f"{auth_end_point}/auth/refresh?refresh_toke",
            json={"refresh_token": creds.refresh_token},
            headers={"Authorization": f"Bearer {creds.access_token}"},
        )
        if response.status_code != 200:
            if response.status_code == 401:
                typer.echo("Invalid credentials. Please re-run: `launch auth login`.")
                raise typer.Exit(1)
            else:
                typer.echo(
                    "Failed to refresh creds. Please re-run: `launch auth login`."
                )
                raise typer.Exit(1)
        json_creds = response.json()
        creds = Credentials(**json_creds)
        self.save(json_creds)
        return creds

    def logout(self):
        try:
            os.remove(_CREDS_PATH)
        except FileNotFoundError:
            pass


CREDS_CACHE = CredsCache()


def get_access_token(endpoint: str) -> str:
    creds = CREDS_CACHE.load(endpoint)
    if creds is None:
        typer.echo("Failed to load creds. Please re-run: `launch auth login`.")
        raise typer.Exit(1)
    return creds.access_token


def save_user_creds(creds):
    CREDS_CACHE.save(creds)


def logout():
    CREDS_CACHE.logout()
