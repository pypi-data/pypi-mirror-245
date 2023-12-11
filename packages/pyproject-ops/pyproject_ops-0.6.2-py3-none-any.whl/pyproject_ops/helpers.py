# -*- coding: utf-8 -*-

"""
Helper functions.

.. note::

    This module is "ZERO-DEPENDENCY".
"""

import typing as T
import hashlib


def sha256_of_bytes(b: bytes) -> str:  # pragma: no cover
    sha256 = hashlib.sha256()
    sha256.update(b)
    return sha256.hexdigest()


def extract_digit_tokens(text: str) -> T.List[str]:
    """
    Extract all consecutive digit tokens from a string.

    Example:

        >>> extract_digit_tokens("1.23.456")
        ["1", "23", "456"]
    """
    for c in list(text):
        if not c.isdigit():
            text = text.replace(c, " ")
    return [token.strip() for token in text.split() if token.strip()]


def identify_py_major_and_minor_version(py_ver: str) -> T.Tuple[int, int]:
    """
    Parse the desired python major and minor version from the pyproject.toml file.
    We use the ``python = x.y`` part under the ``[tool.poetry.dependencies]``
    section to determine the desired python version.

    :param py_ver: ``python = ... syntax`` in pyproject.toml file. valid example:
        ``^3.8``, ``~3.8``, ``3.8.*``, ``>=3.8,<3.12``.
    """
    if py_ver[0].isdigit():
        py_ver_info = extract_digit_tokens(py_ver)
    elif py_ver[0] in ["^", "~"]:
        py_ver_info = extract_digit_tokens(py_ver)
    elif py_ver[0] in [">", "<"]:
        parts = py_ver.split(",")
        if parts[0].startswith(">="):
            py_ver_info = extract_digit_tokens(py_ver)
        else:
            raise ValueError
    else:
        raise ValueError
    if len(py_ver_info) < 2:
        raise ValueError
    return int(py_ver_info[0]), int(py_ver_info[1])
