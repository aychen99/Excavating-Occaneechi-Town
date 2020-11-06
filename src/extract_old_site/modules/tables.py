from bs4 import BeautifulSoup
from pathlib import Path
import os

def extract_body_page(html_string):
    """Get the string containing the table out of a body.html page."""
    soup = BeautifulSoup(html_string, 'html5lib')
    return str(soup.body.pre).replace('<pre>', '').replace('</pre>', '').strip()

def extract_table_header(html_string):
    """Get the table title and num from a head*.html page."""
    soup = BeautifulSoup(html_string, 'html5lib')
    caption_parts = soup.center.text.strip().split('.', 1)
    return {
        "tableNum": caption_parts[0].replace("Table ", "").strip(),
        "caption": caption_parts[1].strip()
    }

def extract_top_level_table_html(html_string, dig_parent_dir, readfile):
    """Extract all info from a table*.html page."""
    soup = BeautifulSoup(html_string, 'html5lib')
    frames = soup.find_all('frame')
    header_html = readfile(frames[0]['src'], Path(dig_parent_dir) / "dig/html/tables")
    table_body_html = readfile(frames[1]['src'], Path(dig_parent_dir) / "dig/html/tables")
    header_info = extract_table_header(header_html)
    table_body_str = extract_body_page(table_body_html)
    return {
        "tableNum": header_info['tableNum'],
        "caption": header_info['caption'],
        "table": table_body_str
    }

def extract_all_tables(dig_parent_dir, readfile):
    """Extract all tables from /dig/html/tables as strings."""
    table_dir = Path(dig_parent_dir) / "dig/html/tables"
    table_pages_by_num = {}
    for filename in table_dir.iterdir():
        if 'table' not in filename.name:
            continue
        page_num = None
        if '_' in filename.name:
            page_num = filename.name.split('_')[0].replace('table', '')
        else:
            page_num = filename.name.split('.')[0].replace('table', '')
        if page_num not in table_pages_by_num:
            table_pages_by_num[page_num] = []
        table_pages_by_num[page_num].append(filename.name)
    tables = {}
    htmlPathsToTableFileNums = {}
    for page_num, table_pages in table_pages_by_num.items():
        table_info = extract_top_level_table_html(
            readfile(table_pages[0], table_dir),
            dig_parent_dir,
            readfile
        )
        for table_page in table_pages:
            if page_num not in tables:
                tables[page_num] = table_info
                htmlPathsToTableFileNums["/dig/html/tables/" + table_page] = page_num
            else:
                table_info = extract_top_level_table_html(
                    readfile(table_page, table_dir),
                    dig_parent_dir,
                    readfile
                )
                if tables[page_num] != table_info:
                    raise Exception("Table page number " + str(page_num)
                                     + " has table contents that differ.")
                htmlPathsToTableFileNums["/dig/html/tables/" + table_page] = page_num
    return {"tables": tables, "htmlPathsToTableFileNums": htmlPathsToTableFileNums}

def extract_table_image(html_string):
    """Get all information from an img.html in the artifacts folder."""
    soup = BeautifulSoup(html_string, 'html5lib')
    path = Path("/dig/html/tables") / soup.body.img['src']
    path = Path(os.path.normpath(path)).as_posix()
    soup.body.center.a.decompose()
    figure_num_and_caption = soup.body.center.text.strip().split('.', 1)
    figure_num = figure_num_and_caption[0].replace("Figure", "").strip()
    caption = figure_num_and_caption[1].strip()

    return {
        "path": path,
        "figureNum": figure_num,
        "caption": caption
    }

def extract_all_table_image_htmls(dig_parent_dir, readfile):
    """Get a dictionary of tab*.html pages to the corresponding figure nums."""
    table_dir = Path(dig_parent_dir) / "dig/html/tables"
    paths_to_table_nums = {}
    for filename in table_dir.iterdir():
        if 'tab' in filename.name and 'table' not in filename.name:
            html_string = readfile(filename.name, filename.parent)
            image = extract_table_image(html_string)
            paths_to_table_nums[filename.name] = image['figureNum']
        
    return paths_to_table_nums

# Functions for validation
def validate_tables_imgs_with_exc_imgs(table_imgs, exc_imgs):
    pass
