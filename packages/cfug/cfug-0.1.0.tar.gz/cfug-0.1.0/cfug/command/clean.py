import click

from ..project import Project


@click.command(help="Cleans all build files.")
def clean():
    Project.find().run_cmake("--build", ".", "--target", "clean")
