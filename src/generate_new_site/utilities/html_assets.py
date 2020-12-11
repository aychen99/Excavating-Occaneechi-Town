import shutil
import glob
import os
import pathlib
import json


def copy_html_assets(assets_in, assets_out, index, dig_dir, copy_files=True, register=False):
    # TODO: Fix a bug so that it can copy files in the root, rather than only in subdirectories
    all_dirs = [os.path.relpath(x[0], assets_in.as_posix())
                for x in os.walk(assets_in)]
    # Remove the top level directory itself
    all_dirs.pop(0)
    for dir_str in all_dirs:
        (assets_out / dir_str).mkdir(parents=True, exist_ok=True)
        stuff_to_glob = (assets_in / dir_str).as_posix() + "/*"
        for name in glob.glob(stuff_to_glob):
            filepath = pathlib.Path(name)
            if filepath.name == '.DS_Store':
                continue
            if filepath.is_file():
                if '/assets/js/excavation.js' in filepath.as_posix():
                    # Minimize the very large JSON contained in the JS
                    exc_js = filepath.open('r').read()
                    exc_js = exc_js.replace("const excavation = ", "")
                    new_js = json.loads(exc_js)
                    new_js = "const excavation = " + json.dumps(new_js, separators=(",", ":"))
                    new_path = os.path.relpath(name, assets_in.as_posix())
                    with open(pathlib.Path(assets_out / new_path), 'w') as f:
                        f.write(new_js)
                    unmin_js_path = os.path.relpath(name, assets_in.as_posix())
                    unmin_js_path = (
                        (assets_out / unmin_js_path).parent
                        / "excavation_unmin.js"
                    )
                    shutil.copy(name, unmin_js_path)
                else:
                    new_path = os.path.relpath(name, assets_in.as_posix())
                    if copy_files:
                        shutil.copy(name, assets_out / new_path)
                    if register:
                        old_path = pathlib.Path('/') / os.path.relpath(filepath, dig_dir)
                        new_path_to_register = assets_out / new_path
                        index.pathtable.register(old_path.as_posix(), new_path_to_register)

    return


def copy_videos(videos_in, videos_out, index, dig_dir, copy_files=True):
    if not videos_out.is_dir():
        videos_out.mkdir(parents=True, exist_ok=True)
    for filepath in videos_in.iterdir():
        if (copy_files):
            shutil.copy(filepath, videos_out / filepath.name)
        # Register the video in the pathtable
        old_video_path = pathlib.Path('/') / os.path.relpath(filepath, dig_dir)
        new_video_path = videos_out / filepath.name
        index.pathtable.register(old_video_path, new_video_path)
