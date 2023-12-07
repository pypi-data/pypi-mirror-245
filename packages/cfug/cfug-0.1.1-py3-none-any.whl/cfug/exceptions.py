import os

from click import ClickException


class CFugError(ClickException):
    """
    Base class for all CFug related exceptions.
    """


class ProjectNotFoundError(CFugError):
    """
    Exception that is thrown when user runs the `cfug` command in a directory
    that doesn't look like to be a CFug project.
    """

    def __init__(self):
        super().__init__(
            f"Could not find a '.cfug' file in '{os.path.realpath('.')}' or it's parent directories."
        )


class ProjectNotConfiguredError(CFugError):
    """
    Exception that is thrown when user attempts to run CMake commands on a
    project that hasn't been configured yet.
    """

    def __init__(self):
        super().__init__(
            "Project has not been configured yet. Please run `cfug configure` first."
        )
