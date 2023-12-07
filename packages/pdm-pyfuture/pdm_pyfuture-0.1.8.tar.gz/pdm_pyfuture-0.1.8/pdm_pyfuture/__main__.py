from __future__ import annotations

import argparse

from pdm.cli.commands.build import Command as BuildCommand
from pdm.core import Core
from pdm.project import Project


class MultiBuildCommand(BuildCommand):
    """
    Run a PDM script using tab completion
    """

    name = "multibuild"

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        """The command handler function.

        :param project: the pdm project instance
        :param options: the parsed Namespace object
        """
        pass


def plugin(core: Core) -> None:
    core.register_command(MultiBuildCommand)
