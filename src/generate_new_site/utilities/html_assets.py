import shutil
import glob
import os
import pathlib
import json


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
                    shutil.copy(name, assets_out / new_path)

    return


def copy_videos(videos_in, videos_out):
    if not videos_out.is_dir():
        videos_out.mkdir(parents=True, exist_ok=True)
    for filepath in videos_in.iterdir():
        shutil.copy(filepath, videos_out / filepath.name)


def copy_data(data_in, data_out):
    copy_html_assets(data_in, data_out)
