import click
import license
import os

from pathvalidate import sanitize_filename
from typing import Any, Optional

from ..project import Project
from ..template import ProjectTemplate


@click.command(help="Initializes new project.")
@click.option(
    "--template",
    "template_name",
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
    "--license",
    "license_name",
    type=str,
    required=False,
    default="",
    prompt="License",
    help="License of the project, if any.",
)
@click.option(
    "--author", type=str, required=False, default="", help="Name of the author."
)
@click.option(
    "--email",
    type=str,
    required=False,
    default="",
    help="E-mail address of the author.",
)
@click.option(
    "--description",
    type=str,
    required=False,
    default="",
    prompt="Description",
    help="Description of the project.",
)
@click.option(
    "--homepage-url",
    type=str,
    required=False,
    default="",
    prompt="Homepage URL",
    help="Project's homepage URL.",
)
@click.argument("project-name")
def new(
    template_name: str,
    version: Optional[str],
    license_name: Optional[str],
    author: Optional[str],
    email: Optional[str],
    description: Optional[str],
    homepage_url: Optional[str],
    project_name: str,
):
    template = ProjectTemplate.find(template_name)
    if not template:
        raise click.BadParameter(f"Unrecognized template: '{template_name}'")

    if sanitize_filename(project_name) != project_name:
        raise click.BadParameter(f"Invalid project name: '{project_name}'")

    if os.path.exists(project_name):
        raise click.BadParameter(f"File/directory '{project_name}' already exists")

    li: Optional[Any] = None
    if license_name:
        try:
            li = license.find(license_name)
        except KeyError:
            raise click.BadParameter(f"Unrecognized license: '{license_name}'")

        if not author:
            author = click.prompt("Author's name")

        if not email:
            email = click.prompt("Author's E-mail address")

    Project(root_directory=os.path.realpath(project_name)).create(
        template=template,
        version=version,
        description=description,
        homepage_url=homepage_url,
        license=li,
        author=author,
        email=email,
    )
