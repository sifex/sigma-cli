import click
from sigma.rule import SigmaRule


@click.group(name="create", help="Creates rules using Sigma CLI.")
def create_group():
    pass

@create_group.command(name="rule", help="Creates a Sigma rule.")
@click.option('--title', '-t', prompt=True)
def create_rule(title):
    sigma_rule: SigmaRule = SigmaRule.from_dict({
        'title': 'Testing',
        'logsource': {
            'product': 'windows'
        },
        'detection': {
            'selection': {
                'field': 'value'
            },
            'condition': 'selection'
        }
    })
    sigma_rule.title = title
    sigma_rule.logsource = ()

    print(sigma_rule.to_dict())