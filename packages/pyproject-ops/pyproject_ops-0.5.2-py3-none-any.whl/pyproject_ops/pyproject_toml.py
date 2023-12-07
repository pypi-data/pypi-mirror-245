# -*- coding: utf-8 -*-

"""
Enumeration of important paths on local file system.
"""

import typing as T
import dataclasses

try:  # pragma: no cover
    import tomllib

    has_tomllib = True
except ImportError:  # pragma: no cover
    try:
        import tomli as tomllib

        has_tomllib = True
    except ImportError:
        has_tomllib = False

from pathlib_mate import Path

from .helpers import identify_py_major_and_minor_version

if T.TYPE_CHECKING:  # pragma: no cover
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectToml:
    """
    Namespace class for accessing important paths.

    :param dir_project_root: The root directory of the project, it is usually
        the git root directory. It has to have a ``pyproject.toml`` file or
        ``setup.py`` in it.
    :param package_name: The name of the Python package you are working on.
        There has to be a folder with the same name under ``dir_project_root``,
        And it has to have a ``__init__.py`` file in it.
    """

    @classmethod
    def from_pyproject_toml(cls, path_pyproject_toml: Path) -> "PyProjectOps":
        """
        Create the PyProjectOps instance from ``pyproject.toml`` file by reading
        the package name and python version information from it.

        It also compares the package version in the ``_version.py`` file with
        the version in ``pyproject.toml`` file, if they are not match, it will
        raise an error.
        """
        if has_tomllib is False:
            raise ImportError("tomli is required to parse pyproject.toml")
        toml_dict = tomllib.loads(path_pyproject_toml.read_text())
        package_name = toml_dict["tool"]["poetry"]["name"]
        package_version = toml_dict["tool"]["poetry"]["version"]
        python_version = toml_dict["tool"]["poetry"]["dependencies"]["python"]
        major, minor = identify_py_major_and_minor_version(python_version)
        pyproject_ops: "PyProjectOps" = cls(
            dir_project_root=path_pyproject_toml.parent,
            package_name=package_name,
            python_version=f"{major}.{minor}",
        )
        if pyproject_ops.package_version != package_version:
            raise ValueError(
                f"The version in {pyproject_ops.path_version_py} is {pyproject_ops.package_version}, "
                f"and the version in {path_pyproject_toml} is {package_version}, "
                f"they has to be match!"
            )
        return pyproject_ops
