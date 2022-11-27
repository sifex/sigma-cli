import click

from .check import check
from .convert import convert
from .list import list_group


@click.group()
def cli():
    pass


def main():
    cli.add_command(list_group)
    cli.add_command(convert)
    cli.add_command(check)
    cli()


if __name__ == "__main__":
    main()
