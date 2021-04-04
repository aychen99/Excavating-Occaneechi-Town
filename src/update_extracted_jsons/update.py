import shutil
import glob
import os
import pathlib
import json
from bs4 import BeautifulSoup


def edit_page_content(
    json_obj, page_num, paragraph_num, op_type,
    paragraph_type=None, paragraph_html=None
):
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

    # Change the title of the page's parent section/module, and also edit
    # the right parts of the "Contents" chapter to reflect the new title.
    # Does not support changing the title of a subsection, only a section.
    for module_index, outer_module in enumerate(json_obj["modules"]):
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
                    page_obj = json_obj["pages"][page_num]
                    page_obj["parentModuleShortTitle"] = new_title
                    # Update the module title in "Table of Contents"
                    update_table_of_contents_page_in_contents(
                        part1_json, chapter_name, module_index, new_title,
                        old_title=section["name"]
                    )
                # Update the page/section title:
                update_list_of_pages_page_in_contents(
                    part1_json, chapter_name, page_num, new_title,
                    old_title=section["name"]
                )
                section["name"] = new_title
                # Change the title in the page object itself.
                json_obj["pages"][page_num]["pageTitle"] = new_title
                return

    raise Exception(
        "Could not update page title for " + chapter_name
        + ", page " + page_num + ", new title " + new_title
    )

def insert_page_and_module_in_front_matter(
    part1_json, part_collection_jsons, json_to_insert_num, module_num,
    content, chapter_name, module_short_title, module_long_title,
    new_section_path, new_module_path, author=None
):
    """
    Insert a page and module in Introduction + Table of Contents.

    Note that in the original site, page v is missing from the front matter.
    To simplify code logic, the assumption is made that the first page inserted
    will be the "How to Cite" page at page ii, thus resolving the issue of a
    missing page v. No other pages in any other chapters should be missing.

    Parameters
    ----------
    part1_json : dict
        A json file from running extraction on part 1, the "Contents" chapter.
    part_collection_jsons : list
        A list of the jsons that come from extracting a complete collection of
        parts. Specifically, "Introduction + Contents" for this function.
    json_to_insert_num : int
        The json in the part_collection_jsons list where the new page should
        be inserted, specified as the int index within the list (and thus
        starting from 0).
    module_num : int
        Either the index of the currently existing module where the page will
        be inserted, or the index where a new module should be created. Index
        starts from 0.
    content : list
        List of dicts. Each dict has a key "type" (which will usually be either
        "paragraph" or "italic-title") and a key "content" (which contains the
        HTML content that is to go in that paragraph/section of the page).
        Essentially, just replicate the format of an already extracted JSON and
        that will work when passed in as an argument.
    chapter_name : str
        Name of the chapter that the page is being inserted in. Used as a
        double check for consistency purposes.
    module_short_title : str
        Short title of the module when creating a new module.
    module_long_title : str
        Long title of the module when creating a new module.
    new_section_path : str
        A href link to the section being created along with the module.
    new_module_path : str
        A href link to the module being created, used for hyperlink resolving.
    author : str
        Author of the module to insert the page into. Only used when creating a
        new module.
    """

    # NOTE: the "Feature Descriptions" extraction results differ from all the
    # other text chapters, so any changes there will need special code later

    json_path_to_chapter_name_dict = {
        "/html/part0": "Introduction",
        "/html/part1": "Contents",
    }
    json_to_insert = part_collection_jsons[json_to_insert_num]
    
    # Check that the chapter name is correct for the JSON selected, as Chapter
    # Name is required in later function calls
    if json_path_to_chapter_name_dict[json_to_insert["path"]] != chapter_name:
        raise Exception(
            "Chapter name of JSON and provided chapter name argument don't "
            + "match, expected: "
            + json_path_to_chapter_name_dict[json_to_insert["path"]]
            + ", got: " + chapter_name
        )

    # Get the page number that the new page will receive
    if len(json_to_insert["modules"]) == module_num:
        # Inserting page at end of existing chapter/part
        outer_module = json_to_insert["modules"][-1]
        page_num = outer_module["module"]["sections"][-1]["pageNum"]
        page_num = int_to_roman(roman_to_int(page_num) + 1)
    elif len(json_to_insert["modules"]) > module_num:
        outer_module = json_to_insert["modules"][module_num]
        page_num = outer_module["module"]["sections"][0]["pageNum"]
    else:
        raise Exception(
            "Attempting to insert page more than one module ahead of the last "
            "module in the chapter, chapter " + chapter_name + "module num "
            + module_num
        )

    update_table_of_contents_page_in_contents(
        part1_json, chapter_name, module_num, module_long_title,
        new_module=True, new_href=new_section_path
    )
    update_list_of_pages_page_in_contents(
        part1_json, chapter_name, page_num, module_long_title,
        new_page=True, new_href=new_section_path
    )
    update_json_obj_before_inserting_page_for_front_matter(
        part_collection_jsons, json_to_insert_num, chapter_name, page_num
    )
    json_to_insert["modules"].insert(module_num, {
        "module": {
            "path": new_module_path,
            "shortTitle": module_short_title,
            "fullTitle": module_long_title,
            "author": author,
            "sections": [{
                "name": module_long_title,
                "path": new_section_path,
                "subsections": [],
                "pageNum": page_num
            }]
        }
    })

    json_to_insert["pages"][page_num] = {
        "parentModuleShortTitle": module_short_title,
        "pageTitle": module_long_title,
        "content": content
    }

def update_table_of_contents_page_in_contents(
    part1_json, chapter_name, module_num, new_title, new_module=False,
    old_title=None, new_href=None
):
    """
    Update/add a module title to the "Table of Contents" page in Contents.

    Parameters
    ----------
    part1_json : dict
        A json file from running extraction on part 1, the "Contents" chapter.
    chapter_name : str
        Name of the chapter to update/add the module title in. In line with the
        titles in the "Table of Contents" page, this must be one of
        "Getting Started", "Archaeology Primer", "Introduction", "Contents",
        "Background", "Excavations", "Artifacts", "Food Remains",
        "Interpretations", "Electronic Dig", "Bibliography", and "Downloads".
    module_num : int
        The index where a new module should be created in the given chapter.
        Zero-based.
    new_title : str
        The new title for the module that is being updated/added.
    new_module : Boolean
        Add a new module if True, or change an old one if False.
    old_title : str
        The old title of the module that is being updated if new_module is set
        to False.
    new_href : str
        A href link to the section being created along with the new module
        if new_module is set to True.
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
        ul_name = paragraph["content"].replace("<b>", "").replace("</b>", "")
        if ul_name == chapter_name:
            ul = page["content"][index + 1]["content"]
            soup = BeautifulSoup(ul, "html5lib")
            existing_lis = soup.ul.find_all("li")
            if new_module:
                if not new_href:
                    raise Exception(
                        "New href needed to add module to ToC, new module "
                        + new_title + " in chapter " + chapter_name
                    )
                new_li = soup.new_tag("li")
                a_tag = soup.new_tag("a")
                a_tag["href"] = new_href
                i_tag = soup.new_tag("i")
                i_tag.string = new_title
                a_tag.append(i_tag)
                new_li.append(a_tag)
                if module_num == len(existing_lis):
                    soup.ul.append(new_li)
                elif module_num > len(existing_lis):
                    raise Exception(
                        "Trying to add a new module too far in, new module "
                        + new_title + "in chapter " + chapter_name
                        + " is being added at index " + module_num
                        + " when only " + len(existing_lis) + " exist already"
                    )
                else:
                    existing_lis[module_num].insert_before(new_li)
            else:
                li_to_modify = existing_lis[module_num]
                if old_title not in li_to_modify.a.text:
                    raise Exception(
                        "Old module title of " + old_title + " not in module "
                        + "at index " + module_num + " in chapter "
                        + chapter_name
                    )
                li_to_modify.a.clear()
                i_tag = soup.new_tag("i")
                i_tag.string = new_title
                li_to_modify.a.append(i_tag)
            new_ul = str(soup.body)
            new_ul = new_ul.replace("<body>", "").replace("</body>", "")
            page["content"][index + 1]["content"] = new_ul
            return

    raise Exception(
        "Could not update table of contents page for new module title "
        + new_title + " at module index " + module_num + " in chapter "
        + chapter_name
    )

def update_list_of_pages_page_in_contents(
    part1_json, chapter_name, page_num, new_title, new_page=False,
    old_title=None, new_href=None
):
    """
    Update a "Pages **-**" page when adding a page/changing a page title.

    NOTE THAT AS CURRENTLY WRITTEN, this function only works with updates to
    page titles in the front matter, with the exception of the list of figures.
    Page titles in other chapters will be updated, but will be inconsistent
    with the original formatting for that chapter in List of Pages.

    Parameters
    ----------
    part1_json : dict
        A json file from running extraction on part 1, the "Contents" chapter.
    chapter_name : str
        Name of the chapter to update/add the page in.
    page_num : str
        The page number of the page that was inserted/modified.
    new_title : str
        The new title for the page that is being updated/added.
    new_page : Boolean
        If True, a new page was added; if False, an old one was changed.
    old_title : str
        The old title of the page that is being updated if new_page is set
        to False.
    new_href : str
        A href link to the section being created along with the new page if
        new_page is set to True.
    """
    if chapter_name not in ["Introduction", "Contents"]:
        raise Exception(
            'Error: updating the List of Pages for a page that is not in '
            'the "Introduction" or "Contents" chapter is not yet supported.'
        )

    # Get the right "Pages **-**" page in the List of Pages to update, and also
    # the section corresponding to it in case of page insertion.
    # NOTE: Will need significant refactoring if adding pages in Background
    # through Bibliography or in Appendix A needs to be done, as those pages
    # span multiple sections rather than being in just a single section.
    list_of_pages_page_num = ""
    section_to_change = None
    for outer_module in part1_json["modules"]:
        module = outer_module["module"]
        if module["fullTitle"] == "List of Pages":
            for section in module["sections"]:
                if "Pages i" in section["name"]:
                    list_of_pages_page_num = section["pageNum"]
                    section_to_change = section
                    break
            break
    page = part1_json["pages"][list_of_pages_page_num]
    
    if new_page:
        # Add a new page to the list of pages and bump up other page numbers.
        # Assumes the list of pages is properly ordered beforehand.
        index_to_insert = None
        largest_page_num = page_num
        for index, paragraph in enumerate(page["content"]):
            if f"Page {page_num}</" in paragraph["content"]:
                # Cannot change list during iteration, so save index for later
                index_to_insert = index
                break
        
        # Bump up other page numbers
        for i in range(index_to_insert, len(page["content"])):
            paragraph = page["content"][i]
            parts = paragraph["content"].split("Page ")
            current_page_num = parts[1].split("</", 1)[0]
            next_page_num = int_to_roman(roman_to_int(current_page_num) + 1)
            largest_page_num = next_page_num
            paragraph["content"] = (
                parts[0] + "Page " + next_page_num + "</"
                + parts[1].split("</", 1)[1]
            )
            # Handle the special case of missing page v from original site
            if next_page_num == 'v':
                if not "Page v</" in page["content"][i+1]["content"]:
                    largest_page_num = None
                    break

        # Insert the new page
        page["content"].insert(index_to_insert, {
            "type": "paragraph",
            "content": (
                f'<a href="{new_href}"><u>Page {page_num}</u></a>'
                + f'. {new_title}.'
            )
        })

        # Update the title of the "List of Pages" page if needed. Only time
        # this should not happen is when inserting a page before page v
        # for the first time.
        if largest_page_num:
            part1_json["pages"][list_of_pages_page_num]["pageTitle"] = (
                f"Pages i-{largest_page_num}"
            )
            section_to_change["name"] = f"Pages i-{largest_page_num}"
        return
    else:
        # Change the list of pages to use the new title for an existing page.
        for paragraph in page["content"]:
            if f"Page {page_num}</" in paragraph["content"]:
                if old_title not in paragraph["content"]:
                    existing_title = paragraph["content"].split("</a>.")[1]
                    print(
                        "Page num found, titles don't match. Expected: "
                        + old_title + ", Got: " + existing_title
                    )
                paragraph["content"] = (
                    paragraph["content"].split("</a>.")[0]
                    + f"</a>. {new_title}."
                )
                return

    raise Exception(
        "Could not update list of pages for page " + page_num
        + " in chapter " + chapter_name
        + ". New page inserted = " + new_page
    )

def update_json_obj_before_inserting_page_for_front_matter(
    json_collection, json_to_insert_num, chapter_name, page_num
):
    """
    Update the json obj(s) storing extracted data before inserting a new page.

    Parameters
    ----------
    json_collection : list
        A list of all the extracted json data objects that belong to the group
        of chapters that need to be updated all at once, properly ordered.
        Specifically, Background through References/Bibliography forms a
        collection, Introduction + Contents forms a collection, and all the
        other chapters each are considered a collection. Thus, when inserting a
        page in the front matter (Introduction + Contents), pass in the list
        [part0_json, part1_json].
    json_to_insert_num : int
        The index of the json within the json_collection list where the new
        page is being inserted.
    chapter_name : str
        The name of the chapter where the page is being inserted.
    page_num : str
        The page num of the page that is being inserted.
    """
    if chapter_name not in ["Introduction", "Contents"]:
        raise Exception(
            'Error: updating the json obj for a page that is not in '
            'the "Introduction" or "Contents" chapter is not yet supported.'
        )

    def update_section_pagenums(jsons, chapter_name, page_num):
        """
        Update the pageNums associated with each section in the jsons.
        """
        int_page_num = roman_to_int(page_num)
        for json in jsons:
            for outer_module in json["modules"]:
                module = outer_module["module"]
                for section in module["sections"]:
                    int_section_page_num = roman_to_int(section["pageNum"])
                    if int_section_page_num >= int_page_num:
                        section["pageNum"] = int_to_roman(
                            int_section_page_num + 1
                        )
                        # Deal with the special case of a missing page v
                        if (
                            chapter_name in ["Introduction", "Contents"]
                            and int_section_page_num == 4
                        ):
                            if not any(
                                "v" in _json["pages"]
                                for _json in jsons
                            ):
                                return

    def update_page_values(jsons, json_to_insert_num, page_num):
        """
        Update the page object for each page num in a json's pages dict.
        """
        current_page_num = page_num
        next_page_num = int_to_roman(roman_to_int(current_page_num) + 1)
        starting_json = jsons[json_to_insert_num]
        starting_json_index = json_to_insert_num
        if page_num not in starting_json["pages"]:
            # Leave the key empty and insert the page later, meanwhile
            # move on to the next json_obj
            starting_json["pages"][page_num] = None
            starting_json_index += 1
            if starting_json_index == len(jsons):
                return
            starting_json = jsons[starting_json_index]
            current_page_obj = starting_json["pages"][current_page_num]
            del starting_json["pages"][current_page_num]
        else:
            current_page_obj = starting_json["pages"][current_page_num]
        temp_page_obj = None
        # Unlike with updating the List of Pages page and the Table of Contents
        # page, the preference here is to not rely on the pages dict in a json
        # obj being ordered.
        for i in range(starting_json_index, len(jsons)):
            json = jsons[i]
            # Keep looping over json until all relevant page numbers updated
            while True:
                if next_page_num in json["pages"]:
                    temp_page_obj = json["pages"][next_page_num]
                    json["pages"][next_page_num] = current_page_obj
                    current_page_obj = temp_page_obj
                    current_page_num = next_page_num
                    next_page_num = int_to_roman(
                        roman_to_int(current_page_num) + 1
                    )
                elif (
                    i < len(jsons) - 1
                    and next_page_num in jsons[i + 1]["pages"]
                ):
                    temp_page_obj = jsons[i + 1]["pages"][next_page_num]
                    del jsons[i + 1]["pages"][next_page_num]
                    json["pages"][next_page_num] = current_page_obj
                    current_page_num = next_page_num
                    next_page_num = int_to_roman(
                        roman_to_int(current_page_num) + 1
                    )
                    current_page_obj = temp_page_obj
                    break
                else:
                    # Add a new page num key to the current json's pages dict,
                    # then have that key's value be the current page obj.
                    # Also handles the case of page v missing from original
                    # site.
                    json["pages"][next_page_num] = current_page_obj
                    return

    update_section_pagenums(json_collection, chapter_name, page_num)
    update_page_values(json_collection, json_to_insert_num, page_num)

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
    with (JSONS_DIR / 'started.json').open() as f:
        getting_started = json.load(f)

    # Insert page operations done at the end for consistency between page nums
    # NOTE: Always insert the "How to Cite" page as page ii first, so that the
    # missing page v in the front matter will be fixed.

    print("Updating edition and date on title page, page i... ...")
    edit_page_content(part0, "i", 0, "modify", "paragraph",
    """<center>\n\n<p><b><font size=\"+3\">Excavating Occaneechi Town</font><br/>\nArchaeology of an Eighteenth-Century Indian Village in North Carolina</b></p>\n\n<p>\n\n</p><p><i>Edited by</i><br/>\nR. P. Stephen Davis, Jr.<br/>\nPatrick C. Livingood<br/>\nH. Trawick Ward<br/>\nVincas P. Steponaitis\n\n</p><p><i>With contributions by</i><br/>\nLinda Carnes-McNaughton<br/>\nI. Randolph Daniel, Jr.<br/>\nRoy S. Dickens, Jr.<br/>\nLawrence A. Dunmore, III<br/>\nKristen J. Gremillion<br/>\nJulia E. Hammett<br/>\nForest Hazel<br/>\nMary Ann Holm<br/>\nJames H. Merrell<br/>\nGary L. Petherick<br/>\nV. Ann Tippitt\n\n</p><p>\n\n</p><p><b>Second Web Edition<br/>\n2021</b>\n\n</p></center>"""
    )

    print("Updating Patrick C. Livingood's initials in prefaces... ...")
    edit_page_content(part0, "iii", -1, "modify", "italic-title", "R.P.S.D., P.C.L., H.T.W., V.P.S.<br/>\nDecember 14, 1997")
    edit_page_content(part0, "iv", -1, "modify", "italic-title", "R.P.S.D., P.C.L., H.T.W., V.P.S.<br/>\nJuly 28, 2003")

    print("Updating titles of two original prefaces... ...")
    # Change title of "Preface to First Edition" to "Preface to CD-ROM Edition"
    update_page_title(part0, part1, "Introduction", "iii", "Preface to CD-ROM Edition")
    # Change "Preface to Web Edition" to "Preface to First Web Edition"
    update_page_title(part0, part1, "Introduction", "iv", "Preface to First Web Edition")

    print("Adding colophon, a.k.a. How to Cite page as page ii... ...")
    insert_page_and_module_in_front_matter(part1, [part0, part1], 0, 1, [{
        "type": "paragraph",
        "content": '<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">' +
                   '<img alt="Creative Commons License" style="border-width:0"  src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />' +
                   'This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.<br>'
    }, {
        "type": "paragraph",
        "content": """When citing this work, please include this information: <br>R. P. Stephen Davis Jr., Patrick C. Livingood, H. Trawick Ward, and Vincas P. Steponaitis, eds. <i>Excavating Occaneechi Town: Archaeology of an Eighteenth-Century Indian Village in North Carolina</i>. Chapel Hill: University of North Carolina Press, second web edition, last updated March 2021. DOI 10.5149/9781469666310_Davis."""
    }, {
        "type": "paragraph",
        "content": """© 1998 Research Laboratories of Archaeology, University of North Carolina at Chapel Hill"""
    }, {
        "type": "paragraph",
        "content": """Preface to First Web Edition © 2003 Research Laboratories of Archaeology, University of North Carolina at Chapel Hill"""
    }, {
        "type": "paragraph",
        "content": """Preface to Second Web Edition © 2021 Research Laboratories of Archaeology, University of North Carolina at Chapel Hill"""
    }, {
        "type": "paragraph",
        "content": """<i>Excavating Occaneechi Town</i> was originally published as a CD-ROM by the University of North Carolina Press in 1998. Its first web edition went live in 2003. The second web edition was published in 2021."""
    }, {
        "type": "paragraph",
        "content": """ISBN 9781469666310"""
    }], "Introduction", "How to Cite", "How to Cite", "/html/part0/newbody1.html", "/html/part0/newtab1.html", author=None)
    
    print(
        "Adding Preface to Second Web Edition as new module at end of "
        "the Introduction chapter... ..."
    )
    insert_page_and_module_in_front_matter(part1, [part0, part1], 0, 5, [{
        "type": "paragraph",
        "content": """<i>Excavating Occaneechi Town</i> has come a long way since it was conceived and published in the 1990s. As detailed in the prefaces to previous editions, it first appeared in 1998 as a CD-ROM, UNC Press’s first electronic monograph. Innovative for its time, this edition was honored with an Electronic Product Award from the American Association of Publishers. The monograph later migrated to a website, which went live in 2003. The new version maintained the same content as its predecessor and was meant to increase the monograph’s longevity and reach, a set of goals it accomplished. However, over the years since the first web edition appeared, the landscape of digital delivery has changed dramatically, necessitating the second web edition presented here."""
    }, {
        "type": "paragraph",
        "content": """Two extraordinary teams of undergraduate students at the University of North Carolina at Chapel Hill undertook the redesign of <i>Excavating Occaneechi Town</i> for a course called “Software Engineering Lab.” In 2018, Micah Anderson, Tom Boyd, Trey Hayes, and Conrad Ma created the new Electronic Dig. And, in 2020, Andy Chen, Jacob King, and Ankush Vij designed the new look for the rest of the monograph and wrote the code that translated the old pages into their current format. Their skill and dedication are well reflected in the quality of the current edition."""
    }, {
        "type": "paragraph",
        "content": "As new security features were added to internet browsers, vulnerabilities associated with the Java programming of the 2003 version of Electronic Dig made it ever more difficult to run; eventually, it stopped working entirely. Anderson, Boyd, Hayes, and Ma created a new version of the app, starting from scratch and using a WAMP software bundle. The new Electronic Dig replicates the key features of the earlier versions, albeit with a somewhat different, tablet-friendly design. Given the inevitability of future changes in operating systems and browsers, it is hard to predict how long this new app will remain functional, as apps tend to be much more sensitive to such changes than simple web pages are. That said, we take some comfort in knowing that Electronic Dig is a tool for teaching, not for research. It serves as a useful addition but is not essential to the website as a scholarly resource."
    }, {
        "type": "paragraph",
        "content": "The HTML pages used in the first web edition became less visually attractive and more difficult to use as screen resolutions increased and digital platforms proliferated. The original web version was designed for VGA monitors that displayed only 640 x 480 pixels, less than half the resolution of most computer screens today, and the page layout did not anticipate the central role tablets and smart phones now play in accessing web content. Chen, King, and Vij completely redesigned the website to accommodate this new digital environment. The current website uses CSS and JavaScript — technologies that have advanced significantly since 2003 — to create dynamic pages that automatically adapt to the reader’s device. It also includes new, scalable excavation maps and drawings, as well as higher-resolution versions of the original field and artifact photographs. Apart from these design changes and fixing a few minor bugs, the second web edition is essentially the same in both content and pagination as its predecessors."
    }, {
        "type": "paragraph",
        "content": "Our thanks go not only to these students for their excellent work but also to their professors, Diane Pozefsky and Jeff Terrell, who allowed us to take part in their course. We are also grateful to John Sherer, Iris Levesque, Ellen Bush, and Dino Battista at UNC Press for their help and encouragement in bringing this new edition to publication and to Elaine Westbrooks and Tim Shearer at UNC Libraries for giving this electronic publication a digital home."
    }, {
        "type": "paragraph",
        "content": "R.P.S.D., P.C.L., V.P.S. <br>February 7, 2021"
    }], "Introduction", "Preface to Second Web Edition", "Preface to Second Web Edition", "/html/part0/newbody5.html", "/html/part0/newtab5.html", author=None)

    print("Updating Getting Started page with hardcoded new content... ...")
    edit_page_content(getting_started, "GS2", 4, "modify", "paragraph", """This chapter includes the front matter of this electronic book: <a href=\"/html/part0/tab0.html\"><i>Title Page</i></a>, <a href=\"/html/part0/newtab1.html\"><i>How to Cite</i></a>, <a href=\"/html/part0/tab1.html\"><i>Foreword</i></a>, <a href=\"/html/part0/tab2.html\"><i>Preface to CD-ROM Edition</i></a>, <a href=\"/html/part0/tab3.html\"><i>Preface to First Web Edition</i></a>, and <a href=\"/html/part0/newtab5.html\"><i>Preface to Second Web Edition</i></a>.""")

    # Write edited file(s) back to disk
    UPDATED_JSON_OUTPUT_DIR = JSONS_DIR / "updated"
    UPDATED_JSON_OUTPUT_DIR.mkdir(exist_ok=True)
    with open(UPDATED_JSON_OUTPUT_DIR / 'part0.json', 'w') as f:
        json.dump(part0, f, indent=4)
    with open(UPDATED_JSON_OUTPUT_DIR / 'part1.json', 'w') as f:
        json.dump(part1, f, indent=4)
    with open(UPDATED_JSON_OUTPUT_DIR / 'started.json', 'w') as f:
        json.dump(getting_started, f, indent=4)
