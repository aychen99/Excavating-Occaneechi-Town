from bs4 import BeautifulSoup
import pathlib
import os
from .path_ops import rel_path


def update_text_paragraph(paragraph_string, index, page_obj_path):
    """Update the <a> tags in a textpage/feature description paragraph."""
    # Map of video names to YouTube links, placed here for now
    mapToYouTube = {
        "plowzone": "https://www.youtube.com/embed/fXlnTa9_k90",
        "pits": "https://www.youtube.com/embed/Hj4lMnb6Q0s",
        "discover": "https://www.youtube.com/embed/P_dqJEv6Vds",
        "disease": "https://www.youtube.com/embed/Hx7EIN8tMh8",
        "feature": "https://www.youtube.com/embed/_XsDY8Po_I8",
        "trowel": "https://www.youtube.com/embed/8kkF2YceTd4",
        "wtrscrn": "https://www.youtube.com/embed/UJIQ3XuX8EA"
    }

    # Change innerHTML content of each section/paragraph
    # so that links (e.g. image and references) are updated.
    # TODO: if there is time, find a less redundant way of storing the info
    # for images, tables, and references than directly in the anchor tag.
    soup = BeautifulSoup(paragraph_string, 'html5lib')
    for a in soup.find_all('a'):
        old_path = a['href']
        if a.has_attr('data-is-primer') and a['data-is-primer'] == 'yes':
            del a['data-is-primer']
            old_path = pathlib.Path('/html/primer') / old_path
            old_path = os.path.normpath(old_path)
            old_path = pathlib.Path(old_path).as_posix()
            video_name = old_path.split('/')[-1].split('.')[0]
            a['href'] = '#genModal'
            a['data-toggle'] = 'modal'
            a['data-target'] = '#genModal'
            a['class'] = 'a-video'
            a['data-figure-path'] = mapToYouTube[video_name]
        elif 'slid' in old_path:
            # Set up image modal
            if 'mov.html' in old_path or 'mpg.html' in old_path:
                old_path = pathlib.Path('/html/someDir') / old_path
                old_path = os.path.normpath(old_path)
                old_path = pathlib.Path(old_path).as_posix()
                lookup = index.figuretable
                img_num = lookup.get_figure_num(old_path)
                figure = lookup.get_figure(img_num)
                video_name = figure.img_orig_path.as_posix()
                video_name = video_name.split('/')[-1].split('.')[0]
                a['href'] = '#genModal'
                a['data-toggle'] = 'modal'
                a['data-target'] = '#genModal'
                a['data-figure-path'] = mapToYouTube[video_name]
                a['class'] = 'a-video'
                a['data-figure-caption'] = (
                    "<b>Figure " + str(img_num) + "</b>. "
                    + str(figure.caption)
                )
            else:
                old_path = pathlib.Path('/html/someDir') / old_path
                old_path = os.path.normpath(old_path)
                old_path = pathlib.Path(old_path).as_posix()
                lookup = index.figuretable
                img_num = lookup.get_figure_num(old_path)
                figure = lookup.get_figure(img_num)
                # a['href'] = '#genModal'
                # a['data-toggle'] = 'modal'
                # a['data-target'] = '#genModal'
                a['class'] = 'a-img'
                a['data-sub-html'] = (
                    "<b>Figure " + str(img_num) + "</b>. "
                    + str(figure.caption)
                )
                new_img_path = index.pathtable.get_path(figure.img_orig_path)
                new_img_path = rel_path(new_img_path, page_obj_path).as_posix()
                a['data-src'] = new_img_path
                a['href'] = new_img_path
        elif 'ref' in old_path:
            # Set up reference modal
            a['href'] = '#genModal'
            a['data-toggle'] = 'modal'
            a['data-target'] = '#genModal'
            a['class'] = 'a-ref'
            letters = old_path.split('ref_')[-1].split('.')[0]
            ref_cls = index.references
            info = ref_cls.get_reference_by_letters(letters)
            if info:
                author = info['author']
                ref_text = info['reference']
                a['data-author'] = author
                a['data-ref-text'] = ref_text
            else:
                print("Failed to find reference for letters "
                        + letters)
        elif 'html/table' in old_path:
            # Set up table modal
            a['href'] = '#genModal'
            a['data-toggle'] = 'modal'
            a['data-target'] = '#genModal'
            a['class'] = 'a-table'
            old_path = pathlib.Path('/html/someDir') / old_path
            old_path = os.path.normpath(old_path)
            old_path = pathlib.Path(old_path).as_posix()
            lookup = index.datatables
            table = lookup.get_table_by_old_path(old_path)
            a['data-table-header'] = (
                "<b>Table " + table['tableNum'] + "</b>. "
                + table['caption']
            )
            table_string = table['table']
            # Replace old links with new info in the table str
            table_soup = BeautifulSoup(table_string, 'html5lib')
            for table_a in table_soup.find_all('a'):
                figure_num = lookup.get_figure_num_by_html_path(
                    table_a['href']
                )
                figure = index.figuretable.get_figure(figure_num)
                table_a['data-sub-html'] = (
                    "<b>Figure " + str(figure_num) + "</b>. "
                    + str(figure.caption)
                )
                new_img_path = index.pathtable.get_path(figure.img_orig_path)
                new_img_path = rel_path(new_img_path, page_obj_path).as_posix()
                table_a['data-src'] = new_img_path
                table_a['href'] = table_a['data-src']
                table_a['data-thumbnail'] = table_a['data-src']
            new_table_str = (
                str(table_soup.body).replace('<body>', '')
            )
            new_table_str = new_table_str.replace('</body>', '')
            a['data-table-string'] = new_table_str
        elif any(
            partname in old_path
            for partname in ['part0', 'part1', 'part2',
                             'part3', 'part4', 'part5', 'descriptions']
        ):
            # Replace link with link to new page
            if '_' in old_path and 'descriptions' not in old_path:
                old_path = old_path.replace('tab', 'body')
            new_link = index.pathtable.get_path(old_path)
            new_link = rel_path(new_link, page_obj_path)
            a['href'] = new_link
        elif any(
            case in old_path
            for case in ['artifacts', 'excavations', 'part6', 'dbs', 'started',
                         'primer', 'maps', 'data']
        ):
            new_link = index.pathtable.get_path(old_path)
            new_link = rel_path(new_link, page_obj_path)
            a['href'] = new_link
        elif 'video' in old_path:
            # Deal with video files
            a['href'] = old_path.replace('/html/video/', '../../video/')
        elif 'version.html' in old_path:
            a['href'] = "#versionModal"
            a['data-toggle'] = "modal"
            a['data-target'] = "#versionModal"
        elif 'javalaunch.html' in old_path or 'digquery.html' in old_path:
            a['href'] = '../electronic_dig_gateway.html'
        elif 'tutorial' in old_path:
            # TODO: Probably just remove this <li> element in the content,
            # don't have time to restructure this right now
            a['href'] = '../electronic_dig_gateway.html'
        else:
            raise Exception('found path ' + old_path + ' in this paragraph: \n'
                            + paragraph_string)

    # If content is a table in Data Downloads, add classes for styling
    if len(soup.body.contents) == 1 and soup.body.contents[0].name == 'table':
        # print('confirming this is in Data Downloads')
        soup.body.table['class'] = ['table', 'table-bordered']

    # Get rid of extra <html>, <head>, and <body> tags in soup
    new_paragraph = str(soup.body).replace('<body>', '').replace('</body>', '')
    return new_paragraph
