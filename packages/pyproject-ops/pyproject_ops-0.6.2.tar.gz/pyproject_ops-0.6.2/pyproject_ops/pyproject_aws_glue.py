# -*- coding: utf-8 -*-

"""
AWS Glue related automation.
"""

import typing as T
import dataclasses
from pathlib_mate import Path


if T.TYPE_CHECKING:
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectAWSGlue:
    """
    Namespace class for AWS Glue related automation.
    """

    @property
    def dir_build_glue(self: "PyProjectOps") -> Path:
        """
        The AWS glue artifacts build folder.

        Example: ``${dir_project_root}/build/glue/``
        """
        return self.dir_build.joinpath("glue")

    @property
    def dir_build_glue_extra_py_files(self) -> Path:
        """
        The AWS glue extra Python files build folder.
        This folder contains the not-pip-installable python library dependencies.

        Example: ``${dir_project_root}/build/glue/extra_py_files/``
        """
        return self.dir_build_glue.joinpath("extra_py_files")

    @property
    def path_build_glue_extra_py_files_zip(self) -> Path:
        """
        The AWS glue extra Python files zip file path.

        Example: ``${dir_project_root}/build/glue/extra_py_files.zip``
        """
        return self.dir_build_glue.joinpath("extra_py_files.zip")
