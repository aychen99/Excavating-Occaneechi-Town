from bs4 import BeautifulSoup
import pathlib

def extract_references_page(html_string):
    """Extract the references in report282b, 283b, or 284b.html."""
    # Add in extra <p> tags to make parsing easier
    html_string = html_string.replace("<blockquote>", "<blockquote><p>")
    soup = BeautifulSoup(html_string, 'html5lib')
    references = {}
    hrefs_to_refs = {}

    i = 0
    contents = soup.body.contents
    while i < len(contents):
        content = contents[i]
        if content.name == "a":
            author = content.text.strip()
            hrefs_to_refs[content['name']] = {"author": author, "refNum": 0}
            refs = []

            author_refs = None
            if i == len(contents) - 1:
                raise Exception("Found an <a> tag in references, but it was "
                                "the very last element in the page.")
            else:
                author_refs = contents[i+1]
            for ref in author_refs:
                # Remove empty <p> tags
                if ref.text and ref.text.strip() == '':
                    continue

                a_name = None
                if ref.a:
                    a_name = ref.a['name']
                    ref.a.replace_with(ref.a.string)
                    hrefs_to_refs[a_name] = {"author": author, "refNum": len(refs)}
                refs.append(str(ref).replace('<p>', '').replace('</p>', '').replace('\n', ' ').strip())

            references[author] = refs
        i += 1

    return {"refs": references, "hrefsToRefs": hrefs_to_refs}

def extract_all_references(dig_parent_dir, readfile):
    """Extract all references A-Z from the site."""
    dig_parent_path_obj = pathlib.Path(dig_parent_dir)
    extracted = {"refs": {}, "hrefsToRefs": {}}
    for split_page_num in [282, 283, 284]:
        split_page_dir = dig_parent_path_obj / "dig/html/split"
        refs_html = readfile("report" + str(split_page_num) + "b.html", split_page_dir)
        data = extract_references_page(refs_html)
        extracted['refs'].update(data['refs'])
        extracted['hrefsToRefs'].update(data['hrefsToRefs'])

    return extracted

def validate_ref_page(html_string, filename, dig_parent_dir, readfile):
    """Validate that a ref_**.html page links to the right ref."""
    soup = BeautifulSoup(html_string, 'html5lib')
    body_pagename = soup.find_all('frame')[1]['src']
    if body_pagename.replace('body', 'ref') != filename:
        print("body.html did not match up for: " + filename)
        return False
    
    body_html = readfile(body_pagename, pathlib.Path(dig_parent_dir) / "dig/html/part6")
    soup = BeautifulSoup(body_html, 'html5lib')
    report_pagename = soup.find_all('frame')[1]['src'].split('/')[-1]
    href_code = filename.split('_')[1].split('.')[0]
    if report_pagename.split('#')[-1] != href_code:
        print("report.html did not match up for: " + filename)
        return False
    elif not any (name == report_pagename.split('#')[0] 
                  for name in ['report282b.html', 'report283b.html', 'report284b.html']):
        print("Found " + report_pagename.split('#')[0] + " where a report.html was expected.")
        return False

    return True

def validate_all_ref_pages(dig_parent_dir, readfile):
    """Validate that all ref_**.html pages in part6 have correct links."""
    all_correct = True
    for filename in (pathlib.Path(dig_parent_dir) / "dig/html/part6").iterdir():
        if 'ref' in filename.name:
            ref_page_html = readfile(filename.name, filename.parent)
            all_correct = all_correct and validate_ref_page(ref_page_html, filename.name,
                                                            dig_parent_dir, readfile)
    return all_correct
