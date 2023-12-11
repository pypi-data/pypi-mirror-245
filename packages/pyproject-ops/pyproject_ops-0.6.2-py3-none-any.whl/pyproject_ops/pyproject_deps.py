# -*- coding: utf-8 -*-

"""
This module automates dependencies management.

We use `Python poetry <https://python-poetry.org/>`_ to ensure determinative dependencies.
"""

import typing as T
import json
import subprocess
import dataclasses
from pathlib_mate import Path

from .helpers import sha256_of_bytes
from .logger import logger
from .vendor.emoji import Emoji

if T.TYPE_CHECKING:
    from .ops import PyProjectOps


def _quite_pip_install(args: T.List[str]):
    """
    Add a cli argument to disable output for ``pip install`` command.

    We only need to disable ``pip install`` output in CI, because we don't
    want to see long list of installation messages in CI.
    """
    args.append("--disable-pip-version-check")
    args.append("--quiet")


@dataclasses.dataclass
class PyProjectDeps:
    """
    Namespace class for dependencies management related automation.
    """

    def _poetry_lock(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            poetry lock

        This command will resolve the dependencies defined in the ``pyproject.toml``
        file, and write the resolved versions to the ``poetry.lock`` file.
        You have to run this everytime you changed the ``pyproject.toml`` file.
        And you should commit the latest ``poetry.lock`` file to git.

        Ref:

        - poetry lock: https://python-poetry.org/docs/cli/#lock
        """
        if dry_run is True:
            return
        with self.dir_project_root.temp_cwd():
            args = [f"{self.path_bin_poetry}", "lock"]
            subprocess.run(args, check=True)

    def poetry_lock(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._poetry_lock,
            msg="Resolve Dependencies Tree",
            emoji=Emoji.install,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _poetry_install(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            poetry install

        Ref:

        - poetry install: https://python-poetry.org/docs/cli/#install
        """
        if dry_run is True:
            return
        with self.dir_project_root.temp_cwd():
            args = [f"{self.path_bin_poetry}", "install"]
            subprocess.run(args, check=True)

    def poetry_install(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._poetry_install,
            msg="Install main dependencies and Package itself",
            emoji=Emoji.install,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _poetry_install_dev(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            poetry install --with dev

        Ref:

        - poetry install: https://python-poetry.org/docs/cli/#install
        """
        if dry_run is True:
            return
        with self.dir_project_root.temp_cwd():
            subprocess.run(
                [f"{self.path_bin_poetry}", "install", "--with", "dev"], check=True
            )

    def poetry_install_dev(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._poetry_install_dev,
            msg="Install dev dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _poetry_install_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            poetry install --with test

        Ref:

        - poetry install: https://python-poetry.org/docs/cli/#install
        """
        if dry_run is True:
            return
        with self.dir_project_root.temp_cwd():
            subprocess.run(
                [f"{self.path_bin_poetry}", "install", "--with", "test"], check=True
            )

    def poetry_install_test(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._poetry_install_test,
            msg="Install test dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _poetry_install_doc(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            poetry install --with doc

        Ref:

        - poetry install: https://python-poetry.org/docs/cli/#install
        """
        if dry_run is True:
            return
        with self.dir_project_root.temp_cwd():
            subprocess.run(
                [f"{self.path_bin_poetry}", "install", "--with", "doc"], check=True
            )

    def poetry_install_doc(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._poetry_install_doc,
            msg="Install doc dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _poetry_install_all(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            pip install -r requirements-automation.txt
            poetry install
            poetry install --with dev,test,doc

        Ref:

        - poetry install: https://python-poetry.org/docs/cli/#install
        """
        if dry_run is True:
            return
        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            "-r",
            f"{self.path_requirements_automation}",
        ]
        _quite_pip_install(args)
        subprocess.run(args, check=True)
        subprocess.run([f"{self.path_bin_poetry}", "install"], check=True)
        subprocess.run(
            [f"{self.path_bin_poetry}", "install", "--with", "dev,test,doc"], check=True
        )

    def poetry_install_all(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._poetry_install_all,
            msg="Install all dependencies for dev, test, doc",
            emoji=Emoji.install,
            verbose=verbose,
            dry_run=dry_run,
        )

    def _do_we_need_poetry_export(
        self: "PyProjectOps",
        current_poetry_lock_hash: str,
    ) -> bool:
        """
        ``poetry export`` is an expensive command. We would like to use cache
        mechanism to avoid unnecessary export.

        Everytime we run :meth:`PyProjectDeps._poetry_export`, at the end, it will write the
        sha256 hash of the ``poetry.lock`` to the ``poetry-lock-hash.json`` cache file.
        It locates at the repo root directory. This function will compare the
        sha256 hash of the current ``poetry.lock`` to the value stored in the cache file.
        If they don't match, it means that the ``poetry.lock`` has been changed,
        so we should run :meth:`PyProjectDeps._poetry_export` again.

        The content of ``.poetry-lock-hash.json`` looks like::

            {
                "hash": "sha256-hash-of-the-poetry.lock-file",
                "description": "DON'T edit this file manually!"
            }

        Ref:

        - poetry export: https://python-poetry.org/docs/cli/#export

        :param current_poetry_lock_hash: the sha256 hash of the current ``poetry.lock`` file
        """
        if self.path_poetry_lock_hash_json.exists():
            # read the previous poetry lock hash from cache file
            cached_poetry_lock_hash = json.loads(
                self.path_poetry_lock_hash_json.read_text()
            )["hash"]
            return current_poetry_lock_hash != cached_poetry_lock_hash
        else:
            # do poetry export if the cache file not found
            return True

    def _poetry_export_main(
        self: "PyProjectOps",
        with_hash: bool = True,
    ):
        """
        Export main dependencies to the requirements.txt file.

        :param with_hash: whether to include the hash of the dependencies in the
            requirements.txt file.
        """
        self.path_requirements.remove_if_exists()
        args = [
            f"{self.path_bin_poetry}",
            "export",
            "--format",
            "requirements.txt",
            "--output",
            f"{self.path_requirements}",
        ]
        if with_hash is False:
            args.append("--without-hashes")
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def _poetry_export_group(
        self: "PyProjectOps",
        group: str,
        path: Path,
        with_hash: bool = True,
    ):
        """
        Export dependency group to given file.

        :param group: dependency group name, for example dev dependencies are defined
            in the ``[tool.poetry.group.dev]`` and ``[tool.poetry.group.dev.dependencies]``
            sections of he ``pyproject.toml`` file.
        :param path: the path to the exported ``requirements.txt`` file.
        :param with_hash: whether to include the hash of the dependencies in the
            requirements.txt file.
        """
        path.remove_if_exists()
        with self.dir_project_root.temp_cwd():
            args = [
                f"{self.path_bin_poetry}",
                "export",
                "--format",
                "requirements.txt",
                "--output",
                f"{path}",
                "--only",
            ]
            if with_hash is False:
                args.append("--without-hashes")
            args.append(group)
            subprocess.run(args, check=True)

    def _poetry_export_logic(
        self: "PyProjectOps",
        current_poetry_lock_hash: str,
        with_hash: bool = True,
    ):
        """
        Run ``poetry export --format requirements.txt ...`` command and write
        the sha256 hash of the current ``poetry.lock`` file to the cache file.

        :param current_poetry_lock_hash: the sha256 hash of the current ``poetry.lock`` file
        :param with_hash: whether to include the hash of the dependencies in the
            requirements.txt file.
        """
        # export the main dependencies
        self._poetry_export_main(with_hash=with_hash)

        # export dev, test, doc, auto dependencies
        for group, path in [
            ("dev", self.path_requirements_dev),
            ("test", self.path_requirements_test),
            ("doc", self.path_requirements_doc),
            ("auto", self.path_requirements_automation),
        ]:
            self._poetry_export_group(group, path, with_hash=with_hash)

        # write the ``poetry.lock`` hash to the cache file
        self.path_poetry_lock_hash_json.write_text(
            json.dumps(
                {
                    "hash": current_poetry_lock_hash,
                    "description": (
                        "DON'T edit this file manually! This file is the cache of "
                        "the poetry.lock file hash. It is used to avoid unnecessary "
                        "expansive 'poetry export ...' command."
                    ),
                },
                indent=4,
            )
        )

    def _poetry_export(
        self: "PyProjectOps",
        dry_run: bool = False,
    ) -> bool:
        """
        :return: ``True`` if ``poetry export`` is executed, ``False`` if not.
        """
        if dry_run is True:
            return False
        poetry_lock_hash = sha256_of_bytes(self.path_poetry_lock.read_bytes())
        if self._do_we_need_poetry_export(poetry_lock_hash):
            self._poetry_export_logic(poetry_lock_hash)
            return True
        else:
            return False

    def poetry_export(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover

        if verbose:

            @logger.start_and_end(
                msg="Install all dependencies for dev, test, doc",
                start_emoji=Emoji.install,
                error_emoji=f"{Emoji.failed} {Emoji.install}",
                end_emoji=f"{Emoji.succeeded} {Emoji.install}",
                pipe=Emoji.install,
            )
            def func():
                flag = self._poetry_export(dry_run=dry_run)
                if flag is False:
                    logger.info("already did, do nothing")
                return flag

            return func()
        else:
            return self._poetry_export(dry_run=dry_run)

    def _try_poetry_export(self: "PyProjectOps"):
        """
        This is a silent version of :func:`poetry_export`. It is called before
        running ``pip install -r requirements-***.txt`` command. It ensures that
        those exported ``requirements-***.txt`` file exists.
        """
        if self.path_poetry_lock.exists() is False:
            return

        poetry_lock_hash = sha256_of_bytes(self.path_poetry_lock.read_bytes())
        if self._do_we_need_poetry_export(poetry_lock_hash):
            self._poetry_export_logic(poetry_lock_hash)

    def _run_pip_install(self, args: T.List[str], quiet: bool):
        if quiet:
            _quite_pip_install(args)
        subprocess.run(args, check=True)

    def _pip_install(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            pip install -e . --no-deps

        Ref:

        - pip install: https://pip.pypa.io/en/stable/cli/pip_install/#options
        """
        if dry_run is True:
            return

        self._try_poetry_export()

        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            "-e",
            f"{self.dir_project_root}",
            "--no-deps",
        ]
        self._run_pip_install(args, quiet)

        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            "-r",
            f"{self.path_requirements}",
        ]
        self._run_pip_install(args, quiet)

    def pip_install(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._pip_install,
            msg="Install main dependencies and Package itself",
            emoji=Emoji.install,
            verbose=verbose,
            quiet=quiet,
            dry_run=dry_run,
        )

    def _pip_install_dev(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            pip install -r requirements-dev.txt
        """
        if dry_run is True:
            return

        self._try_poetry_export()

        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            "-r",
            f"{self.path_requirements_dev}",
        ]
        self._run_pip_install(args, quiet)

    def pip_install_dev(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._pip_install_dev,
            msg="Install dev dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            quiet=quiet,
            dry_run=dry_run,
        )

    def _pip_install_test(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            pip install -r requirements-test.txt
        """
        if dry_run is True:
            return

        self._try_poetry_export()

        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            "-r",
            f"{self.path_requirements_test}",
        ]
        self._run_pip_install(args, quiet)

    def pip_install_test(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._pip_install_test,
            msg="Install test dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            quiet=quiet,
            dry_run=dry_run,
        )

    def _pip_install_doc(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            pip install -r requirements-doc.txt
        """
        if dry_run is True:
            return

        self._try_poetry_export()

        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            "-r",
            f"{self.path_requirements_doc}",
        ]
        self._run_pip_install(args, quiet)

    def pip_install_doc(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._pip_install_doc,
            msg="Install doc dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            quiet=quiet,
            dry_run=dry_run,
        )

    def _pip_install_automation(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            pip install -r requirements-automation.txt
        """
        if dry_run is True:
            return

        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            "-r",
            f"{self.path_requirements_automation}",
        ]
        self._run_pip_install(args, quiet)

    def pip_install_automation(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._pip_install_automation,
            msg="Install automation dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            quiet=quiet,
            dry_run=dry_run,
        )

    def _pip_install_all(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
    ):
        """
        Run:

        .. code-block:: bash

            pip install -r requirements-main.txt
            pip install -r requirements-dev.txt
            pip install -r requirements-test.txt
            pip install -r requirements-doc.txt
            pip install -r requirements-automation.txt
        """
        if dry_run is True:
            return

        self._try_poetry_export()

        subprocess.run(
            [
                f"{self.path_venv_bin_pip}",
                "install",
                "-e",
                f"{self.dir_project_root}",
                "--no-deps",
            ],
            check=True,
        )

        for path in [
            self.path_requirements,
            self.path_requirements_dev,
            self.path_requirements_test,
            self.path_requirements_doc,
            self.path_requirements_automation,
        ]:
            args = [f"{self.path_venv_bin_pip}", "install", "-r", f"{path}"]
            self._run_pip_install(args, quiet)

    def pip_install_all(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._pip_install_all,
            msg="Install all dependencies",
            emoji=Emoji.install,
            verbose=verbose,
            quiet=quiet,
            dry_run=dry_run,
        )

    def _pip_install_awsglue(
        self: "PyProjectOps",
        glue_version: str = "4.0",
        quiet: bool = False,
        dry_run: bool = False,
    ):
        """
        Pip install the awsglue Python library.

        Reference:

        - aws-glue-libs: https://github.com/awslabs/aws-glue-libs
        - VCS Support - Git: https://pip.pypa.io/en/stable/topics/vcs-support/#git
        """
        if dry_run is True:
            return

        glue_version_to_git_tag_mapper = {
            "4.0": "v4.0",
            "3.0": "v3.0",
            "2.0": "v1.0-and-v2.0",
            "1.0": "v1.0-and-v2.0",
        }
        git_tag = glue_version_to_git_tag_mapper[glue_version]
        args = [
            f"{self.path_venv_bin_pip}",
            "install",
            f"git+https://github.com/awslabs/aws-glue-libs.git@{git_tag}",
        ]
        self._run_pip_install(args, quiet)

    def pip_install_awsglue(
        self: "PyProjectOps",
        quiet: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        return self._with_logger(
            method=self._pip_install_awsglue,
            msg="Install awsglue library",
            emoji=Emoji.install,
            verbose=verbose,
            quiet=quiet,
            dry_run=dry_run,
        )
