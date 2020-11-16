import shutil
import glob
import os
import pathlib


def copy_html_assets(assets_in, assets_out):
    all_dirs = [os.path.relpath(x[0], assets_in.as_posix())
                for x in os.walk(assets_in)]
    # Remove the top level directory itself
    all_dirs.pop(0)
    for dir_str in all_dirs:
        (assets_out / dir_str).mkdir(parents=True, exist_ok=True)
        stuff_to_glob = (assets_in / dir_str).as_posix() + "/*"
        for name in glob.glob(stuff_to_glob):
            filepath = pathlib.Path(name)
            if filepath.is_file():
                new_path = os.path.relpath(name, assets_in.as_posix())
                shutil.copy(name, assets_out / new_path)

    return
