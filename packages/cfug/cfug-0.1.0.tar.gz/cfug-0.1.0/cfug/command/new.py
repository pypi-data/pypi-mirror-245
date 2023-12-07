import click
import os

from pathvalidate import sanitize_filename
from typing import Optional

from ..project import Project


@click.command(help="Initializes new project.")
@click.option(
    "--template",
    type=str,
    default="executable",
    help="Which project template to use. Available options are: executable, header-only and library.",
)
@click.option(
    "--version",
    type=str,
    required=False,
    default="1.0.0",
    prompt="Version",
    help="Initial version number of the project.",
)
@click.option(
    "--description",
    type=str,
    required=False,
    prompt="Description",
    help="Description of the project.",
)
@click.option(
    "--homepage-url",
    type=str,
    required=False,
    help="Project's homepage URL.",
)
@click.argument("project-name")
def new(
    template: str,
    version: Optional[str],
    description: Optional[str],
    homepage_url: Optional[str],
    project_name: str,
):
    if sanitize_filename(project_name) != project_name:
        raise click.BadParameter(f"Invalid project name: '{project_name}'")

    if os.path.exists(project_name):
        raise click.BadParameter(f"File/directory '{project_name}' already exists")

    Project(
        root_directory=os.path.realpath(project_name),
        version=version,
        description=description,
        homepage_url=homepage_url,
    ).initialize(template_name=template)
