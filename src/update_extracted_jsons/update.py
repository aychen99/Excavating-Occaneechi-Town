import shutil
import glob
import os
import pathlib
import json
from bs4 import BeautifulSoup


def edit_page_content(json_obj, page_num, paragraph_num, op_type, paragraph_type=None, paragraph_html=None):
    """
    Edit the "content" field of a page in one of the standard text chapters.
    Limited to performing one operation per call to this function so that
    multiple insert or delete operations don't conflict with each other.

    Parameters
    ----------
    json_obj : dict
        A json file from running extraction on parts 0, 1, 2, etc. in which the
        page to be modified is found.
    page_num : str
        Page number of the page that needs to be modified.
    paragraph_num : int
        Paragraph number to perform the change on. It can be negative, e.g. -2
        means second-to-last paragraph.
    op_type : str
        The type of operation to perform on the paragraph, specifically one of
        insert, delete, or modify.
    paragraph_type : str
        For insert and modify operations, the type of content in the paragraph
        (essentially just "paragraph" or "italic-title").
    paragraph_html : str
        For insert and modify operations, the type of content that should go
        in that paragraph.
    """
    page = json_obj["pages"][page_num]
    if op_type == "delete":
        page["content"].pop(paragraph_num)
    elif op_type == "insert":
        page["content"].insert(paragraph_num, {
            "type": paragraph_type,
            "content": paragraph_html
        })
    elif op_type == "modify":
        paragraph = page["content"][paragraph_num]
        paragraph["type"] = paragraph_type
        paragraph["content"] = paragraph_html
    else:
        raise Exception(
            "Invalid op-type specified. Must be one of insert, "
            "modify, or delete."
        )

def update_page_title(json_obj, part1_json, chapter_name, page_num, new_title):
    """
    Update the title of a page and perform related changes.

    Parameters
    ----------
    json_obj : dict
        A json file from running extraction on parts 0, 1, 2, etc. in which the
        page to be modified is found.
    part1_json : dict
        The json file from extracting the "Contents" chapter, i.e. part 1.
        Needed as the table of contents found in this json need to be updated
        with the new page title as well.
    chapter_name : str
        The name of the chapter that json_obj corresponds to, i.e. one of
        "Introduction", "Contents", "Background", "Artifacts", etc.
    page_num : str
        Page number of the page that needs to be modified.
    new_title : str
        The new title of the page.
    """
    # Change the title in the page object itself.
    json_obj["pages"][page_num]["pageTitle"] = new_title

    # Change the title of the page's parent section/module, and also edit
    # the right parts of the "Contents" chapter to reflect the new title.
    # Does not support changing the title of a subsection, only a section.
    for outer_module in json_obj["modules"]:
        module = outer_module["module"]
        for section in module["sections"]:
            if section["pageNum"] == page_num:
                # Check to see if this is the only section of the parent module
                # and update the module title if it is.
                # If the module's shortTitle and fullTitle differed previously,
                # then they will both be changed to the new title.
                if (
                    len(module["sections"]) == 1
                    and module["fullTitle"] == section["name"]
                ):
                    module["shortTitle"] = new_title
                    module["fullTitle"] = new_title
                    # Update the module title in "Table of Contents"
                    update_table_of_contents_page_in_contents(
                        part1_json, chapter_name, section["name"], new_title
                    )
                # Update the page/section title:
                update_list_of_pages_page_in_contents(
                    part1_json, chapter_name, page_num,
                    section["name"], new_title
                )
                section["name"] = new_title
                return

    raise Exception(
        "Could not update page title for " + chapter_name
        + ", page " + page_num + ", new title " + new_title
    )

def insert_page_in_front_matter():
    """
    Insert a page in the front matter (Introduction + Table of Contents).
    """
    # TODO
    return

def update_table_of_contents_page_in_contents(
    part1_json, chapter_name, old_title, new_title
):
    """
    Update the "Table of Contents" page in Contents when a module title changes.
    """
    page_num = ""
    # Get the table of contents page object
    for outer_module in part1_json["modules"]:
        module = outer_module["module"]
        if module["shortTitle"] == "Table of Contents":
            page_num = module["sections"][0]["pageNum"]
            break
    page = part1_json["pages"][page_num]

    # Update the HTML content of the page to use the new module title
    for index, paragraph in enumerate(page["content"]):
        if paragraph["content"].replace("<b>", "").replace("</b>", "") == chapter_name:
            ul = page["content"][index + 1]["content"]
            soup = BeautifulSoup(ul, "html5lib")
            for li in soup.ul.find_all("li"):
                if old_title in li.a.text:
                    li.a.clear()
                    i_tag = soup.new_tag("i")
                    i_tag.string = new_title
                    li.a.append(i_tag)
                    break
            new_ul = str(soup.body).replace("<body>", "").replace("</body>", "")
            page["content"][index + 1]["content"] = new_ul
            return

    raise Exception(
        "Could not update table of contents page for module originally titled "
        + old_title + " in chapter " + chapter_name
    )

def update_table_of_contents_page_with_new_module_for_front_matter():
    """
    Update the "Table of Contents" page in Contents when adding a new module.
    """
    # TODO
    return

def update_list_of_pages_page_in_contents(
    part1_json, chapter_name, page_num, old_title, new_title
):
    """
    Update the right "Pages **-**" page when a page title changes.
    Only works with a change in the "Introduction" and "Contents" chapters.
    """
    if chapter_name not in ["Introduction", "Contents"]:
        raise Exception(
            'Error: updating the table of contents for a page that is not in '
            'the "Introduction" or "Contents" chapter is not yet supported.'
        )

    # Get the right "Pages **-**" page in the List of Pages to update.
    list_of_pages_page_num = ""
    for outer_module in part1_json["modules"]:
        module = outer_module["module"]
        if module["fullTitle"] == "List of Pages":
            for section in module["sections"]:
                if "Pages i" in section["name"]:
                    list_of_pages_page_num = section["pageNum"]
                    break
            break
    page = part1_json["pages"][list_of_pages_page_num]

    # Change the list of pages to use the new title.
    for paragraph in page["content"]:
        if f"Page {page_num}" in paragraph["content"]:
            if old_title not in paragraph["content"]:
                existing_title = paragraph["content"].split("</a>.")[1]
                print(
                    "Page num found, titles don't match. Expected: "
                    + old_title + ", Got: " + existing_title
                )
            paragraph["content"] = (
                paragraph["content"].split("</a>.")[0] + f"</a>. {new_title}."
            )
            return

    raise Exception(
        "Could not update page title in list of pages for page " + page_num
        + " in chapter " + chapter_name
    )

def update_list_of_pages_in_contents_with_inserted_page(
    part1_json, chapter_name, inserted_page_num, inserted_page_title, new_href
):
    """
    Update the right "Pages **-**" page when a new page is inserted.
    Run this function BEFORE update_json_obj_when_inserting_page_for_front_matter.
    Only works with a change in the "Introduction" and "Contents" chapters.
    """
    # TODO
    return

def update_json_obj_when_inserting_page_for_front_matter(
    part0_json, part1_json, page_num
):
    # TODO
    return

def roman_to_int(roman_num):
    # https://stackoverflow.com/a/52554841
    roman_dict = {'l': 50, 'xl': 40, 'x': 10, 'ix': 9,
                  'v': 5, 'iv': 4, 'i': 1}

    int_version = 0
    while roman_num:
        if roman_num[:2] in roman_dict:
            int_version += roman_dict[roman_num[:2]]
            roman_num = roman_num[2:]
        elif roman_num[:1] in roman_dict:
            int_version += roman_dict[roman_num[:1]]
            roman_num = roman_num[1:]
        else:
            raise Exception('could not convert roman numeral')

    return int_version

def int_to_roman(int_version):
    # https://stackoverflow.com/a/40274588
    num_map = [(50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'),
               (5, 'v'), (4, 'iv'), (1, 'i')]

    result = ''
    while int_version > 0:
        for i, r in num_map:
            while int_version >= i:
                result += r
                int_version -= i
    
    return result

def increment_roman_num(roman_num):
    """
    Increment a roman numeral string. Used for page number changes.
    """
    return int_to_roman(roman_to_int(roman_num) + 1)


def update_extracted_jsons(config, jsons_dir, version="dig"):
    """
    Function in which all changes to site content extracted from the old site
    are hardcoded. Relies on manual inspection of extracted data in the jsons.
    Does not support any changes that are specific to dig or digpro.
    """
    JSONS_DIR = None
    if jsons_dir == "Default":
        JSONS_DIR = pathlib.Path("jsons") / version
    else:
        JSONS_DIR = pathlib.Path(jsons_dir)

    if not JSONS_DIR.exists():
        print('Extracted jsons directory: {} does not exist. Updating aborted.'
              .format(str(JSONS_DIR)))
        return

    # Handle all the JSON file loading here for testability purposes
    with (JSONS_DIR / 'part0.json').open() as f:
        part0 = json.load(f)
    with (JSONS_DIR / 'part1.json').open() as f:
        part1 = json.load(f)

    # Insert page operations done at the end for consistency between page nums

    # Fix edition and date at bottom of title page
    edit_page_content(part0, "i", 0, "modify", "paragraph",
    """<center>\n\n<p><b><font size=\"+3\">Excavating Occaneechi Town</font><br/>\nArchaeology of an Eighteenth-Century Indian Village in North Carolina</b></p>\n\n<p>\n\n</p><p><i>Edited by</i><br/>\nR. P. Stephen Davis, Jr.<br/>\nPatrick C. Livingood<br/>\nH. Trawick Ward<br/>\nVincas P. Steponaitis\n\n</p><p><i>With contributions by</i><br/>\nLinda Carnes-McNaughton<br/>\nI. Randolph Daniel, Jr.<br/>\nRoy S. Dickens, Jr.<br/>\nLawrence A. Dunmore, III<br/>\nKristen J. Gremillion<br/>\nJulia E. Hammett<br/>\nForest Hazel<br/>\nMary Ann Holm<br/>\nJames H. Merrell<br/>\nGary L. Petherick<br/>\nV. Ann Tippitt\n\n</p><p>\n\n</p><p><b>Second Web Edition<br/>\n2021</b>\n\n</p></center>"""
    )
    # Update Patrick C. Livingood's initials in first two prefaces
    edit_page_content(part0, "iii", -1, "modify", "italic-title", "R.P.S.D., P.C.L., H.T.W., V.P.S.<br/>\nDecember 14, 1997")
    edit_page_content(part0, "iv", -1, "modify", "italic-title", "R.P.S.D., P.C.L., H.T.W., V.P.S.<br/>\nJuly 28, 2003")

    # Change title of "Preface to First Edition" to "Preface to CD-ROM Edition"
    update_page_title(part0, part1, "Introduction", "iii", "Preface to CD-ROM Edition")
    # Change "Preface to Web Edition" to "Preface to First Web Edition"
    update_page_title(part0, part1, "Introduction", "iv", "Preface to First Web Edition")

    # Add colophon, a.k.a. "How to Cite" page, as page ii
    # TODO
    # Add "Preface to Second Web Edition" as page vi
    # TODO

    # Write edited file(s) back to disk
    UPDATED_JSON_OUTPUT_DIR = JSONS_DIR / "updated"
    UPDATED_JSON_OUTPUT_DIR.mkdir(exist_ok=True)
    with open(UPDATED_JSON_OUTPUT_DIR / 'part0.json', 'w') as f:
        json.dump(part0, f, indent=4)
    with open(UPDATED_JSON_OUTPUT_DIR / 'part1.json', 'w') as f:
        json.dump(part1, f, indent=4)
