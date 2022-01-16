"""
Provide implementation of command-line interface's entrypoint.
"""
import click

from project_version.commands import check


@click.group()
@click.version_option()
@click.help_option()
def cli() -> None:
    """
    Project version command-line interface.
    """
    pass


cli.add_command(check)

if __name__ == '__main__':
    cli()
