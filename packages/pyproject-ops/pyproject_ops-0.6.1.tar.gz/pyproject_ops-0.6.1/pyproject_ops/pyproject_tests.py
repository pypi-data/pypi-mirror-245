# -*- coding: utf-8 -*-

"""
Testing related automation.
"""

import typing as T
import subprocess
import dataclasses

from .operation_system import OPEN_COMMAND
from .vendor.emoji import Emoji

if T.TYPE_CHECKING:  # pragma: no cover
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectTests:
    """
    Namespace class for testing related automation.
    """

    def _run_unit_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run unit test.
        """
        if dry_run is True:
            return
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def run_unit_test(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._run_unit_test,
            msg="Run Unit Test",
            emoji=Emoji.test,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _run_cov_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run code coverage test.
        """
        if dry_run is True:
            return
        args = [
            f"{self.path_venv_bin_pytest}",
            "-s",
            "--tb=native",
            f"--rootdir={self.dir_project_root}",
            f"--cov={self.package_name}",
            "--cov-report",
            "term-missing",
            "--cov-report",
            f"html:{self.dir_htmlcov}",
            f"{self.dir_tests}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def run_cov_test(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._run_cov_test,
            msg="Run Code Coverage Test",
            emoji=Emoji.test,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _view_cov(self: "PyProjectOps"):
        """
        View coverage test output html file locally in web browser.

        It is usually at the ``${dir_project_root}/htmlcov/index.html``
        """
        subprocess.run([OPEN_COMMAND, f"{self.path_htmlcov_index_html}"])

    def view_cov(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._view_cov,
            msg="View Code Coverage Test Result",
            emoji=Emoji.test,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _run_int_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run integration test.
        """
        if dry_run is True:
            return
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests_int}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def run_int_test(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._run_int_test,
            msg="Run Integration Test",
            emoji=Emoji.test,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _run_load_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run load test.
        """
        if dry_run is True:
            return
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests_load}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def run_load_test(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self.run_load_test,
            msg="Run Load Test",
            emoji=Emoji.test,
            verbose=verbose,
            dry_run=dry_run,
        )
