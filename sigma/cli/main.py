import imp
import click

from .create import create_group
from .list import list_group
from .convert import convert
from .check import check

@click.group()
def cli():
    pass

def main():
    cli.add_command(list_group)
    cli.add_command(create_group)
    cli.add_command(convert)
    cli.add_command(check)
    cli()


if __name__ == "__main__":
    main()
