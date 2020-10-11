from bs4 import BeautifulSoup
import pathlib

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

def extract_info_page(html_string):
    """Extract info from a info_**.html file."""
    pass

def extract_clickable_image_page(html_string):
    """Extract info from a slid_***.html file."""
    pass

def extract_video_image_page(html_string):
    """Extract info from a slid_***.mov.html or slid_***.mpg.html file."""
    pass

def get_ctrl_page_contents(html_string):
    """Extract the html contents linked to from within a ctrl_**.html file."""
    pass

def get_exc_page_contents(html_string):
    """Extract the html contents linked to from within a exc_**.html file."""
    pass