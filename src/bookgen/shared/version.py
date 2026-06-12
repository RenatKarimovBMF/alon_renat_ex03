"""Single source of truth for the project version (Guidelines V3, section 8).

The code version lives here; every versioned config file
(``setup.json``, ``book.json``, ``rate_limits.json``) must declare the same
value and is validated against it at load time.
"""

from __future__ import annotations

VERSION = "1.00"


class VersionMismatchError(RuntimeError):
    """Raised when a config file's version does not match the code version."""


def validate_config_version(name: str, version: str, *, expected: str = VERSION) -> None:
    """Fail fast when a config declares a version other than the code version."""
    if version != expected:
        raise VersionMismatchError(
            f"{name} declares version {version!r} but code version is {expected!r}; "
            "align the config 'version' field with shared/version.py."
        )
