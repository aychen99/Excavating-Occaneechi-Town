import shutil
import glob
import os
import pathlib
import json


def edit_page_content(json_obj, page_num, changes):
    """
    Edit the "content" field of a page in one of the standard text chapters.

    Parameters
    ----------
    json_obj : dict
        A json file from running extraction on parts 0, 1, 2, etc.
    page_num : str
        Page number of the page that needs to be modified.
    changes : list
        A list of lists. Each element of changes is itself a list, containing
        an int indicating the paragraph number to change as its first element,
        a string indicating the type of content in the paragraph (essentially
        just "paragraph" or "italic-title") as its second element, and a string
        representing the HTML that should go in that paragraph as its third
        element. The paragraph number can be negative, e.g. -2 means
        second-to-last paragraph.
    Returns
    -------
    json_obj : dict
        Returns the original json_obj argument after making the changes.
    """
    page_obj = json_obj.pages[page_num]
    for change in changes:
        paragraph = page_obj.content[change[0]]
        paragraph.type = change[1]
        paragraph.content = change[2]

    return json_obj

def update_page_title(json_obj, page_num, new_title):
    json_obj.pages[page_num]["pageTitle"] = new_title

    # Does not support changing the title of a subsection, only a section
    moduleFound = False
    modules = json_obj.modules
    for module in modules:
        for section in module.sections:
            if section.pageNum == page_num:
                # Check to see if it's a module with only one section
                if (
                    len(module.sections) == 1
                    and module.shortTitle == module.longTitle
                    and module.longTitle == section.name
                ):
                    module.shortTitle = new_title
                    module.longTitle = new_title
                    # Update the module title in "Table of Contents"
                    update_table_of_contents_page_for_front_matter(

                    )
                section.name = new_title
                moduleFound = True
                break
        if moduleFound:
            break

    # If the module title was modified:
    update_table_of_contents_page_for_front_matter
    # Update the page title always:
    update_table_of_contents_list_of_pages_for_front_matter

    return json_obj

def insert_page_in_front_matter(
    part0_json, part1_json, page_num, content,
    module_short_title, module_long_title, make_new_module, author=None
):
    """
    Insert a page in the front matter (Introduction + Table of Contents).

    Parameters
    ----------
    part0_json : dict
        A json file from running extraction on part 0.
    part1_json : dict
        A json file from running extraction on part 1.
    page_num : str
        Page number for where to insert the page.
    content : list
        TBD
    module_short_title : str
        Short title of the module to insert the page into.
    module_long_title : str
        Long title of the module to insert the page into.
    make_new_module : Boolean
        Indicates whether to create a new module or use an existing matching
        one when inserting the page.
    author : str
        Author of the module to insert the page into. Only used when creating a
        new module.
    """

    # If page number exists, then increment all page numbers starting from it
    # If it doesn't exist, then leave all page numbers the same.
    pass

def update_table_of_contents_page_for_front_matter(
    part1_json, old_title, new_title
):
    """
    Update the "Table of Contents" page in Contents when no new page was added.
    """
    pass

def update_table_of_contents_page_with_new_module_for_front_matter(
    part1_json, old_title, new_title
):
    """
    Update the "Table of Contents" page in Contents when a new page was added.
    """
    pass

def update_table_of_contents_list_of_pages_for_front_matter(
    part1_json, page_num, new_page_inserted
):
    """
    Update the "Pages i-xxxiv" page.
    """
    # If new_page_inserted (a Boolean) == True, bump up all page numbers.
    # Otherwise, don't bump up page numbers.
    pass

def get_json_contents(json_name, jsons_dir):
    """
    Read a JSON file given the name and the directory where it is.
    """
    pass

def increment_roman_numeral(roman_num):
    """
    Increment a roman numeral. Used for page number changes.
    """
    # https://stackoverflow.com/a/40274588
    # https://stackoverflow.com/a/52554841
    num_map = [(50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'),
               (5, 'v'), (4, 'iv'), (1, 'i')]
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
    int_version += 1
    result = ''
    while int_version > 0:
        for i, r in num_map:
            while int_version >= i:
                result += r
                num -= i
    
    return result


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

    # Handle all the JSON file loading here so we don't have to include that in the tests
    # Write all the files back at the end
    # No idea whether this stuff will work with process_contents though
    with (JSONS_DIR / 'part0.json').open() as f:
        part0 = json.load(f)
    with (JSONS_DIR / 'part1.json').open() as f:
        part1 = json.load(f)

    # Insert page operations done at the end for consistency between page nums

    # Fix edition and date at bottom of title page
    edit_page_content(part0, "i", [1, "paragraph",
    """<center>\n\n<p><b><font size=\"+3\">Excavating Occaneechi Town</font><br/>\nArchaeology of an Eighteenth-Century Indian Village in North Carolina</b></p>\n\n<p>\n\n</p><p><i>Edited by</i><br/>\nR. P. Stephen Davis, Jr.<br/>\nPatrick C. Livingood<br/>\nH. Trawick Ward<br/>\nVincas P. Steponaitis\n\n</p><p><i>With contributions by</i><br/>\nLinda Carnes-McNaughton<br/>\nI. Randolph Daniel, Jr.<br/>\nRoy S. Dickens, Jr.<br/>\nLawrence A. Dunmore, III<br/>\nKristen J. Gremillion<br/>\nJulia E. Hammett<br/>\nForest Hazel<br/>\nMary Ann Holm<br/>\nJames H. Merrell<br/>\nGary L. Petherick<br/>\nV. Ann Tippitt\n\n</p><p>\n\n</p><p><b>Second Web Edition<br/>\n2021</b>\n\n</p></center>"""
    ])
    # Change title of "Preface to First Edition" to "Preface to CD-ROM Edition"
    update_page_title(part0, "iii", "Preface to CD-ROM Edition")

    # Change "Preface to Web Edition" to "Preface to First Web Edition"
    update_page_title(part0, "iv", "Preface to First Web Edition")

    # Update Patrick C. Livingood's initials in first two prefaces
    edit_page_content(part0, "iii", [-1, "italic-title", "R.P.S.D., P.C.L., H.T.W., V.P.S.<br/>\nDecember 14, 1997"])
    edit_page_content(part0, "iv", [-1, "italic-title", "R.P.S.D., P.C.L., H.T.W., V.P.S.<br/>\nJuly 28, 2003"])

    # Update Table of Contents with new pages and page numbers
    # Update "Table of Contents" page

    # Add colophon, a.k.a. "How to Cite" page, as page ii
    # insert_page_in_front_matter(part0, part1, "ii")
    # Add "Preface to Second Web Edition" as page vi
    # insert_page_in_front_matter(part0, part1, "vi")

    # Update "Pages i-xxxiii" page contents and title

    # Write edited file back to disk
    UPDATED_JSON_OUTPUT_DIR = JSONS_DIR / "updated"
    UPDATED_JSON_OUTPUT_DIR.mkdir(exist_ok=True)
    with open(UPDATED_JSON_OUTPUT_DIR / 'part0.json', 'w') as f:
        json.dump(part0, f)
    with open(UPDATED_JSON_OUTPUT_DIR / 'part1.json', 'w') as f:
        json.dump(part1, f)
