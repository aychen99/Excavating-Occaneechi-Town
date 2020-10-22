from os.path import relpath
import pathlib


def rel_path(path, start):
    if path is None:  # Silly goose, there's no path!
        return None

    if start is None:  # Sillier goose, there's no starting location!
        return path

    # 'path' is an external link. Don't try it Anakin.
    if 'https:/' in str(path) or 'http:/' in str(path):
        return path

    if start.is_file():  # Want relpath from file's directory
        return pathlib.Path(relpath(path, start.parent))

    if start.is_dir():  # Already a directory
        return pathlib.Path(relpath(path, start))

    # Should be no such paths that get here, return 'path' for safety
    return path
