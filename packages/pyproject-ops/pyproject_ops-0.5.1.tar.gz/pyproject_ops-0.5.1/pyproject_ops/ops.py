# -*- coding: utf-8 -*-

"""
The namespace for all the pyproject_ops automation methods.
"""

import dataclasses

from .pyproject_paths import PyProjectPaths
from .pyproject_logger import PyProjectLogger
from .pyproject_venv import PyProjectVenv
from .pyproject_toml import PyProjectToml
from .pyproject_deps import PyProjectDeps
from .pyproject_tests import PyProjectTests
from .pyproject_docs import PyProjectDocs
from .pyproject_build import PyProjectBuild
from .pyproject_publish import PyProjectPublish
from .pyproject_config_management import PyProjectConfigManagement
from .pyproject_aws import PyProjectAWS
from .pyproject_aws_lambda import PyProjectAWSLambda
from .pyproject_aws_glue import PyProjectAWSGlue


@dataclasses.dataclass
class PyProjectOps(
    PyProjectPaths,
    PyProjectLogger,
    PyProjectVenv,
    PyProjectToml,
    PyProjectDeps,
    PyProjectTests,
    PyProjectDocs,
    PyProjectBuild,
    PyProjectPublish,
    PyProjectConfigManagement,
    PyProjectAWS,
    PyProjectAWSLambda,
    PyProjectAWSGlue,
):
    """
    The namespace for all the pyproject_ops automation methods.

    :param dir_project_root: The root directory of the project, it is usually
        the git root directory. It has to have a ``pyproject.toml`` file or
        ``setup.py`` in it.
    :param package_name: The name of the Python package you are working on.
        There has to be a folder with the same name under ``dir_project_root``,
        And it has to have a ``__init__.py`` file in it.
    :param python_version: example "3.7", "3.8", ...
    """
    def __post_init__(self):
        self._validate_paths()
        self._validate_python_version()
