from os.path import relpath
import pathlib


def rel_path(path, start):
    if path is None:
        return None
    return pathlib.Path(relpath(path, start.parent))
