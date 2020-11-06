from bs4 import BeautifulSoup
from PIL import Image
from pathlib import Path
import os

def extract_image_page(
    html_string, img_page_parent_dir, dig_parent_dir, current_page_name
):
    """Extract an image and its clickable map from a slid_***.html file."""
    soup = BeautifulSoup(html_string, 'html5lib')

    # Assumes no symlinks in any file path found in an <a> tag,
    # so uses os.path.normpath to resolve ".." patterns
    path = Path(img_page_parent_dir) / soup.body.img['src']
    path = Path(os.path.normpath(path)).as_posix()
    html_page_path = (Path(img_page_parent_dir) / current_page_name).as_posix()
    full_path = (Path(dig_parent_dir) / ("." + path)).as_posix()
    figure_num_and_caption = soup.body.center.text.strip().split('.', 1)
    figure_num = figure_num_and_caption[0].replace("Figure", "").strip()
    caption = figure_num_and_caption[1].strip()
    img_dimensions = get_image_dimensions(full_path)

    map_coords = soup.body.map.find_all('area')
    clickable_areas = []
    for area_def in map_coords:
        coords = area_def['coords'].split(',')
        linked_path = (Path(img_page_parent_dir) / area_def['href']).as_posix()
        clickable_areas.append({
            "x1": int(coords[0]),
            "y1": int(coords[1]),
            "x2": int(coords[2]),
            "y2": int(coords[3]),
            "path": linked_path
        })

    return {
        "path": path,
        "htmlPagePath": html_page_path,
        "figureNum": figure_num,
        "caption": caption,
        "clickableAreas": clickable_areas,
        "originalDimensions": {
            "width": int(img_dimensions["width"]),
            "height": int(img_dimensions["height"])
        }
    }

def get_image_dimensions(img_path):
    """Extract image dimensions given the complete path to the image."""
    width, height = Image.open(Path(img_path)).size
    return {
        "width": width,
        "height": height
    }

def extract_video_image_page(html_string):
    """Extract info from a slid_***.mov.html or slid_***.mpg.html file."""
    pass

def extract_all_images(dig_parent_dir, readfile):
    """Return a dictionary of images and their metadata by file path."""
    extracted_images = {}
    for filepath in (Path(dig_parent_dir) / "dig/html/excavations").iterdir():
        if 'slid' in filepath.name and '.mpg' not in filepath.name and '.mov' not in filepath.name:
            html_string = readfile(filepath.name, filepath.parent)
            image_details = extract_image_page(html_string, "/dig/html/excavations", dig_parent_dir, filepath.name)
            extracted_images[image_details['path']] = image_details
    return extracted_images

def generate_metadata_dicts(extracted_images):
    image_path_to_figure_num = {}
    slid_path_to_figure_num = {}
    figure_num_to_image_path = {}
    figure_num_to_slid_path = {}
    for image in extracted_images.values():
        num = image['figureNum']
        image_path = image['path']
        slid_path = image['htmlPagePath']
        image_path_to_figure_num[image_path] = num
        slid_path_to_figure_num[slid_path] = num
        figure_num_to_image_path[num] = image_path
        figure_num_to_slid_path[num] = slid_path

    return {
        "imagePathToFigureNum": image_path_to_figure_num,
        "slidPathToFigureNum": slid_path_to_figure_num,
        "figureNumToImagePath": figure_num_to_image_path,
        "figureNumToSlidPath": figure_num_to_slid_path
    }