import click

from typing import Tuple

from ..project import Project


@click.command(help="Runs CMake configuration on the project.")
@click.argument("args", nargs=-1)
def configure(args: Tuple[str]):
    Project.find().configure(*args)
