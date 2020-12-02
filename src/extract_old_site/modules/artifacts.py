from bs4 import BeautifulSoup
import pathlib
import os

# Functions for /dig/html/artifacts
def extract_artifacts_image(html_string):
    """Get all information from an img.html in the artifacts folder."""
    soup = BeautifulSoup(html_string, 'html5lib')
    path = pathlib.Path("/html/artifacts") / soup.body.img['src']
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

def extract_all_artifacts_images(dig_dir_str, readfile):
    """Get info from all img.html pages in the artifacts folder."""
    artifacts_dir = pathlib.Path(dig_dir_str) / "html/artifacts"
    images = {}
    for filename in artifacts_dir.iterdir():
        if 'img' in filename.name:
            html_string = readfile(filename.name, filename.parent)
            image = extract_artifacts_image(html_string)
            images[filename.name] = image
    return images

def extract_excavation_zones(html_string):
    """Extract the list of zones with artifacts from the ctrl_**.html page."""
    # TODO: Get the Appendix A page number

    soup = BeautifulSoup(html_string, 'html5lib')
    exc_element_name = soup.body.center.b.text.strip()
    appendix_a_page_num = str(soup.body.center).split("Page ")[-1].replace("<br/></center>", "")
    if appendix_a_page_num == "?":
        # Hotfix for art_ir0.html, associated with /dig/html/excavations/exc_ir.html
        appendix_a_page_num = "224"
    links = soup.table.find_all('tr')
    artifacts_dir = pathlib.Path("/html/artifacts")
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
        "appendixAPageNum": appendix_a_page_num,
        "zones": zones
    }

def extract_artifacts_list(html_string):
    """Extract a list of artifacts from a info_***.html page."""
    soup = BeautifulSoup(html_string, 'html5lib')
    artifact_trs = soup.table.find_all('tr')
    ths = artifact_trs.pop(0).find_all('th')
    fields = []
    for th in ths:
        fields.append(th.text.strip())

    artifacts_dir = pathlib.Path("/html/artifacts")
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

def extract_art_html_page(html_string, dig_dir_str, readfile):
    """Extract all info from a art_***.html page."""
    artifacts_dir = pathlib.Path(dig_dir_str) / "html/artifacts"
    soup = BeautifulSoup(html_string, 'html5lib')
    frames = soup.find_all('frame')
    ctrl_html_string = readfile(frames[0]['src'], artifacts_dir)

    ctrl_extracted = extract_excavation_zones(ctrl_html_string)
    for zone in ctrl_extracted['zones']:
        zone_artifacts_html_string = readfile(zone['pageName'], artifacts_dir)
        artifacts = extract_artifacts_list(zone_artifacts_html_string)
        zone['artifacts'] = artifacts

    return ctrl_extracted

def extract_all_of_artifacts_dir(dig_dir_str, readfile):
    """Extract all artifacts info (but not images) from /dig/html/artifacts.

    Returns a dictionary of excavation elements' old home pages (e.g.
    /dig/html/excavations/exc_aa.html) to the summary info for the
    artifacts contained in them."""
    artifacts = {}
    artifacts_dir = pathlib.Path(dig_dir_str) / "html/artifacts"

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
        extracted = extract_art_html_page(html_string, dig_dir_str, readfile)
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

    artifacts = {"artifacts": [], "fields": fields}
    for tr in trs:
        tds = tr.find_all('td')
        artifact = {}
        for i in range(0, len(fields)):
            value = tds[i].text.strip()
            if value == '':
                value = None
            artifact[fields[i]] = value
        artifacts["artifacts"].append(artifact)
    return artifacts

def extract_appendix_b_page(page_num, dig_dir_str, readfile):
    """Extract the detailed list of artifacts for a given appendix B page."""
    # Makes an assumption, already tested elsewhere, that for a given number x,
    # dbx_*.html all belong to the same page in Appendix B.
    dbs_path_obj = pathlib.Path(dig_dir_str) / "html/dbs"
    name = BeautifulSoup(readfile("head" + str(page_num) + ".html", dbs_path_obj),
                         'html5lib').i.string
    artifacts = []
    fields = None
    for filename in dbs_path_obj.iterdir():
        if "db" + str(page_num) in filename.name:
            extracted_frame = extract_db_frame(readfile(filename.name, filename.parent))
            artifacts += extracted_frame["artifacts"]
            fields = extracted_frame["fields"]

    return {
        "name": name,
        "pageNum": str(page_num),
        "artifacts": artifacts,
        "fields": fields
    }

def extract_appendix_b(dig_dir_str, readfile):
    """Extract all artifact details from all page*.html files."""
    artifacts = {}
    # Hard-coded total of 7 appendix B pages.
    for i in range(0,7):
        print("    Extracting appendix B pg. " + str(i+1))
        extracted_page = extract_appendix_b_page(i, dig_dir_str, readfile)
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
                        "detailsFieldOrder": art_category["fields"],
                        "appendixBPageNum": art_category['pageNum'],
                        "zoneNum": None,
                        "parentExcPage": None,
                        "summary": None
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
                            "detailsFieldOrder": None,
                            "appendixBPageNum": None
                        }
                    if 'More' in artifact:
                        if artifact['More']:
                            appendix_b_page_num = artifact['More'].split('/page')[1].split('.')[0]
                            if (all_artifacts[cat_no]['appendixBPageNum']
                                and all_artifacts[cat_no]['appendixBPageNum'] != appendix_b_page_num
                            ):
                                pass
                                # print("Discrepancy found for " + cat_no)
                            else:
                                all_artifacts[cat_no]['appendixBPageNum'] = appendix_b_page_num
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
                artifact['detailsFieldOrder'] = artifacts_by_cat_no[cat_no]['detailsFieldOrder']
    return artifacts_summary

def replace_figure_paths_with_nums_in_summary_dict(artifacts_summary, artifacts_images):
    # Also currently mutates the original artifacts by exc element dict.
    for exc_element in artifacts_summary.values():
        for zone in exc_element['zones']:
            for artifact in zone['artifacts']:
                if artifact["Photo"]:
                    figure_num = artifacts_images[artifact["Photo"].split('/')[-1]]["figureNum"]
                    artifact["Photo"] = figure_num
    return artifacts_summary
