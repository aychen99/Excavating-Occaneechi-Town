from . import standard_text_chapter
from bs4 import BeautifulSoup
from pathlib import Path
import os

def process_tab_html_contents(
    html_strings, current_tab_page_name,
    current_dir_path, readfile, current_body_page_name
):
    """Turn the raw html_strings from reading a tab.html file into a dict."""
    title = standard_text_chapter.extract_page_title(html_strings['contenta_html'])
    content = standard_text_chapter.extract_page_content(
        html_strings['contentb_html'], current_dir_path
    )
    page_num_map = {
        "body0_1.html": "Data 1",
        "body0_2.html": "Data 2",
        "body1_1.html": "Data 3",
        "body2_1.html": "Data 4",
        "body2_2.html": "Data 5",
        "body2_3.html": "Data 6",
        "body3_1.html": "Data 7",
        "body3_2.html": "Data 8",
        "body3_3.html": "Data 9",
        "body3_4.html": "Data 10",
        "body3_5.html": "Data 11",
        "body3_6.html": "Data 12",
        "body3_7.html": "Data 13",
        "body3_8.html": "Data 14",
        "body3_9.html": "Data 15",
        "body3_10.html": "Data 16",
    }
    page_num = page_num_map[current_body_page_name]
    sidebar_info = standard_text_chapter.extract_sidebar(
        html_strings['sidebar_html'],
        current_dir_path,
        html_strings['body_page_name']
    )
    topbar_info = standard_text_chapter.extract_topbar(
        html_strings['topbar_html'],
        current_dir_path,
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

def extract_full_module(module_file_names, current_dir_path, dig_dir_path, readfile):
    """Extract content from one module in a chapter and store in a dict."""
    extracted = {
        "module": {},
        "pages": {}
    }
    full_current_dir_path = dig_dir_path / ("." + current_dir_path)
    processed_pages = []
    tab_html_str = readfile(module_file_names[0], full_current_dir_path)
    associated_body_page_names = []
    for filename in (dig_dir_path / ('.' + current_dir_path)).iterdir():
        if filename.name.replace('body', '')[0] == module_file_names[0].replace('tab', '')[0]:
            associated_body_page_names.append(filename)
    for filename in associated_body_page_names:
        body_html_contents = standard_text_chapter.get_body_page_html_contents(
            readfile(filename.name, filename.parent),
            current_dir_path,
            dig_dir_path,
            readfile,
            has_page_num=False
        )
        extracted_contents = standard_text_chapter.get_tab_page_html_contents(
            tab_html_str,
            current_dir_path,
            dig_dir_path,
            readfile,
            has_page_num=False
        )
        extracted_contents['sidebar_html'] = body_html_contents['sidebar_html']
        extracted_contents['contenta_html'] = body_html_contents['reporta_html']
        extracted_contents['contentb_html'] = body_html_contents['reportb_html']
        extracted_contents['body_page_name'] = filename.name

        processed_page = process_tab_html_contents(extracted_contents, module_file_names[0],
                                                    current_dir_path, readfile, filename.name)
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

def extract_data_downloads(dig_dir_str, readfile):
    started_dir_path_obj = Path(dig_dir_str) / "html/data"
    tab_filenames = []
    for filepath in started_dir_path_obj.iterdir():
        if "tab" in filepath.name and "tabs" not in filepath.name:
            tab_filenames.append(filepath.name)
    return standard_text_chapter.extract_full_chapter(
        tab_filenames,
        "/html/data",
        Path(dig_dir_str),
        readfile,
        extract_full_module=extract_full_module
    )
