from bs4 import BeautifulSoup
from PIL import Image
import pathlib
import os

def extract_image_page(html_string, img_page_parent_dir, dig_parent_dir):
    """Extract an image and its clickable map from a slid_***.html file."""
    soup = BeautifulSoup(html_string, 'html5lib')

    # Assumes no symlinks in any file path found in an <a> tag,
    # so uses os.path.normpath to resolve ".." patterns
    path = pathlib.Path(img_page_parent_dir) / soup.body.img['src']
    path = str(pathlib.Path(os.path.normpath(path)).as_posix())
    full_path = str(pathlib.PurePosixPath(dig_parent_dir) / ("." + path))
    caption = soup.body.center.text.strip()
    img_dimensions = get_image_dimensions(full_path)

    map_coords = soup.body.map.find_all('area')
    clickable_areas = []
    for area_def in map_coords:
        coords = area_def['coords'].split(',')
        linked_path = str(pathlib.PurePosixPath(img_page_parent_dir) / area_def['href'])
        clickable_areas.append({
            "x1": int(coords[0]),
            "y1": int(coords[1]),
            "x2": int(coords[2]),
            "y2": int(coords[3]),
            "path": linked_path
        })

    return {
        "path": path,
        "caption": caption,
        "clickableAreas": clickable_areas,
        "originalDimensions": {
            "width": int(img_dimensions["width"]),
            "height": int(img_dimensions["height"])
        }
    }

def get_image_dimensions(img_path):
    """Extract image dimensions given the complete path to the image."""
    width, height = Image.open(pathlib.Path(img_path)).size
    return {
        "width": width,
        "height": height
    }