from os.path import relpath
import pathlib


def rel_path(path, start):
    if path is None:
        return None
    if 'https:/' in str(path) or 'http:/' in str(path):
        return path
    return pathlib.Path(relpath(path, start.parent))
