import typer
from rich import print

import anylearn.cli.jupload as jupload
from anylearn.cli._utils import HostArgument
from anylearn.sdk.auth import authenticate, disauthenticate


app = typer.Typer(name="anyctl")
app.add_typer(jupload.app, name="jupload")


@app.command()
def login(host: str = HostArgument):
    if authenticate(host) is not None:
        print("[green]Login OK[/green]")
    else:
        print("[red]Login Failed[/red]")


@app.command()
def logout(host: str = HostArgument):
    disauthenticate(host)
    print("[green]Logout OK[/green]")
