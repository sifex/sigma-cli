import os
import pathlib

import click
from sigma.collection import SigmaCollection

from .backends import backends
from .pipelines import pipelines, pipeline_resolver
from sigma.validators import validators
from prettytable import PrettyTable
from textwrap import dedent

@click.group(name="list", help="List available targets or processing pipelines.")
def list_group():
    pass

@list_group.command(name="rules", help="List available rules.")
@click.argument(
    "rule_path",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
)
def list_rules(rule_path: str):
    table = PrettyTable()
    table.field_names = ("Title", "Status", "Level", "Description")
    sc = SigmaCollection.load_ruleset(rule_path)
    table.add_rows(list(map(
        lambda rule: [rule.to_dict().get(k, '') for k in ('title', 'status', 'level', 'description')],
        sc.rules
    )))
    table.align = "l"
    table.compact_printing = False
    click.echo(table.get_string())

@list_group.command(name="targets", help="List conversion target query languages.")
def list_targets():
    table = PrettyTable()
    table.field_names = ("Identifier", "Target Query Language", "Processing Pipeline Required")
    table.add_rows([
        (name, backend.text, "Yes" if backend.requires_pipeline else "No")
        for name, backend in backends.items()
    ])
    table.align = "l"
    click.echo(table.get_string())

@list_group.command(name="formats", help="List formats supported by specified conversion backend.")
@click.argument(
    "backend",
    type=click.Choice(backends.keys()),
)
def list_formats(backend):
    table = PrettyTable()
    table.field_names = ("Format", "Description")
    table.add_rows([
        (name, description)
        for name, description in backends[backend].formats.items()
    ])
    table.align = "l"
    click.echo(table.get_string())

@list_group.command(name="pipelines", help="List processing pipelines.")
@click.argument(
    "backend",
    required=False,
    type=click.Choice(backends.keys())
)
def list_pipelines(backend):
    table = PrettyTable()
    table.field_names = ("Identifier", "Priority", "Processing Pipeline", "Backends")
    for name, definition in pipelines.items():
        if backend is None or backend in definition.backends or len(definition.backends) == 0:
            pipeline = pipeline_resolver.resolve_pipeline(name)
            if len(definition.backends) > 0:
                backends = ", ".join(definition.backends)
            else:
                backends = "all"
            table.add_row((name, pipeline.priority, pipeline.name, backends))
    table.align = "l"
    click.echo(table.get_string())

@list_group.command(name="validators", help="List rule validators.")
def list_validators():
    table = PrettyTable(
        field_names=("Name", "Description",),
        align="l",
    )
    table.add_rows([
        (name, dedent(validator.__doc__ or "-").strip())
        for name, validator in validators.items()
    ])
    click.echo(table.get_string())