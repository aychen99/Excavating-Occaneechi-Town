import shutil
from os.path import relpath
import pathlib

high_res_images = {}

def copy_images(dig_dir, imgs_in, imgs_out, index, new_img_dir=None):
    if new_img_dir is not None:
        new_imgs = {path.stem.lower(): path for path in new_img_dir.rglob("*.*")}
    # Iterate through subdirectories
    for img_dir in imgs_in.iterdir():
        if img_dir.is_dir():
            # Make copy of subdirectory in output img directory
            new_dir = imgs_out / img_dir.name
            new_dir.mkdir(parents=True, exist_ok=True)
            # Iterate through images
            for img in img_dir.iterdir():
                if img.suffix in {".jpeg", ".jpg", ".gif"}:
                    # Make copy of image in new subdirectory
                    # Handle higher res img
                    if new_img_dir is not None and img.stem.lower() in new_imgs:
                        new_img = new_dir / new_imgs[img.stem.lower()].name
                        if not new_img.exists():
                            shutil.copy(new_imgs[img.stem.lower()], new_img)
                        high_res_images[img.name] = new_img.name
                    else:
                        new_img = new_dir / img.name
                        if not new_img.exists():
                            shutil.copy(img, new_img)
                    # Register the new path in the path table
                    img = pathlib.Path('/') / relpath(img, dig_dir)
                    index.pathtable.register(img, new_img)
    return


def register_images(dig_dir, imgs_in, imgs_out, index, new_img_dir=None):
    if new_img_dir is not None:
        new_imgs = {path.stem.lower(): path for path in new_img_dir.rglob("*.*")}
    # Iterate through subdirectories
    for img_dir in imgs_in.iterdir():
        if img_dir.name == '.DS_Store':
            continue
        # Save new subdirectory path
        new_dir = imgs_out / img_dir.name
        # Iterate through images
        for img in img_dir.iterdir():
            # Save new image path
            if new_img_dir is not None and img.stem.lower() in new_imgs:
                new_img = new_dir / new_imgs[img.stem.lower()].name
                high_res_images[img.name] = new_img.name
            else:
                new_img = new_dir / img.name
            # Register the new path in the path table
            img = pathlib.Path('/') / relpath(img, dig_dir)
            index.pathtable.register(img, new_img)
    return
