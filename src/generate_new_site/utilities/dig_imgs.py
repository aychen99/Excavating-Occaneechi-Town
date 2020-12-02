import shutil
from os.path import relpath
import pathlib


def copy_images(dig_dir, imgs_in, imgs_out, index):
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
                    new_img = new_dir / img.name
                    if not new_img.exists():
                        shutil.copy(img, new_img)
                    # Register the new path in the path table
                    img = pathlib.Path('/') / relpath(img, dig_dir.parent)
                    index.pathtable.register(img, new_img)

    return


def register_images(dig_dir, imgs_in, imgs_out, index):

    # Iterate through subdirectories
    for img_dir in imgs_in.iterdir():
        if img_dir.name == '.DS_Store':
            continue
        # Save new subdirectory path
        new_dir = imgs_out / img_dir.name
        # Iterate through images
        for img in img_dir.iterdir():
            # Save new image path
            new_img = new_dir / img.name
            # Register the new path in the path table
            img = pathlib.Path('/') / relpath(img, dig_dir)
            index.pathtable.register(img, new_img)
    return
