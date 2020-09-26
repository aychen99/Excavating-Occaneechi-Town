from bs4 import BeautifulSoup
import pathlib

def extract_page_content():
    """Extract contents of a page from a report*b.html file."""
    pass

def extract_page_title(html_string):
    """Extract the page title from a report*a.html file."""
    soup = BeautifulSoup(html_string, 'html.parser')
    return str(soup.body.center.i.string)

def extract_page_number(html_string):
    """Extract the page number from a report*c.html file."""
    soup = BeautifulSoup(html_string, 'html.parser')
    # Note: Leaves page number as a string due to Roman numerals
    return str(soup.body.center.string).replace('Page ', '')

def extract_sidebar(html_string, folder_path, parent_body_page_name):
    """Extract sidebar info from a "index*_*.html" file."""
    # Note: because the original html content did not have any closing </p>
    # tags, this function depends on using html5lib for proper parsing.
    soup = BeautifulSoup(html_string, 'html5lib')
    paragraphs = soup.body.find_all('p')

    currentModuleFullName = str(paragraphs[0].b.string).strip()
    moduleAuthor = None
    sections = None
    p_tag_with_sections = -1
    if len(paragraphs) == 1:
        # Only the full module name is in this sidebar, no links or sections.
        pass
    elif len(paragraphs) == 2:
        # Check to see if it's a combination of the module title & author(s),
        # or of the module title and section links.
        if len(paragraphs[1].find_all('a')) == 0:
            moduleAuthor = str(paragraphs[1].string).strip()
        else:
            p_tag_with_sections = 1
    else:
        moduleAuthor = str(paragraphs[1].string).strip()
        p_tag_with_sections = 2

    if p_tag_with_sections > 0:
        sections = []
        links_contents = paragraphs[p_tag_with_sections].contents
        i = 0
        while i < len(links_contents) - 1:
            section_object = None
            content = links_contents[i]
            if content.name == 'a':
                section_object = {
                    'name': str(content.string).strip(),
                    'path': str(pathlib.PurePosixPath(folder_path) / str(content['href'])),
                    'subsections': []
                }
            elif isinstance(content, str) and content.strip() != '':
                # Then it's the link to the current page, without an <a> tag around it.
                section_object = {
                    'name': str(content.string).strip(),
                    'path': str(pathlib.PurePosixPath(folder_path) / parent_body_page_name),
                    'subsections': []
                }

            if section_object:
                if i != 0 and ('\xa0' in links_contents[i-1] or '\xa0' in content):
                    # Covers both the case where there's an <a> tag around the
                    # title, and when it's the current page so there's no <a> tag.
                    # Relies on fact that no sidebar has more than three levels of
                    # links, i.e. subsections do not themselves have subsections.
                    sections[-1]['subsections'].append(section_object)
                else:
                    sections.append(section_object)
            i += 1

    return {
        'currentModuleFullName': currentModuleFullName,
        'moduleAuthor': moduleAuthor,
        'sections': sections
    }

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
