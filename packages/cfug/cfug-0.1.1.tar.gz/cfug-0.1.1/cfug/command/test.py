import click

from ..project import Project


@click.command(help="Runs test cases.")
def test():
    Project.find().run_cmake("--build", ".", "--target", "test")
