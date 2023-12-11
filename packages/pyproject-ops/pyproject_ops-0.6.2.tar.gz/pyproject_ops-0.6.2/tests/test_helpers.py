# -*- coding: utf-8 -*-

import pytest
from pyproject_ops.helpers import (
    extract_digit_tokens,
    identify_py_major_and_minor_version,
)


def test_extract_digit_tokens():
    assert extract_digit_tokens("^1.23.456.*") == ["1", "23", "456"]


def test_identify_py_major_and_minor_version():
    assert identify_py_major_and_minor_version("3.8") == (3, 8)
    assert identify_py_major_and_minor_version("3.8.*") == (3, 8)
    assert identify_py_major_and_minor_version("^3.8") == (3, 8)
    assert identify_py_major_and_minor_version("~3.8") == (3, 8)
    assert identify_py_major_and_minor_version(">=3.8") == (3, 8)

    with pytest.raises(ValueError):
        identify_py_major_and_minor_version("abc")
    with pytest.raises(ValueError):
        identify_py_major_and_minor_version("<3.10")
    with pytest.raises(ValueError):
        identify_py_major_and_minor_version("3")


if __name__ == "__main__":
    from pyproject_ops.tests import run_cov_test

    run_cov_test(__file__, "pyproject_ops.helpers", preview=False)
