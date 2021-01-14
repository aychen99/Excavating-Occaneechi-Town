# Test hyperlinks in HTML pages that are generated.
# Cases include but may not be limited to:
# - regular hyperlink (relative link, not absolute link)
#   - link to another HTML page
#   - link to an external site
#   - link to a file, e.g. in /video or /dataForDownload
#   - Excavations and Appendix A links
# - Pagination button
# - <a> tags that rely on JavaScript for functionality
#   - LightGallery link (wrapper for a <figure> in carousels or text)
#   - Citation link
#   - Table link
#   - Video link
#   - Archaeology Primer image toggling link

import logging
import json
import pathlib
from bs4 import BeautifulSoup


if __name__ == "__main__":
    # Change level to logging.INFO for all potential problem messages,
    # and logging.ERROR for only error messages without additional info
    logging.basicConfig(
        filename='hyperlink_checks.log', filemode='w', level=logging.INFO
    )
    script_root_dir = pathlib.Path(__file__).parent
    # Use config.json to decide where to look.
    with open(script_root_dir / "config.json") as f:
        config = json.load(f)
    
    newdigdir = config['generationOutputDirPath']
    if newdigdir == 'Default':
        newdigdir = script_root_dir / "newdig"
    elif pathlib.Path(newdigdir).exists:
        newdigdir = pathlib.Path(newdigdir)
    else:
        raise Exception("Directory for generated new site does not exist.")

    for page in newdigdir.glob('**/*.html'):
        logging.info("Reading: " + str(page))
        with open(page, 'r') as f:
            page_str = f.read()
        soup = BeautifulSoup(page_str, 'html5lib')
        anchors = soup.find_all('a')
        for a in anchors:
            if (
                a.has_attr('class')
                and any(
                    c in a['class'] 
                    for c in ['a-img', 'a-ref', 'a-table', 'a-video']
                )
            ):
                # Dynamic anchor relying on JavaScript to do anything properly
                # Additional attribute values inserted in process_content.py
                if 'a-img' in a['class']:
                    # Loads with LightGallery according to load-modals.js
                    for attr in ['href', 'data-src', 'data-sub-html']:
                        if not a.has_attr(attr):
                            logging.error(
                                'No ' + attr + ' in a-img ' + str(a)
                            )
                    continue
                elif 'a-ref' in a['class']:
                    # Loads a references modal according to load-modals.js
                    for attr in [
                        'href', 'data-target', 'data-author', 'data-ref-text'
                    ]:
                        if not a.has_attr(attr):
                            logging.error(
                                'No ' + attr + ' in a-ref ' + str(a)
                            )
                    if (
                        not a.has_attr('data-toggle')
                        or not a['data-toggle'] == 'modal'
                    ):
                        logging.error(
                            'No data-toggle for modal set in ' + str(a)
                        )
                    continue
                elif 'a-table' in a['class']:
                    # Loads a table modal according to load-modals.js
                    for attr in [
                        'href', 'data-target',
                        'data-table-header', 'data-table-string'
                    ]:
                        if not a.has_attr(attr):
                            logging.error(
                                'No ' + attr + ' in a-table ' + str(a)
                            )
                    if (
                        not a.has_attr('data-toggle')
                        or not a['data-toggle'] == 'modal'
                    ):
                        logging.error(
                            'No data-toggle for modal set in ' + str(a)
                        )
                    continue
                elif 'a-video' in a['class']:
                    # Loads a YouTube video modal according to load-modals.js
                    for attr in [
                        'href', 'data-target',
                        'data-figure-path', 'data-figure-caption'
                    ]:
                        if not a.has_attr(attr):
                            logging.error(
                                'No ' + attr + ' in a-video ' + str(a)
                            )
                    if (
                        not a.has_attr('data-toggle')
                        or not a['data-toggle'] == 'modal'
                    ):
                        logging.error(
                            'No data-toggle for modal set in ' + str(a)
                        )
                    continue

            if a.find_parent('pre'):
                # Should be an image link in Table 3 or 4
                for attr in [
                    'href', 'data-src', 'data-sub-html', 'data-thumbnail'
                ]:
                    if not a.has_attr(attr):
                        logging.error(
                            'No ' + attr + ' in image anchor ' + str(a)
                        )
                continue

            if (
                a.find_parent(id='text-chapter-contents')
                and a.find_parent('ul')
                and not a.find_parent('nav')
                and any(
                    page in soup.find(id='pageNumClickable').text
                    for page in ['AP13', 'AP14', 'AP23']
                )
            ):
                # Is a link in page 13, 14, or 23 of the Archaeology Primer
                # that serves to change the current image being displayed on
                # the page instead of redirecting or opening a modal.
                for attr in ['data-image-caption', 'data-image-path']:
                    if not a.has_attr(attr):
                        logging.error(
                            'No ' + attr + ' in a-img ' + str(a)
                        )
                if (
                    not a.has_attr('href')
                    or not a['href'] == 'javascript:void(0);'
                ):
                    logging.error(
                        'href of image toggle anchor in Archaeology Primer '
                        + 'is not set to javascript:void(0); at ' + str(a)
                    )
                continue

            if a.has_attr('id') and a['id'] == 'pageNumClickable':
                # Button allowing you to go to any page number
                # Automatic pass
                continue

            if a.has_attr('href'):
                href = a['href']
                if 'https://' in href:
                    # Link to external site
                    if not 'https://electronicdig.sites.oasis.unc.edu' in href:
                        # The site links to both the Electronic Dig main page
                        # and also to /views/tutorial1.html in
                        # the Table of Contents
                        logging.error(
                            'Found non-electronic dig external site ' + href
                        )
                    continue
                elif href == '#':
                    # Should only be seen in index.html
                    logging.warning(
                        'Scrolls to top and does nothing else: ' + str(a)
                    )
                    continue
                elif href == '#genModal':
                    # Should have already been covered by has_attr('class')
                    logging.error(
                        'anchor tag points to #genModal but does not have '
                        + 'a proper "dynamic" class: ' + str(a)
                    )
                elif href == '#carouselFigures':
                    # Button for switching between images in a carousel in
                    # Excavations.
                    # Automatic pass
                    continue
                elif href == '#versionModal':
                    # Opens up the Instructional vs Professional
                    # version disclaimer
                    if (
                        not (a.has_attr('data-toggle')
                             and a['data-toggle'] == 'modal')
                        or not (a.has_attr('data-target')
                                and a['data-target'] == '#versionModal')
                    ):
                        logging.error(
                            'Version modal anchor tag missing a required '
                            + 'attribute: ' + str(a)
                        )
                elif (page.parent / href).exists():
                    continue
                else:
                    logging.error(
                        'Non-existent path in anchor ' + str(a)
                    )
            else:
                logging.error('Bad anchor tag: ' + str(a))
