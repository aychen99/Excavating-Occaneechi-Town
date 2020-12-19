from . import standard_text_chapter
from bs4 import BeautifulSoup
from pathlib import Path
import os

def process_tab_html_contents(
    html_strings, current_tab_page_name,
    current_dir_path_str, readfile
):
    """Turn the raw html_strings from reading a tab.html file into a dict."""
    title = standard_text_chapter.extract_page_title(html_strings['reporta_html'])
    content = standard_text_chapter.extract_page_content(
        html_strings['reportb_html'], current_dir_path_str
    )
    page_num = "GS" + str(int(current_tab_page_name.split(".")[0].replace("tab", ""))+1)
    sidebar_info = standard_text_chapter.extract_sidebar(
        html_strings['sidebar_html'],
        current_dir_path_str,
        html_strings['body_page_name']
    )
    topbar_info = standard_text_chapter.extract_topbar(
        html_strings['topbar_html'],
        current_dir_path_str,
        current_tab_page_name
    )

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

def extract_full_module(module_file_names, current_dir_path_str, dig_dir_path, readfile):
    """Extract content from one module in a chapter and store in a dict."""
    extracted = {
        "module": {},
        "pages": {}
    }
    full_current_dir_path = dig_dir_path / ("." + current_dir_path_str)
    processed_pages = []
    for filename in module_file_names:
        tab_html_str = readfile(filename, full_current_dir_path)
        extracted_contents = standard_text_chapter.get_tab_page_html_contents(
            tab_html_str,
            current_dir_path_str,
            dig_dir_path,
            readfile,
            has_page_num=False
        )
        processed_page = process_tab_html_contents(extracted_contents, filename,
                                                   current_dir_path_str, readfile)
        processed_pages.append(processed_page)
    
    if not standard_text_chapter.validate_tab_html_extraction_results(processed_pages):
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

def extract_getting_started(dig_dir_str, readfile):
    started_dir_path_obj = Path(dig_dir_str) / "html/started"
    tab_filenames = []
    for filepath in started_dir_path_obj.iterdir():
        if "tab" in filepath.name and "tabs" not in filepath.name:
            tab_filenames.append(filepath.name)
    return standard_text_chapter.extract_full_chapter(
        tab_filenames,
        "/html/started",
        Path(dig_dir_str),
        readfile,
        extract_full_module=extract_full_module
    )
