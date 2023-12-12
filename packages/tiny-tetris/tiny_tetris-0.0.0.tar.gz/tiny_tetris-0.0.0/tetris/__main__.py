import click

from tetris import __version__


@click.group(no_args_is_help=False, invoke_without_command=True)
@click.version_option(None, "-v", "--version", message=__version__)
def tetris() -> None:  # pragma: no cover
    """`tetris` entry point."""
