"""Tests for version validation."""

import pytest

from bookgen.shared.version import VERSION, VersionMismatchError, validate_config_version


def test_validate_config_version_accepts_matching() -> None:
    validate_config_version("book.json", VERSION)


def test_validate_config_version_rejects_mismatch() -> None:
    with pytest.raises(VersionMismatchError):
        validate_config_version("book.json", "0.10")
