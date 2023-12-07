import os
import pygit2
import subprocess
import sys

from caseconvertor import camelcase
from pathlib import Path
from typing import Any, Optional

from .exceptions import ProjectNotConfiguredError, ProjectNotFoundError
from .template import ProjectTemplate


class Project:
    @classmethod
    def find(cls) -> "Project":
        path = Path.cwd()

        while str(path) != path.root:
            if os.path.exists(os.path.join(path, ".cfug")):
                return cls(root_directory=str(path))
            path = path.parent

        raise ProjectNotFoundError()

    def __init__(self, root_directory: str):
        self.root_directory = root_directory

    @property
    def name(self) -> str:
        name = camelcase(os.path.basename(self.root_directory))
        return f"{name[0].upper()}{name[1:]}"

    @property
    def build_directory(self) -> str:
        return os.path.join(self.root_directory, "build")

    def create(
        self,
        template: ProjectTemplate,
        version: Optional[str] = None,
        description: Optional[str] = None,
        homepage_url: Optional[str] = None,
        license: Optional[Any] = None,
        author: Optional[str] = "",
        email: Optional[str] = "",
    ):
        template.context["project"] = self
        template.context["version"] = version
        template.context["description"] = description
        template.context["homepage_url"] = homepage_url

        # Create the project directory.
        os.mkdir(self.root_directory)

        # Create empty ".cfug" marker file.
        with open(os.path.join(self.root_directory, ".cfug"), "w"):
            pass

        # Initialize git repository.
        pygit2.init_repository(self.root_directory)

        # Render license, if one was given.
        if license:
            with open(os.path.join(self.root_directory, "LICENSE"), "w") as f:
                f.write(license.render(name=author, email=email))

        # Install the template.
        template.install(self.root_directory)

        # TODO: Create initial commit like create-react-app does?

    def configure(self, *args):
        build_directory = self.build_directory
        if not os.path.isdir(build_directory):
            os.mkdir(build_directory)

        subprocess.run(
            args=["cmake", "..", *args],
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=build_directory,
        )

    def run_cmake(self, *args):
        build_directory = self.build_directory
        if not os.path.exists(os.path.join(build_directory, "Makefile")):
            raise ProjectNotConfiguredError()

        subprocess.run(
            args=["cmake", *args],
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=build_directory,
        )
