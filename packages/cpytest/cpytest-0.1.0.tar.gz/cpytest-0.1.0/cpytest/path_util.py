"""Utility module for path operations."""

from pathlib import Path
import re


def is_valid_module_name(py_module_path: str) -> bool:
    """Check if a string is a valid python module name."""
    for module in py_module_path.split("."):
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', module) is None:
            return False
    return True


def py_module_path(base: Path, path: Path) -> str:
    """Return a string representation of a Path relative to a base path.

    Examples:
        >>> py_module_path(Path("/home/user"), Path("/home/user/file.py"))
        'file'
        >>> py_module_path(Path("/home/user"), Path("/home/user/sub/file.py"))
        'sub.file'
    """
    assert isinstance(base, Path)
    assert isinstance(path, Path)
    path = relative_path(base, path)
    py_module_path = ".".join(path.parts[:-1] + (path.stem,))
    if not is_valid_module_name(py_module_path):
        raise ValueError(f"invalid module name: {py_module_path}")
    return py_module_path


def relative_path(base: Path, path: Path) -> Path:
    """Return a relative path from a base path.

    If the path is not relative to the base path:
        - if the path is absolute, return the path's name
        - if the path is relative, return the path as is
    """
    try:
        return path.relative_to(base)
    except ValueError:
        if path.is_absolute():
            return Path(path.name)
        return path
