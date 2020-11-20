from bs4 import BeautifulSoup
from pathlib import Path
import os

def extract_page_content(html_string, folder_path_str):
    """Extract contents of a page from a report*b.html file.

    Parameters
    ----------
    html_string : str
        The HTML content of the report*b.html page to be extracted, as a str.
    folder_path_str : str
        Str indicating the current html str's parent folder within /dig/html.

    Returns
    -------
    extracted_paragraphs : list
        List of objects representing paragraphs, each with a type and content.
    """
    soup = BeautifulSoup(html_string, 'html5lib')
    folder_path = Path(folder_path_str)

    extracted_paragraphs = []
    # Replace all relative links in <a> tags with full ones to help generation
    for a in soup.find_all('a'):
        new_href = os.path.normpath(folder_path / a['href'])
        new_href = Path(new_href).as_posix()
        a['href'] = new_href
        del a['target']

    # Extract the page's paragraph contents
    for content in soup.body.contents:
        if isinstance(content, str) and content.strip() == '':
            # Skip processing a '\n' character
            pass
        elif content.name == 'p':
            inner_html = str(content).replace('<p>', '').replace('</p>', '')
            if (inner_html.strip() == '' or inner_html == 'None'):
                # Skip processing an empty <p> tag
                pass
            else:
                p_contents = [
                    item
                    for item in content.contents
                    if str(item).strip() != ''
                ]
                if len(p_contents) == 1 and p_contents[0].name == 'i':
                    # Paragraph tag contains a section title in italics
                    extracted_paragraphs.append({
                        'type': 'italic-title',
                        'content': str(p_contents[0].string)
                    })
                else:
                    # Paragraph tag contains a normal paragraph and text.
                    # Newlines need to be removed during extraction.
                    lines = str(content).split('\n')
                    lines = [
                        line.replace('<p>', '').replace('</p>', '')
                        for line in lines
                    ]
                    lines = [
                        line.replace('  ', ' ').strip() # Remove double spaces
                        for line in lines
                        if line.strip() != ''
                    ]
                    p_inner_html = ' '.join(lines)
                    extracted_paragraphs.append({
                        'type': 'paragraph',
                        'content': p_inner_html
                    })
        elif content.name == 'ul' or content.name == 'ol':
            list_items = str(content) # Keep <ul> or <ol> tags
            extracted_paragraphs.append({
                'type': 'paragraph',
                'content': list_items.strip()
            })
        elif content.name == 'table':
            table = str(content) # Keep table as is, mainly for data downloads
            extracted_paragraphs.append({
                'type': 'paragraph',
                'content': table.strip()
            })
        else:
            # TODO
            pass

    return extracted_paragraphs

def extract_page_title(html_string):
    """Extract the page title from a report*a.html file.

    Parameters
    ----------
    html_string : str
        The HTML content of the report*a.html page to be extracted, as a str.

    Returns
    -------
    str
        Page title as a string, without any HTML tags.
    """
    soup = BeautifulSoup(html_string, 'html.parser')
    return str(soup.body.center.i.string)

def extract_page_number(html_string):
    """Extract the page number from a report*c.html file.

    Parameters
    ----------
    html_string : str
        The HTML content of the report*c.html page to be extracted, as a str.

    Returns
    -------
    str
        Page number as a string, to cover both Arabic and Roman numerals.
    """
    soup = BeautifulSoup(html_string, 'html.parser')
    return str(soup.body.center.string).replace('Page ', '')

def extract_sidebar(html_string, folder_path_str, parent_body_page_name):
    """Extract sidebar info from a "index*_*.html" file.

    Parameters
    ----------
    html_string : str
        The HTML content of the index*_*.html page to be extracted, as a str.
    folder_path_str : str
        Str indicating the current html str's parent folder within /dig/html.
    parent_body_page_name: str
        The name of the body*_*.html page that loads this sidebar as a frame.

    Returns
    -------
    dict
        Dict with this sidebar's name, author, sections, and current section.
    """
    # Note: because the original html content did not have any closing </p>
    # tags, this function depends on using html5lib for proper parsing.
    soup = BeautifulSoup(html_string, 'html5lib')
    folder_path = Path(folder_path_str)
    # Get lines/sections from the sidebar, which are contained in <p> tags
    paragraphs = soup.body.find_all('p')
    # Remove empty paragraphs
    paragraphs = [
        p
        for p in paragraphs
        if str(p).replace('<p>', '').replace('</p>', '').strip() != ''
    ]

    # Use b directly, rather than b.string, to account for Getting Started,
    # where the title may include an <i> tag and thus have no b.string.
    current_module_full_name = (
        str(paragraphs[0].b).replace("<b>", "")
                            .replace("</b>", "")
                            .strip()
    )
    moduleAuthor = None
    sections = []
    current_section = None
    p_tag_with_sections = -1
    if len(paragraphs) == 1:
        # Deal with the edge case of the foreword in part 0
        if paragraphs[0].find('br'):
            moduleAuthor = (
                str(paragraphs[0]).split('<br/>')[-1]
                                  .split('<br>')[-1]
                                  .replace('</p>', '')
                                  .strip()
            )
        # If we aren't in the edge case of the foreword, then
        # only the full module name is in this sidebar, no links or sections.
        # Thus, create one section object to represent this one section.
        # Note that this may lead to inconsistency between the names
        # in report*a.html, tabs*.html, and this sidebar index*.html.
        section_object = {
            'name': current_module_full_name,
            'path': (folder_path / parent_body_page_name).as_posix(),
            'subsections': []
        }
        current_section = section_object
        sections.append(section_object)
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
        links_contents = paragraphs[p_tag_with_sections].contents
        i = 0
        while i < len(links_contents) - 1:
            section_object = None
            content = links_contents[i]
            if content.name == 'a':
                section_object = {
                    'name': str(content.string).strip(),
                    'path': (folder_path / str(content['href'])).as_posix(),
                    'subsections': []
                }
            elif isinstance(content, str) and content.strip() != '':
                # Then it's the link to the current page,
                # without an <a> tag around it.
                section_object = {
                    'name': str(content.string).strip(),
                    'path': (folder_path / parent_body_page_name).as_posix(),
                    'subsections': []
                }
                current_section = section_object

            if section_object:
                if (
                    i != 0 and
                    ('\xa0' in links_contents[i-1] or '\xa0' in content)
                ):
                    # \xa0 is a non-breaking space, or &nbsp; in HTML.
                    # This covers both the case where there's an <a> tag around
                    # the title, and when it's the current page so there's no
                    # <a> tag. Relies on fact that no sidebar has more than
                    # three levels of links, i.e. subsections do not themselves
                    # have subsections.
                    sections[-1]['subsections'].append(section_object)
                else:
                    sections.append(section_object)
            i += 1

    return {
        'currentModuleFullName': current_module_full_name,
        'moduleAuthor': moduleAuthor,
        'sections': sections,
        'currentSection': current_section
    }

def extract_topbar(html_string, folder_path_str, parent_tab_page_name):
    """Extract info on the modules of a chapter from a tabs*.html file."""
    soup = BeautifulSoup(html_string, 'html5lib')
    folder_path = Path(folder_path_str)
    links_contents = soup.body.b.contents
    # Change the parent_tab_page_name so the extraction always uses the first
    # page of a module (tab0.html, tab1.html, etc.), rather than pages like
    # tab0_3.html, when recording the module's path.
    part_nums = parent_tab_page_name.split('_')
    if len(part_nums) > 1:
        parent_tab_page_name = part_nums[0] + ".html"

    modules = []
    current_module = None
    for element in links_contents:
        if isinstance(element, str):
            stripped_string = element.replace('|', '').strip()
            if stripped_string != '':
                # Is the current module, without a link to it
                module_obj = {
                    'moduleShortName': stripped_string,
                    'path': (folder_path / parent_tab_page_name).as_posix()
                }
                modules.append(module_obj)
                current_module = module_obj
        elif element.name == 'a':
            if 'index.html' in element['href'] or 'copyright.html' in element['href']:
                pass
            elif '/' in element['href']:
                raise Exception('/ character found in hyperlink in the topbar of '
                                + (folder_path / parent_tab_page_name).as_posix()
                                + 'when it was not supposed to be.')
            else:
                modules.append({
                    'moduleShortName': str(element.string).strip(),
                    'path': (folder_path / element['href']).as_posix()
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
    full_current_dir_path = dig_parent_dir_path / ("." + current_dir_path)
    sidebar_html_string = readfile(frames[0]['src'], full_current_dir_path)
    report_html_string = readfile(frames[1]['src'], full_current_dir_path)
    report_folder_path = (full_current_dir_path / frames[1]['src']).parent
    report_abc_content = extract_frames(report_html_string, report_folder_path, readfile)

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
    full_current_dir_path = dig_parent_dir_path / ("." + current_dir_path)
    topbar_html_string = readfile(frames[0]['src'], full_current_dir_path)
    body_html_content = get_body_page_html_contents(readfile(frames[1]['src'],
                                                    full_current_dir_path),
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

def process_tab_html_contents(
    html_strings, current_tab_page_name,
    current_dir_path, dig_parent_dir_path, readfile
):
    """Turn the raw html_strings from reading a tab.html file into a dict."""
    title = extract_page_title(html_strings['reporta_html'])
    content = extract_page_content(html_strings['reportb_html'], current_dir_path)
    page_num = extract_page_number(html_strings['reportc_html'])
    sidebar_info = extract_sidebar(html_strings['sidebar_html'],
                                   current_dir_path,
                                   html_strings['body_page_name'])
    topbar_info = extract_topbar(html_strings['topbar_html'],
                                 current_dir_path,
                                 current_tab_page_name)

    processed = {
        "page": {
            "parentModuleShortTitle": topbar_info['currentModule']['moduleShortName'],
            "pageNum": page_num,
            "pageTitle": title,
            "content": content,
        },
        "module": {
            "path": topbar_info['currentModule']['path'],
            "shortTitle": topbar_info['currentModule']['moduleShortName'],
            "fullTitle": sidebar_info['currentModuleFullName'],
            "author": sidebar_info['moduleAuthor'],
            "sections": sidebar_info['sections']
        },
        "additionalSectionInfo": {
            "currentSection": sidebar_info['currentSection'],
            "pageNum": page_num
        }
    }
    return processed

def validate_tab_html_extraction_results(results):
    baseline_module = results[0]['module']
    noError = True
    for result in results:
        if not result['module'] == baseline_module:
            print('Difference in these modules: \n'
                  + str(result['module']) + '\n'
                  + str(baseline_module))
            noError = False

    return noError

def extract_full_module(module_file_names, current_dir_path, dig_parent_dir_path, readfile):
    """Extract content from one module in a chapter and store in a dict."""
    extracted = {
        "module": {},
        "pages": {}
    }
    full_current_dir_path = dig_parent_dir_path / ("." + current_dir_path)
    processed_pages = []
    for filename in module_file_names:
        tab_html_str = readfile(filename, full_current_dir_path)
        extracted_contents = get_tab_page_html_contents(tab_html_str, current_dir_path,
                                                        dig_parent_dir_path, readfile)
        processed_page = process_tab_html_contents(extracted_contents, filename,
                                                   current_dir_path, dig_parent_dir_path, readfile)
        processed_pages.append(processed_page)

    if not validate_tab_html_extraction_results(processed_pages):
        return "Failed: inconsistency in pages within module " + module_file_names[0]

    sectionsToPageNums = {}
    for processed_page in processed_pages:
        sectionInfo = processed_page['additionalSectionInfo']
        pageNumDictKey = (sectionInfo['currentSection']['path']
                          + '-' + sectionInfo['currentSection']['name'])
        if pageNumDictKey in sectionsToPageNums:
            return "Failed: Two sections with the same path + name"
        sectionsToPageNums[pageNumDictKey] = sectionInfo['pageNum']

    extracted['module'] = processed_pages[0]['module']
    for processed_page in processed_pages:
        pageNum = processed_page['page'].pop('pageNum', None)
        extracted['pages'][pageNum] = processed_page['page']

    for section in extracted['module']['sections']:
        section['pageNum'] = sectionsToPageNums[section['path'] + '-' + section['name']]
        if len(section['subsections']) > 0:
            for subsection in section['subsections']:
                subsection['pageNum'] = sectionsToPageNums[subsection['path']
                                                           + '-' + subsection['name']]

    return extracted

def extract_full_chapter(all_module_file_names, current_dir_path, dig_parent_path, readfile):
    """Extract an entire chapter by going through all tab*_*.html files."""
    filenames = sorted(all_module_file_names)
    module_start_tab_names = [filename for filename in filenames if "_" not in filename]
    extracted = {
        "path": current_dir_path,
        "modules": [],
        "pages": {}
    }
    # Sort so that the lowest numbered modules are extracted and added
    # to the "modules" array first.
    module_start_tab_names = sorted(module_start_tab_names)
    for tab_name in module_start_tab_names:
        current_module_file_names = [filename for filename in filenames
                                     if tab_name.split('.')[0] in filename]
        module_object = extract_full_module(current_module_file_names,
                                            current_dir_path, dig_parent_path, readfile)
        extracted['modules'].append(module_object)
    for module in extracted['modules']:
        pages = module.pop('pages')
        for page_num, page_obj in pages.items():
            extracted['pages'][page_num] = page_obj

    return extracted

def extract_standard_part(part_folder_name, dig_parent_dir, readfile):
    """Extract an entire chapter based on folder name, e.g. /dig/html/part2."""
    # Get all tab*.html or tab*_*.html files, which are starting points for
    # the extraction process
    folder_to_extract_full_path = Path(dig_parent_dir) / "./dig/html" / part_folder_name
    tab_filenames = []
    for filepath in folder_to_extract_full_path.iterdir():
        if "tab" in filepath.name and "tabs" not in filepath.name:
            tab_filenames.append(filepath.name)
    return extract_full_chapter(tab_filenames,
                                "/dig/html/" + part_folder_name,
                                Path(dig_parent_dir),
                                readfile)

def reextract_title_page(part_0_data, dig_parent_dir, readfile):
    """Extract the actual title page from part 0 and put it in the dict."""
    title_page_html_str = readfile("report0b.html", Path(dig_parent_dir) / "./dig/html/split")
    soup = BeautifulSoup(title_page_html_str, 'html5lib')
    part_0_data["pages"]["i"]["content"].append({
        "type": "paragraph",
        "content": str(soup.center)
    })
    return part_0_data
