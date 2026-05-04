"""ase-cli — ASE practice validation CLI."""

import typer

app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main() -> None:
    """Validate ASE practices in your repo."""
