from .image_page import extract_image_page
from bs4 import BeautifulSoup
import pathlib
import os

# Because all the pages are stored in the "/dig/html/excavations" folder,
# those are hardcoded into this module.

def extract_zoom_to(html_string):
    """Extract related elements to a feature from a zoom_**.html file."""
    soup = BeautifulSoup(html_string, 'html5lib')
    links = soup.body.find_all('a')
    extracted = []
    for link in links:
        extracted.append({
            "name": str(link.string).strip(),
            "path": str(pathlib.PurePosixPath("/dig/html/excavations") / link['href'])
        })
    return extracted

def extract_info_page(html_string, current_dir_path, dig_parent_dir_path, readfile):
    """Extract info from a info_**.html file."""
    # Assumes set structure of the document, particularly 
    # the main paragraph and td cells

    def remove_dots_and_make_posix(filename):
        path = os.path.normpath(pathlib.Path('/dig/html/excavations') / filename)
        return str(pathlib.Path(path).as_posix())

    soup = BeautifulSoup(html_string, 'html5lib')
    name = str(soup.body.big.b.string).strip()
    exc_area_icon_path = remove_dots_and_make_posix(soup.body.img['src'])
    main_paragraph = soup.body.find_all('p')[0]
    extracted_info = {'Dimensions': {}}
    i = 0
    while i < len(main_paragraph.contents):
        content = main_paragraph.contents[i]
        if isinstance(content, str) and ':' in content:
            line_parts = [part.strip() for part in content.split(':')]
            value = line_parts[1]
            # Handle ft^2 and ft^3, which use a <sup> tag
            if i + 1 < len(main_paragraph.contents):
                next_content_str = str(main_paragraph.contents[i+1]).strip()
                if '<sup>' in next_content_str:
                    value = value + next_content_str.replace('<small>', '').replace('</small>', '')
            if any(type_of_info in line_parts[0] for type_of_info in ['Type', 'Volume', 'Area']):
                extracted_info[line_parts[0]] = value
            else:
                extracted_info['Dimensions'][line_parts[0]] = value
        i += 1
    td_cells = soup.body.table.tbody.find_all('td')
    images = []
    full_current_dir_path = pathlib.Path(dig_parent_dir_path) / ("." + current_dir_path)
    for link in td_cells[0].find_all('a'):
        if '.mov.html' in link['href'] or '.mpg.html' in link['href']:
            print("Found mov/mpg link in " + name)
            return
        else:
            image_page_html = readfile(link['href'], full_current_dir_path)
            image = extract_image_page(image_page_html, current_dir_path,
                                       dig_parent_dir_path, link['href'])
            images.append(image)
    
    artifacts_path = None
    if td_cells[1].a:
        artifacts_path = remove_dots_and_make_posix(td_cells[1].a['href'])
    description_path = None
    if td_cells[2].a:
        description_path = remove_dots_and_make_posix(td_cells[2].a['href'])

    return {
        "name": name,
        "miniMapIcon": exc_area_icon_path,
        "info": extracted_info,
        "images": images,
        "artifactsPath": artifacts_path,
        "descriptionPath": description_path
    }

def get_ctrl_page_contents(html_string, current_dir_path, dig_parent_dir_path, readfile):
    """Extract the html contents linked to from within a ctrl_**.html file."""
    full_current_dir_path = pathlib.Path(dig_parent_dir_path) / ("." + current_dir_path)
    
    soup = BeautifulSoup(html_string, 'html5lib')
    frames = soup.find_all('frame')

    info_page_html = readfile(frames[0]['src'], full_current_dir_path)
    zoom_page_html = readfile(frames[1]['src'], full_current_dir_path)

    extracted = extract_info_page(info_page_html, current_dir_path, dig_parent_dir_path, readfile)
    extracted['relatedElements'] = extract_zoom_to(zoom_page_html)
    return extracted

def get_exc_page_contents(html_string, current_dir_path, dig_parent_dir_path, readfile):
    """Extract the html contents linked to from within a exc_**.html file."""
    # Essentially do the exact same as for the ctrl page for now.
    full_current_dir_path = pathlib.Path(dig_parent_dir_path) / ("." + current_dir_path)

    frames = BeautifulSoup(html_string, 'html5lib').find_all('frame')
    ctrl_html_string = readfile(frames[1]['src'], full_current_dir_path)
    return get_ctrl_page_contents(ctrl_html_string, current_dir_path, dig_parent_dir_path, readfile)