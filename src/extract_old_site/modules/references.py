from bs4 import BeautifulSoup, NavigableString
from pathlib import Path

def extract_references_page(html_string):
    """Extract the references in report282b, 283b, or 284b.html.

    Keeps any double spaces present in the original reference, as well as <i>
    and other minor HTML tags.
    """
    # Add in extra <p> tags to make parsing easier
    html_string = html_string.replace("<blockquote>", "<blockquote><p>")
    # Fix the two broken refs of McCollough et al. and MacCord
    html_string = html_string.replace("Lenhardt<p>", "Lenhardt<blockquote><p>")
    soup = BeautifulSoup(html_string, 'html5lib')
    references = {}
    hrefs_to_refs = {}

    i = 0
    contents = soup.body.contents
    while i < len(contents):
        author = None
        author_refs = None
        if i < len(contents) - 1 and contents[i+1].name == "blockquote":
            content = contents[i]
            if content.name == "a":
                if i == len(contents) - 1:
                    raise Exception("Found an <a> tag in references, but it was "
                                    "the very last element in the page.")
                author = content.text.strip()
                author_refs = contents[i+1]
                hrefs_to_refs[content['name']] = {"author": author, "refNum": 0}
            elif isinstance(content, NavigableString):
                author = str(content).strip()
                author_refs = contents[i+1]
            else:
                raise Exception("Found an element right before a blockquote"
                                + "that is not a NavigableString or an <a> "
                                + "tag, " + str(content))

        if author:
            extracted_refs = []
            for ref in author_refs: # ref here refers to a <p> tag in the soup
                # Remove empty <p> tags
                if ref.text and ref.text.strip() == '':
                    continue

                a_name = None
                if ref.a:
                    a_name = ref.a['name']
                    ref.a.replace_with(ref.a.string)
                    hrefs_to_refs[a_name] = {
                        "author": author,
                        "refNum": len(extracted_refs)
                    }
                extracted_refs.append(
                    str(ref).replace('<p>', '')
                            .replace('</p>', '')
                            .replace('\n', ' ')
                            .strip()
                )

            references[author] = extracted_refs

        i += 1

    return {"refs": references, "hrefsToRefs": hrefs_to_refs}

def extract_all_references(dig_parent_dir, readfile):
    """Extract all references A-Z from the site."""
    dig_parent_path_obj = Path(dig_parent_dir)
    extracted = {"refs": {}, "hrefsToRefs": {}}
    for split_page_num in [282, 283, 284]:
        split_page_dir = dig_parent_path_obj / "dig/html/split"
        refs_html = readfile(
            "report" + str(split_page_num) + "b.html", split_page_dir
        )
        data = extract_references_page(refs_html)
        extracted['refs'].update(data['refs'])
        extracted['hrefsToRefs'].update(data['hrefsToRefs'])

    return extracted
