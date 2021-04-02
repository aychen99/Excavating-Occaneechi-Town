from os.path import relpath
import pathlib


def rel_path(path, start):
    if path is None:  # Silly goose, there's no path!
        return None

    if start is None:  # Sillier goose, there's no starting location!
        return path

    # 'path' is an external link. Don't try it Anakin.
    if 'https:/' in path.as_posix() or 'http:/' in path.as_posix():
        return path

    if start.suffix != '':  # Want relpath from file's directory
        return pathlib.Path(relpath(path, start.parent))

    if start.suffix == '':  # Already a directory
        return pathlib.Path(relpath(path, start))

    # Should be no such paths that get here, return 'path' for safety
    return path

def get_jsonpath(json_dir, json_name, use_updated_jsons):
    json_dir = pathlib.Path(json_dir)
    if use_updated_jsons and (json_dir / "updated" / json_name).exists():
        # json exists in "updated" section, use that one instead
        return json_dir / "updated" / json_name
    return json_dir / json_name
