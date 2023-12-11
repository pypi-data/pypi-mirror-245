# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import fire
from pathlib_mate import Path

from ._version import __version__
from .vendor.jsonutils import json_loads
from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectOpsConfig:
    """
    ``pyproject_ops.json`` file stores the configuration for ``pyproject_ops`` CLI
    for your project.

    If you don't want to use the CLI, instead you want to use pyproject_ops
    as a Python library in your own automation script, you can create the
    :class:`PyProjectOps` object yourself.
    """

    package_name: str = dataclasses.field()
    dev_py_ver_major: int = dataclasses.field()
    dev_py_ver_minor: int = dataclasses.field()
    dev_py_ver_micro: int = dataclasses.field()
    doc_host_aws_profile: T.Optional[str] = dataclasses.field(default=None)
    doc_host_s3_bucket: T.Optional[str] = dataclasses.field(default=None)


def find_pyproject_ops_json(dir_cwd: Path) -> Path:
    """
    Try to locate the ``pyproject_ops.json`` file by searching all the way up.
    """
    if dir_cwd.parent == dir_cwd:
        raise FileNotFoundError(
            f"Cannot find 'pyproject_ops.json' in {dir_cwd} or its parent directory."
        )
    path = dir_cwd.joinpath("pyproject_ops.json")
    if path.exists():
        return path
    else:
        return find_pyproject_ops_json(dir_cwd.parent)


dir_cwd = Path.cwd()
path_pyproject_ops_json = find_pyproject_ops_json(dir_cwd)
pyops_config = PyProjectOpsConfig(
    **json_loads(path_pyproject_ops_json.read_text(encoding="utf-8"))
)
pyops = PyProjectOps(
    dir_project_root=path_pyproject_ops_json.parent,
    package_name=pyops_config.package_name,
    python_version=f"{pyops_config.dev_py_ver_major}.{pyops_config.dev_py_ver_minor}",
)


class Command:
    """
    python project ops command line interface.
    """
    def __call__(self, version: bool = False):
        if version:
            print(__version__)
        else:
            print("python project ops command line interface.")
            print("type: 'pyops -h' for help")


    def venv_create(self):
        """
        ** 🐍 Create Virtual Environment
        """
        pyops.create_virtualenv()

    def venv_remove(self):
        """
        ** 🗑 🐍 Remove Virtual Environment
        """
        pyops.remove_virtualenv()

    def install(self):
        """
        ** 💾 Install main dependencies and Package itself
        """
        pyops.pip_install()

    def install_dev(self):
        """
        💾 💻 Install Development Dependencies
        """
        pyops.pip_install_dev()

    def install_test(self):
        """
        💾 🧪 Install Test Dependencies
        """
        pyops.pip_install_test()

    def install_doc(self):
        """
        💾 📔 Install Document Dependencies
        """
        pyops.pip_install_doc()

    def install_automation(self):
        """
        💾 🤖 Install Dependencies for Automation Script
        """
        pyops.pip_install_automation()

    def install_all(self):
        """
        ** 💾 💻 🧪 📔 🤖 Install All Dependencies
        """
        pyops.pip_install_all()

    def poetry_export(self):
        """
        Export requirements-*.txt from poetry.lock file
        """
        pyops.poetry_export()

    def poetry_lock(self):
        """
        ** Resolve dependencies using poetry, update poetry.lock file
        """
        pyops.poetry_lock()

    def test(self):
        """
        ** 🧪 Run test
        """
        pyops.pip_install()
        pyops.pip_install_test()
        pyops.run_unit_test()

    def test_only(self):
        """
        🧪 Run test without checking test dependencies
        """
        pyops.run_unit_test()

    def cov(self):
        """
        ** 🧪 Run code coverage test
        """
        pyops.pip_install()
        pyops.pip_install_test()
        pyops.run_cov_test()

    def cov_only(self):
        """
        🧪 Run code coverage test without checking test dependencies
        """
        pyops.run_cov_test()

    def view_cov(self):
        """
        👀 🧪 View coverage test output html file locally in web browser.
        """
        pyops.view_cov()

    def int(self):
        """
        ** 🧪 Run integration test
        """
        pyops.pip_install()
        pyops.pip_install_test()
        pyops.run_int_test()

    def int_only(self):
        """
        🧪 Run integration test without checking test dependencies
        """
        pyops.run_int_test()

    def build_doc(self):
        """
        ** 📔 Build documentation website locally
        """
        pyops.pip_install()
        pyops.pip_install_doc()
        pyops.build_doc()

    def build_doc_only(self):
        """
        📔 Build documentation website locally without checking doc dependencies
        """
        pyops.build_doc()

    def view_doc(self):
        """
        ** 👀 📔 View documentation website locally
        """
        pyops.view_doc()

    def deploy_versioned_doc(self):
        """
        🚀 📔 Deploy Documentation Site To S3 as Versioned Doc
        """
        pyops.deploy_versioned_doc(
            bucket=pyops_config.doc_host_s3_bucket,
            aws_profile=pyops_config.doc_host_aws_profile,
        )

    def deploy_latest_doc(self):
        """
        🚀 📔 Deploy Documentation Site To S3 as Latest Doc
        """
        pyops.deploy_latest_doc(
            bucket=pyops_config.doc_host_s3_bucket,
            aws_profile=pyops_config.doc_host_aws_profile,
        )

    def view_latest_doc(self):
        """
        👀 📔 View the latest documentation website on S3
        """
        pyops.view_latest_doc(bucket=pyops_config.doc_host_s3_bucket)

    def publish(self):
        """
        📦 Publish package to PyPI
        """
        pyops.pip_install()
        pyops.pip_install_dev()
        pyops.python_build()
        pyops.twine_upload()


def main():
    fire.Fire(Command())
