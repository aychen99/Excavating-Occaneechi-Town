from bs4 import BeautifulSoup
from pathlib import Path
import os

# NOTE: tab0.html can be safely ignored

def extract_primer_page(html_string, dig_dir_str, current_page_name, readfile):
    # primer*.html, including subpages like 14a, 13b, 23a, etc.
    soup = BeautifulSoup(html_string, 'html5lib')
    page_num = soup.div.b.text.replace("Page ", "").split(" of")[0]
    title = soup.center.h1.text
    content = []
    non_paragraph_content = None
    image = None

    if soup.map:
        # Special case of primer05.html
        square_map = str(soup.map)
        map_js = str(soup.script)
        form = soup.form
        del form['method']
        form['onsubmit'] = 'return false;'
        del form.input['size']
        form_str = str(form)
        map_img = Path(os.path.normpath(Path('/html/primer') / soup.img['src'])).as_posix()
        non_paragraph_content = {
            "type": "map",
            "form": form_str,
            "mapJs": map_js,
            "map": square_map,
            "mapImg": map_img
        }
    elif soup.ul:
        # Primer 13, 14, or 23
        files = []
        for li in soup.ul.find_all('li'):
            if not li.a:
                files.append(current_page_name)
                new_a = soup.new_tag('a', href=current_page_name)
                new_a.string = li.string
                li.clear()
                li.append(new_a)
            else:
                files.append(li.a['href'])
        ul = str(soup.ul)
        non_paragraph_content = {
            "type": "ul",
            "content": ul,
            "pageToImgMap": {}
        }
        caption_for_no_image = None
        first_html_name = files[0].replace('primer', '').replace('.html', '')
        if not first_html_name.isdigit():
            files.insert(0, 'primer' + first_html_name[:-1] + '.html')

        def is_image_caption_table(table_tag):
            return table_tag.name == 'table' and table_tag.has_attr('align') and table_tag['align'] == 'right'
        for filename in files:
            file_html = readfile(filename, Path(dig_dir_str) / "html/primer")
            new_soup = BeautifulSoup(file_html, 'html5lib')
            table_for_image = new_soup.find(is_image_caption_table)
            if table_for_image.td.has_attr('valign'):
                # Primer 14 or 23
                if table_for_image.td.b:
                    # Not an a, b, or c page
                    caption_for_no_image = str(table_for_image.td.b).replace('<b>', '').replace('</b>', '').replace("\n", " ")
                    caption_for_no_image = " ".join(caption_for_no_image.split('<br>'))
                else:
                    image_src = Path(os.path.normpath(Path('/html/primer') / new_soup.img['src'])).as_posix()
                    image_caption = new_soup.font.text.strip()
                    non_paragraph_content["pageToImgMap"][filename] = {
                        "src": image_src,
                        "caption": image_caption
                    }
            else:
                # Primer 13
                caption_for_no_image = "Click on a stage of the excavation process to view it."
                image_src = Path(os.path.normpath(Path('/html/primer') / new_soup.img['src'])).as_posix()
                image_caption = new_soup.font.decode_contents().replace('<font>', '').replace('</font>', '').replace("\n", " ")
                image_caption = " ".join(image_caption.split('<br/>'))
                non_paragraph_content["pageToImgMap"][filename] = {
                    "src": image_src,
                    "caption": image_caption
                }
        
        non_paragraph_content["noImageCaption"] = caption_for_no_image
    else:
        # All the other primers
        if soup.img:
            def is_image_caption_table(table_tag):
                return table_tag.name == 'table' and table_tag.has_attr('align') and table_tag['align'] == 'right'
            # Note: If no soup.img, is primer 25
            image_path = Path(os.path.normpath(Path('/html/primer') / soup.img['src'])).as_posix()
            image_caption = soup.font.decode_contents().replace('<font>', '').replace('</font>', '').replace("\n", " ")
            image_caption = " ".join(image_caption.split('<br/>'))
            image = {
                "path": image_path,
                "caption": image_caption
            }

    # Standardize links in all <a> tags
    a_tags = soup.find_all('a')
    for a in a_tags:
        if 'javascript:opennewwindow' in a['href']:
            a['href'] = '/html/primer/' + a['href'].split('(')[-1].replace("'", "").split(')')[0]
        else:
            a['href'] = Path(os.path.normpath(Path('/html/primer') / a['href'])).as_posix()

    for p in soup.find_all('p'):
        if str(p).replace('<p>', '').replace('</p>', '').strip() != '' and not p.font:
            p_text = ' '.join([line.strip() for line in str(p).replace('<p>', '').replace('</p>', '').split('\n')])
            # Remove double spaces
            p_text = p_text.replace('  ', ' ')
            content.append({
                "type": "paragraph",
                "content": p_text
            })

    if non_paragraph_content:
        content.append(non_paragraph_content)

    return {
        "image": image,
        "map": None,
        "content": content,
        "title": title,
        "pageNum": "AP" + page_num
    }

def extract_entire_primer(dig_dir_str, readfile):
    primer_dir = Path(dig_dir_str) / 'html/primer'

    primer = {
        "path": '/html/primer',
        "modules": None,
        "pages": {}
    }
    videos = {}
    primer_htmls_by_page_num = {}
    for filepath in primer_dir.iterdir():
        if filepath.name == 'contents.html':
            primer["modules"] = extract_table_of_contents(readfile(filepath.name, filepath.parent))
        elif filepath.name == 'tab0.html':
            pass
        elif 'primer' in filepath.name:
            page_num = filepath.name.replace('primer', '').replace('.html', '')
            if page_num.isdigit() and page_num not in primer_htmls_by_page_num:
                primer_htmls_by_page_num[page_num] = filepath.name
        elif any(video_name in filepath.name for video_name in ['feature.html', 'pits.html', 'plowzone.html', 'trowel.html', 'wtrscrn.html']):
            video_info = extract_video_page(readfile(filepath.name, filepath.parent))
            videos['/html/primer/' + filepath.name] = video_info
        else:
            raise Exception("unknown file " + filepath + " found.")

    for primer_html_name in primer_htmls_by_page_num.values():
        page_stuff = extract_primer_page(readfile(primer_html_name, Path(dig_dir_str) / "html/primer"), dig_dir_str, primer_html_name, readfile)
        primer["pages"][page_stuff["pageNum"]] = page_stuff

    primer["videos"] = videos
    return primer


def extract_video_page(html_string):
    # pits, plowzone, trowel, wtrscrn, feature.html
    soup = BeautifulSoup(html_string, 'html5lib')
    link = soup.embed['src']
    caption = soup.b.text.strip()
    return {
        "path": Path(os.path.normpath(Path('/html/primer') / link)).as_posix(),
        "caption": caption
    }

def extract_table_of_contents(html_string):
    # contents.html
    soup = BeautifulSoup(html_string, 'html5lib')
    contents_table = soup.find_all('table')[1]

    modules = []
    for td in contents_table.find_all('td'):
        contents = td.contents
        currentPageNum = None
        for content in contents:
            if str(content).strip() != '':
                if content.name == 'font' and content.text:
                    modules.append({
                        "path": None,
                        "shortTitle": content.text,
                        "fullTitle": content.text,
                        "author": None,
                        "sections": [] 
                    })
                elif content.name == 'a' and content.text:
                    if modules[-1]['path'] == None:
                        modules[-1]['path'] = "/html/primer/" + content['href']
                    modules[-1]['sections'].append({
                        "name": content.text,
                        "path": "/html/primer/" + content['href'],
                        "subsections": [],
                        "pageNum": currentPageNum
                    })
                elif str(content).strip().split('.')[0].isdigit():
                    currentPageNum = "AP" + str(content).strip().split('.')[0]

    return modules
