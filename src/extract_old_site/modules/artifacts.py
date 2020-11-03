from bs4 import BeautifulSoup
import pathlib
import os

# Functions for /dig/html/artifacts
def extract_artifacts_image(html_string):
    """Get all information from an img.html in the artifacts folder."""
    soup = BeautifulSoup(html_string, 'html5lib')
    path = pathlib.Path("/dig/html/artifacts") / soup.body.img['src']
    path = str(pathlib.Path(os.path.normpath(path)).as_posix())
    soup.body.center.a.decompose()
    figure_num_and_caption = soup.body.center.text.strip().split('.', 1)
    figure_num = figure_num_and_caption[0].replace("Figure", "").strip()
    caption = figure_num_and_caption[1].strip()

    return {
        "path": path,
        "figureNum": figure_num,
        "caption": caption
    }

def extract_all_artifacts_images(dig_parent_dir, readfile):
    """Get info from all img.html pages in the artifacts folder."""
    artifacts_dir = pathlib.Path(dig_parent_dir) / "dig/html/artifacts"
    images = {}
    for filename in artifacts_dir.iterdir():
        if 'img' in filename.name:
            html_string = readfile(filename.name, filename.parent)
            image = extract_artifacts_image(html_string)
            images[filename.name] = image
    return images

def extract_excavation_zones(html_string, dig_parent_dir):
    """Extract the list of zones with artifacts from the ctrl_**.html page."""
    # TODO: Get the Appendix A page number

    soup = BeautifulSoup(html_string, 'html5lib')
    exc_element_name = soup.body.center.b.text.strip()
    links = soup.table.find_all('tr')
    artifacts_dir = pathlib.Path("/dig/html/artifacts")
    parent_exc_page = str(pathlib.Path(os.path.normpath(artifacts_dir / links[0].a['href'])).as_posix())
    
    soup.table.clear()
    zone_a_tags = soup.body.find_all('a')
    zones = []
    for a_tag in zone_a_tags:
        zones.append({
            "name": a_tag.text.strip(),
            "pageName": a_tag['href']
        })

    return {
        "excavationElement": exc_element_name,
        "parentExcPage": parent_exc_page,
        "zones": zones
    }

def extract_artifacts_list(html_string, dig_parent_dir):
    """Extract a list of artifacts from a info_***.html page."""
    soup = BeautifulSoup(html_string, 'html5lib')
    artifact_trs = soup.table.find_all('tr')
    ths = artifact_trs.pop(0).find_all('th')
    fields = []
    for th in ths:
        fields.append(th.text.strip())

    artifacts_dir = pathlib.Path("/dig/html/artifacts")
    artifacts = []
    for tr in artifact_trs:
        tds = tr.find_all('td')
        artifact = {}
        for i in range(0, len(fields)):
            value = tds[i].text.strip()
            if tds[i].a:
                value = str(pathlib.Path(os.path.normpath(artifacts_dir / tds[i].a['href'])).as_posix())
            if value == '':
                value = None
            artifact[fields[i]] = value
        artifacts.append(artifact)

    return artifacts

def extract_art_html_page(html_string, dig_parent_dir, readfile):
    """Extract all info from a art_***.html page."""
    artifacts_dir = pathlib.Path(dig_parent_dir) / "dig/html/artifacts"
    soup = BeautifulSoup(html_string, 'html5lib')
    frames = soup.find_all('frame')
    ctrl_html_string = readfile(frames[0]['src'], artifacts_dir)

    ctrl_extracted = extract_excavation_zones(ctrl_html_string, dig_parent_dir)
    for zone in ctrl_extracted['zones']:
        zone_artifacts_html_string = readfile(zone['pageName'], artifacts_dir)
        artifacts = extract_artifacts_list(zone_artifacts_html_string, dig_parent_dir)
        zone['artifacts'] = artifacts

    return ctrl_extracted

def extract_all_of_artifacts_dir(dig_parent_dir, readfile):
    """Extract all artifacts info (but not images) from /dig/html/artifacts.
    
    Returns a dictionary of excavation elements' old home pages (e.g.
    /dig/html/excavations/exc_aa.html) to the summary info for the
    artifacts contained in them."""
    artifacts = {}
    artifacts_dir = pathlib.Path(dig_parent_dir) / "dig/html/artifacts"

    # Ensure that similarly named files like art_aa0.html or art_aa1.html
    # and art_ab0.html or art_ab2.html are extracted only once.
    dict_by_letters = {}
    for filename in artifacts_dir.iterdir():
        if 'art' in filename.name:
            letters = filename.name.split('_')[1][0:2]
            if letters not in dict_by_letters:
                dict_by_letters[letters] = filename.name
    
    for filename in dict_by_letters.values():
        html_string = readfile(filename, artifacts_dir)
        extracted = extract_art_html_page(html_string, dig_parent_dir, readfile)
        artifacts[extracted['parentExcPage']] = extracted
    return artifacts

# Functions for /dig/html/dbs
def extract_db_frame(html_string):
    """Extract artifact details from a db*_*.html frame in appendix B."""
    soup = BeautifulSoup(html_string, 'html5lib')
    trs = soup.body.table.find_all('tr')
    ths = trs.pop(0).find_all('th')
    fields = []
    for th in ths:
        fields.append(th.text.strip())

    artifacts = []
    for tr in trs:
        tds = tr.find_all('td')
        artifact = {}
        for i in range(0, len(fields)):
            value = tds[i].text.strip()
            if value == '':
                value = None
            artifact[fields[i]] = value
        artifacts.append(artifact)
    return artifacts

def extract_appendix_b_page(page_num, dig_parent_dir, readfile):
    """Extract the detailed list of artifacts for a given appendix B page."""
    # Makes an assumption, already tested elsewhere, that for a given number x,
    # dbx_*.html all belong to the same page in Appendix B.
    dbs_path_obj = pathlib.Path(dig_parent_dir) / "dig/html/dbs"
    name = BeautifulSoup(readfile("head" + str(page_num) + ".html", dbs_path_obj),
                         'html5lib').i.string
    artifacts = []
    for filename in dbs_path_obj.iterdir():
        if "db" + str(page_num) in filename.name:
            artifacts += extract_db_frame(readfile(filename.name, filename.parent))

    return {
        "name": name,
        "pageNum": page_num,
        "artifacts": artifacts
    }

def extract_appendix_b(dig_parent_dir, readfile):
    """Extract all artifact details from all page*.html files."""
    artifacts = {}
    # Hard-coded total of 7 appendix B pages.
    for i in range(0,7):
        print("    Extracting appendix B pg. " + str(i+1))
        extracted_page = extract_appendix_b_page(i, dig_parent_dir, readfile)
        artifacts[extracted_page['name']] = extracted_page
    return artifacts

# Functions for processing extracted data
def generate_cat_num_to_artifacts_dict(artifacts_summary=None, artifacts_details=None, append=False):
    """Make a dict of cat nums to artifacts from a dictionary of artifacts.
    
    The artifacts_summary parameter is the result of calling
    extract_all_of_artifacts_dir. The artifacts_details parameter is the result
    of calling extract_appendix_b.
    """
    all_artifacts = {}
    if artifacts_details:
        for art_category in artifacts_details.values():
            for artifact in art_category['artifacts']:
                cat_no = artifact['Catalog No.']
                if cat_no not in all_artifacts:
                    all_artifacts[cat_no] = {
                        "details": [],
                        "appendixBPageNum": art_category['pageNum'],
                        "zoneNum": None,
                        "parentExcPage": None
                    }
                if append:
                    all_artifacts[cat_no]['details'].append(artifact)

    if artifacts_summary:
        for exc_element in artifacts_summary.values():
            for zone in exc_element['zones']:
                for artifact in zone['artifacts']:
                    cat_no = artifact['Cat. No.']
                    if cat_no not in all_artifacts:
                        all_artifacts[cat_no] = {
                            "details": None,
                            "appendixBPageNum": None
                        }
                    summary = None
                    if append:
                        summary = artifact
                    all_artifacts[cat_no].update({
                        "summary": summary,
                        "zoneNum": exc_element['zones'].index(zone),
                        "parentExcPage": exc_element['parentExcPage']
                    })
    
    return all_artifacts

def insert_details_into_summary_dict(artifacts_summary, artifacts_by_cat_no):
    """Put in info from Appendix B into the artifacts by exc element dict.
    
    Currently mutates the original artifacts by exc element dict."""
    for exc_element in artifacts_summary.values():
        for zone in exc_element['zones']:
            for artifact in zone['artifacts']:
                cat_no = artifact['Cat. No.']
                artifact['details'] = artifacts_by_cat_no[cat_no]['details']
    return artifacts_summary

# Functions for validating input/output
def validate_artifacts_images_with_excavations(artifacts_images, excavations_images):
    """Check that excavations and artifacts image files have the same info."""
    all_same = True
    for path, art_img in artifacts_images.items():
        exc_img = excavations_images[path]
        for field in ['path', 'figureNum', 'caption']:
            if art_img[field] != exc_img[field]:
                all_same = False
                print("Not the same: " + str(art_img) + "\n" + str(exc_img))
    return all_same

def validate_same_art_page_letter_extraction(dig_parent_dir, readfile):
    """Check that all art_xx**.html files provide the same extracted info."""
    artifacts_dir = pathlib.Path(dig_parent_dir) / "dig/html/artifacts"

    dict_by_letters = {}
    for filename in artifacts_dir.iterdir():
        if 'art' in filename.name:
            letters = filename.name.split('_')[1][0:2]
            if letters not in dict_by_letters:
                dict_by_letters[letters] = []
            dict_by_letters[letters].append(filename.name)
    
    all_art_files_same_info = True
    for filename_list in dict_by_letters.values():
        all_same_info = True
        baseline_soup = BeautifulSoup(readfile(filename_list[0], artifacts_dir), 'html5lib')
        baseline_ctrl = baseline_soup.find_all('frame')[0]['src']
        zones = extract_excavation_zones(readfile(baseline_ctrl, artifacts_dir), dig_parent_dir)
        zones = zones['zones']
        info_pagenames = set()
        for zone in zones:
            info_pagenames.add(zone['pageName'])
        for filename in filename_list:
            soup = BeautifulSoup(readfile(filename, artifacts_dir), 'html5lib')
            frames = soup.find_all('frame')
            letter_num = filename.split('_')[1].split('.')[0]
            if (frames[0]['src'] != baseline_ctrl
                    or frames[1]['src'].split('_')[1].split('.')[0] != letter_num
                    or frames[1]['src'] not in info_pagenames):
                all_same_info = False
        all_art_files_same_info = all_art_files_same_info and all_same_info
    
    return all_art_files_same_info
