from . import standard_text_chapter
from bs4 import BeautifulSoup
from pathlib import Path
import os

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
    content_html_string = readfile(frames[1]['src'], full_current_dir_path)
    content_folder_path = (full_current_dir_path / frames[1]['src']).parent
    content_abc_content = standard_text_chapter.extract_frames(
        content_html_string, content_folder_path, readfile
    )

    return {
        'sidebar_html': sidebar_html_string,
        'contenta_html': content_abc_content[0],
        'contentb_html': content_abc_content[1]
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
        'contenta_html': body_html_content['contenta_html'],
        'contentb_html': body_html_content['contentb_html'],
        'body_page_name': frames[1]['src']
    }

def process_tab_html_contents(
    html_strings, current_tab_page_name,
    current_dir_path, dig_parent_dir_path, readfile, current_body_page_name
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
    tab_html_str = readfile(module_file_names[0], full_current_dir_path)
    associated_body_page_names = []
    for filename in (Path(dig_parent_dir_path) / ('.' + current_dir_path)).iterdir():
        if filename.name.replace('body', '')[0] == module_file_names[0].replace('tab', '')[0]:
            associated_body_page_names.append(filename)
    for filename in associated_body_page_names:
        body_html_contents = get_body_page_html_contents(readfile(filename.name, filename.parent), current_dir_path, dig_parent_dir_path, readfile)
        extracted_contents = get_tab_page_html_contents(tab_html_str, current_dir_path,
                                                            dig_parent_dir_path, readfile)
        extracted_contents['sidebar_html'] = body_html_contents['sidebar_html']
        extracted_contents['contenta_html'] = body_html_contents['contenta_html']
        extracted_contents['contentb_html'] = body_html_contents['contentb_html']
        extracted_contents['body_page_name'] = filename.name

        processed_page = process_tab_html_contents(extracted_contents, module_file_names[0],
                                                    current_dir_path, dig_parent_dir_path, readfile, filename.name)
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

def extract_data_downloads(dig_parent_dir, readfile):
    started_dir_path_obj = Path(dig_parent_dir) / "./dig/html/data"
    tab_filenames = []
    for filepath in started_dir_path_obj.iterdir():
        if "tab" in filepath.name and "tabs" not in filepath.name:
            tab_filenames.append(filepath.name)
    return extract_full_chapter(tab_filenames,
                                "/dig/html/data",
                                Path(dig_parent_dir),
                                readfile)
