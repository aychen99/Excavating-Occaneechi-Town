from bs4 import BeautifulSoup
import pathlib
import os
from . import standard_text_chapter

# Inelegant in the interest of time

def extract_sidebar_sections(html_string):
    soup = BeautifulSoup(html_string, 'html5lib')
    section_links = soup.find_all('a')
    sections = []
    for link in section_links:
        path = os.path.normpath(pathlib.Path('/dig/html/descriptions') / link['href'])
        path = str(pathlib.Path(path).as_posix())
        sections.append({
                    'name': str(link.string).strip(),
                    'path': path,
                    'subsections': []
        })

    return sections

def extract_page_title(html_string):
    """Extract the page title from a report*a.html file."""
    soup = BeautifulSoup(html_string, 'html.parser')
    return str(soup.body.center.b.string)

def extract_descriptions(dig_parent_dir, readfile):
    dig_parent_dir_path = pathlib.Path(dig_parent_dir)
    current_dir_path = "/dig/html/descriptions"
    full_current_dir_path = dig_parent_dir_path / ("dig/html/descriptions")

    processed_pages = []
    sections_name_changes = {}
    for filename in full_current_dir_path.iterdir():
        if 'tab' in filename.name and 'tabs' not in filename.name:
            tab_page_content = readfile(filename, full_current_dir_path)
            html_strings = standard_text_chapter.get_tab_page_html_contents(tab_page_content,
                                                                            current_dir_path,
                                                                            dig_parent_dir_path,
                                                                            readfile)
            title = extract_page_title(html_strings['reporta_html'])
            content = standard_text_chapter.extract_page_content(html_strings['reportb_html'])
            page_num = standard_text_chapter.extract_page_number(html_strings['reportc_html'])
            sidebar_info_sections = extract_sidebar_sections(html_strings['sidebar_html'])

            current_section = None
            for section in sidebar_info_sections:
                if section['name'] == title:
                    current_section = section
                    break
                if '(' in title:
                    parts = title.split('(')
                    no_parentheses_title = ' '.join([parts[0].strip(), parts[1].split(')')[1].strip()])
                    if section['name'] == no_parentheses_title:
                        current_section = section
                        sections_name_changes[section['name']] = title
                        break
            if current_section == None:
                raise Exception("Couldn't find the proper section for title " + title)
            processed_pages.append({
                "page": {
                    "parentModuleShortTitle": "Feature Descriptions",
                    "pageNum": page_num,
                    "pageTitle": title,
                    "content": content,
                },
                "module": {
                    "path": "/dig/html/descriptions/tab0.html",
                    "shortTitle": "Feature Descriptions",
                    "fullTitle": "Feature Descriptions",
                    "author": None,
                    "sections": sidebar_info_sections
                },
                "additionalSectionInfo": {
                    "currentSection": current_section,
                    "pageNum": page_num,
                }
            })
    
    if not standard_text_chapter.validate_tab_html_extraction_results(processed_pages):
        return "Failed: inconsistency in pages within module Feature Descriptions."
    
    extracted = {
        "module": {},
        "pages": {}
    }
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
        if section['name'] in sections_name_changes:
            section['name'] = sections_name_changes[section['name']]

    return extracted