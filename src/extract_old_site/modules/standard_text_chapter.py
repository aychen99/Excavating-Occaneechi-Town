from bs4 import BeautifulSoup

def extract_page_content():
    pass

def extract_page_title(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    return str(soup.body.center.i.string)

def extract_page_number():
    pass

def extract_sidebar():
    pass

def extract_topbar():
    pass

def extract_full_page():
    pass

def extract_frames(html_string, readfile):
    soup = BeautifulSoup(html_string, 'html.parser')
    data = []
    frames = soup.frameset.find_all(['frame'])
    for frame in frames:
        data.append(readfile(frame['src']))
    return data

def extract_text_chapter_page(html_as_string, data_dict=None, page_number=None):
    pass
