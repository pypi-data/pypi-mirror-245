import click

from eulerpublisher.container.base import cli as oe_cli
from eulerpublisher.container.ai import cli as ai_cli


@click.group(
    name="container",
    help="Command for publishing container images"
)
def group():
    pass


# Unified interface for extension.
group.add_command(oe_cli.group)
group.add_command(ai_cli.group)
