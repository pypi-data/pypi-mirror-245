import click

from ..project import Project


@click.command(help="Builds the project.")
def build():
    Project.find().run_cmake("--build", ".")
