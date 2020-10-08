from bs4 import BeautifulSoup
import pathlib

def extract_page_content(html_string):
    """Extract contents of a page from a report*b.html file."""
    soup = BeautifulSoup(html_string, 'html5lib')

    extracted = []
    for content in soup.body.contents:
        if isinstance(content, str) and content.strip() == '':
            # Skip processing an '\n' character
            pass
        elif content.name == 'p':
            inner_html = str(content).replace('<p>', '').replace('</p>', '')
            if (inner_html.strip() == '' or inner_html == 'None'):
                # Skip processing an empty <p> tag
                pass
            else:
                p_contents = [item for item in content.contents if str(item).strip() != '']
                if len(p_contents) == 1 and p_contents[0].name == 'i':
                    extracted.append({
                        'type': 'italic-title',
                        'content': str(p_contents[0].string)
                    })
                else:
                    lines = str(content).split('\n')
                    lines = [line.replace('<p>', '').replace('</p>', '') for line in lines]
                    lines = [line.replace('  ', ' ').strip() for line in lines if line.strip() != '']
                    p_html = ' '.join(lines)
                    extracted.append({
                        'type': 'paragraph',
                        'content': p_html
                    })
        else:
            # TODO
            pass

    return extracted

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
    current_section = None
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
                current_section = section_object

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
        'sections': sections,
        'currentSection': current_section
    }

def extract_topbar(html_string, folder_path, parent_tab_page_name):
    """Extract info on the modules of a chapter from a tabs*.html file."""
    soup = BeautifulSoup(html_string, 'html5lib')
    links_contents = soup.body.b.contents

    modules = []
    current_module = None
    for element in links_contents:
        if isinstance(element, str):
            stripped_string = element.replace('|', '').strip()
            if stripped_string != '':
                # Is the current module, without a link to it
                module_obj = {
                    'moduleShortName': 'Archaeology',
                    'path': str(pathlib.PurePosixPath(folder_path) / parent_tab_page_name)
                }
                modules.append(module_obj)
                current_module = module_obj
        elif element.name == 'a':
            if 'index.html' in element['href'] or 'copyright.html' in element['href']:
                pass
            else:
                modules.append({
                    'moduleShortName': str(element.string).strip(),
                    'path': str(pathlib.PurePosixPath(folder_path) / element['href'])
                })

    return {
        "modules": modules,
        "currentModule": current_module
    }

def extract_frames(html_string, full_current_dir_path, readfile):
    """Read in data from the contained frames in a report#.html page."""
    soup = BeautifulSoup(html_string, 'html.parser')
    data = []
    frames = soup.frameset.find_all(['frame'])
    for frame in frames:
        data.append(readfile(frame['src'], full_current_dir_path))
    return data

def get_body_page_html_contents(html_string, current_dir_path, dig_parent_dir_path, readfile):
    """Extract all parts of a body*_*.html page and its contained frames.
    
    Parameters
    ----------
    html_string : str
        Result of reading a body*_*.html file
    current_dir_path : str
        Directory of the body*_*.html file in Posix Path format
        (e.g. "/dig/html/part2").
    dig_parent_dir_path : Path
        Containing directory of the /dig folder as a Path object, e.g.
        if body0_1.html is found in "C:\\Users\\Dev\\dig\\html\\part2",
        then dig_parent_dir_path is a WindowsPath('C:/Users/Dev').
    readfile : function
        Function to read any file based on the file name or folder path.
    """

    soup = BeautifulSoup(html_string, 'html5lib')
    frames = soup.find_all('frame')
    full_current_dir_path = dig_parent_dir_path / current_dir_path
    sidebar_html_string = readfile(frames[0]['src'], full_current_dir_path)
    report_html_string = readfile(frames[1]['src'], full_current_dir_path)
    report_abc_content = extract_frames(report_html_string, full_current_dir_path, readfile)

    return {
        'sidebar_html': sidebar_html_string,
        'reporta_html': report_abc_content[0],
        'reportb_html': report_abc_content[1],
        'reportc_html': report_abc_content[2]
    }

def get_tab_page_html_contents(html_string, current_dir_path, dig_parent_dir_path, readfile):
    """Extract all parts of a tab*.html or tab*_*.html page and its frames."""
    soup = BeautifulSoup(html_string, 'html5lib')
    frames = soup.find_all('frame')
    full_current_dir_path = dig_parent_dir_path / current_dir_path
    topbar_html_string = readfile(frames[0]['src'], full_current_dir_path)
    body_html_content = get_body_page_html_contents(readfile(frames[1]['src'], full_current_dir_path),
                                                    current_dir_path,
                                                    dig_parent_dir_path,
                                                    readfile)
    return {
        'topbar_html': topbar_html_string,
        'sidebar_html': body_html_content['sidebar_html'],
        'reporta_html': body_html_content['reporta_html'],
        'reportb_html': body_html_content['reportb_html'],
        'reportc_html': body_html_content['reportc_html'],
        'body_page_name': frames[1]['src']
    }

def extract_full_module():
    pass

def extract_full_chapter():
    pass

def extract_text_chapter_page(html_as_string, data_dict=None, page_number=None):
    pass
