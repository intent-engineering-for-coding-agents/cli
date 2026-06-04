"""iec-cli — Intent Engineering practice validation CLI."""

from importlib.metadata import version

import typer

from iec_cli.check import check_app
from iec_cli.eval import eval_app
from iec_cli.init import init

app = typer.Typer(no_args_is_help=True)
app.command(name="init")(init)
app.add_typer(check_app, name="check")
app.add_typer(eval_app, name="eval")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"iec-cli {version('iec-cli')}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    version_arg: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Validate Intent Engineering practices in your repo."""
