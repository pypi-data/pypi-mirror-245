# -*- coding: utf-8 -*-

"""
Build related automation.
"""

import typing as T
import shutil
import dataclasses

from .vendor.emoji import Emoji
from .vendor.build_dist import (
    build_dist_with_python_build,
    build_dist_with_poetry_build,
)

if T.TYPE_CHECKING:
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectBuild:
    """
    Namespace class for build related automation.
    """

    def _python_build(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Build python source distribution using
        `pypa-build <https://pypa-build.readthedocs.io/en/latest/>`_.
        """
        if dry_run is True:
            return
        if self.dir_dist.exists():
            shutil.rmtree(self.dir_dist, ignore_errors=True)
        build_dist_with_python_build(
            dir_project_root=self.dir_project_root,
            path_bin_python=self.path_venv_bin_python,
            verbose=True,
        )

    def python_build(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._python_build,
            msg="Build python distribution using pypa-build",
            emoji=Emoji.build,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _poetry_build(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Build python source distribution using

        `poetry build <https://python-poetry.org/docs/cli/#build>`_.
        """
        if dry_run is True:
            return
        if self.dir_dist.exists():
            shutil.rmtree(self.dir_dist, ignore_errors=True)
        build_dist_with_poetry_build(
            dir_project_root=self.dir_project_root,
            path_bin_poetry=self.path_bin_poetry,
            verbose=True,
        )

    def poetry_build(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._poetry_build,
            msg="Build python distribution using poetry",
            emoji=Emoji.build,
            verbose=verbose,
            dry_run=dry_run,
        )
