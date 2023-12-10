# PyInstaller entry points for setuptools
# https://pyinstaller.readthedocs.io/en/stable/hooks.html

# When a module is detected by PyInstaller, it will search
# for corresponding hooks and tests in this directory.

from pathlib import Path

import itaxotools


def get_namespace_dirs():
    paths = [Path(path) for path in itaxotools.__path__]
    return [str(path / "__pyinstaller") for path in paths]


def get_hook_dirs():
    return get_namespace_dirs()


def get_PyInstaller_tests():
    return get_namespace_dirs()
