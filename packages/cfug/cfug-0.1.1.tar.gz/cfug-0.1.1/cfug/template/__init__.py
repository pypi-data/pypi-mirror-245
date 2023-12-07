import os

from jinja2 import Template
from pathvalidate import sanitize_filename
from typing import Any, Dict, Optional


class ProjectTemplate:
    @classmethod
    def find(cls, name: str) -> Optional["ProjectTemplate"]:
        directory = os.path.realpath(
            os.path.join(os.path.realpath(__file__), "..", sanitize_filename(name))
        )

        if not os.path.isdir(directory):
            return None

        return cls(directory=directory)

    def __init__(self, directory: str):
        self.directory = directory
        self.context: Dict[str, Any] = {}

    def install(self, target_directory: str):
        self._install_traverse(
            source_directory=self.directory, target_directory=target_directory
        )

    def _install_traverse(self, source_directory: str, target_directory: str):
        for filename in os.listdir(source_directory):
            if filename.startswith("."):
                continue

            full_source_filename = os.path.join(source_directory, filename)
            if os.path.isdir(full_source_filename):
                full_target_filename = os.path.join(target_directory, filename)
                os.mkdir(full_target_filename)
                self._install_traverse(
                    source_directory=full_source_filename,
                    target_directory=full_target_filename,
                )
            else:
                self._install_file(
                    source_directory=source_directory,
                    target_directory=target_directory,
                    filename=filename,
                )

    def _install_file(
        self, source_directory: str, target_directory: str, filename: str
    ):
        source_filename = os.path.join(source_directory, filename)
        target_filename = os.path.join(
            target_directory,
            f".{filename[1:]}" if filename.startswith("_") else filename,
        )

        with open(source_filename, "r") as f:
            template = Template(f.read(), autoescape=False)

        with open(target_filename, "w") as f:
            f.write(template.render(self.context))
