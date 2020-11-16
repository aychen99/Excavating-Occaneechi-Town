from bs4 import BeautifulSoup
import pathlib
import os
from .path_ops import rel_path

def update_text_paragraph(paragraph_string, index, page_obj_path):
    """Update the <a> tags in a textpage/feature description paragraph."""
    # Change innerHTML content of each section/paragraph
    # so that links (e.g. image and references) are updated.
    # TODO: if there is time, find a less redundant way of storing the info
    # for images, tables, and references than directly in the anchor tag.
    soup = BeautifulSoup(paragraph_string, 'html5lib')
    for a in soup.find_all('a'):
        old_path = a['href']
        if 'slid' in old_path:
            # Set up image modal
            if 'mov.html' in old_path or 'mpg.html' in old_path:
                continue # TODO
            else:
                old_path = pathlib.Path('/dig/html/someDir') / old_path
                old_path = os.path.normpath(old_path)
                old_path = str(pathlib.Path(old_path).as_posix())
                lookup = index.figuretable
                img_num = lookup.get_figure_num(old_path)
                figure = lookup.get_figure(img_num)
                a['href'] = '#genModal'
                a['data-toggle'] = 'modal'
                a['data-target'] = '#genModal'
                a['class'] = 'a-img'
                a['data-figure-caption'] = (
                    "<b>Figure " + str(img_num) + "</b>. "
                    + str(figure.caption)
                )
                a['data-figure-path'] = (
                    figure.img_orig_path.as_posix()
                    .replace('/dig/html/images/', '../../imgs/')
                )
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
        elif 'table' in old_path:
            # Set up table modal
            a['href'] = '#genModal'
            a['data-toggle'] = 'modal'
            a['data-target'] = '#genModal'
            a['class'] = 'a-table'
            old_path = pathlib.Path('/dig/html/someDir') / old_path
            old_path = os.path.normpath(old_path)
            old_path = str(pathlib.Path(old_path).as_posix())
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
                table_a['href'] = '#tableImgModal'
                table_a['data-toggle'] = 'modal'
                table_a['data-target'] = '#tableImgModal'
                table_a['data-figure-caption'] = (
                    "<b>Figure " + str(figure_num) + "</b>. "
                    + str(figure.caption)
                )
                table_a['data-figure-path'] = (
                    figure.img_orig_path.as_posix()
                    .replace('/dig/html/images/', '../../imgs/')
                )
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
            if '_' in old_path:
                old_path = old_path.replace('tab', 'body')
            new_link = index.pathtable.get_path(old_path)
            new_link = rel_path(new_link, page_obj_path)
            a['href'] = new_link
        elif 'artifacts' in old_path:
            # TODO Deal with artifacts
            pass
        elif 'excavations' in old_path:
            new_link = index.pathtable.get_path(old_path)
            new_link = rel_path(new_link, page_obj_path)
            a['href'] = new_link
        elif 'part6' in old_path:
            # TODO: Create new dedicated references page,
            # for the table of contents.
            # Only problem being run into is /part6/tab0, tab1, and tab2.html.
            pass
        elif 'dbs' in old_path:
            # TODO: Create dedicated Appendix B page for artifacts details
            pass
        elif 'video' in old_path:
            # TODO: Deal with video files
            pass
        elif 'version.html' in old_path:
            # TODO: Deal with professional vs instructional version
            pass
        else:
            raise Exception('found path ' + old_path + ' in this paragraph: \n'
                            + paragraph_string)

    # Get rid of extra <html>, <head>, and <body> tags in soup
    new_paragraph = str(soup.body).replace('<body>', '').replace('</body>', '')
    return new_paragraph