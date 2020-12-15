from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from . import text
from ..utilities.path_ops import rel_path
from ..utilities.str_ops import make_str_filename_safe, normalize_file_page_num
from ..utilities.process_content import update_text_paragraph
from .site import SiteChapter, SiteModule, SitePage
import json


TEMPLATES_DIRECTORY = str(Path(__file__).parent.parent / "templates")
TEXT_TEMPLATE_FILENAME = "archaeology_primer.html.jinja"

TEXT_TEMPLATE = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    autoescape=select_autoescape(['html', 'xml']),
    line_statement_prefix='#', line_comment_prefix='##',
    trim_blocks=True, lstrip_blocks=True
).get_template(TEXT_TEMPLATE_FILENAME)


class PrimerChapter(SiteChapter):
    """
    Identical to a textchapter except for from_json.
    """

    def __init__(self, name, parent, path=None):
        super().__init__(name=name, parent=parent, path=path)

    def add_child(self, child):
        """
        Add a child to this TextChapter, update self.path if appropriate.

        Parameters
        ----------
        child : TextModule
            Child module of this text chapter.
        """
        super().add_child(child)
        if self.path is None:
            self.set_path()

    def set_path(self, path=None):
        """Set this Chapter's href, manually or automatically."""
        if path is not None:  # Set manually
            self.path = path
        elif len(self.children) > 0:  # Set to first module's href by default
            self.path = self.children[0].path

    def write(self):
        super().write()

    @classmethod
    def from_json(cls, json_path, name, dir, index):
        chapter = text.TextChapter(name=name, parent=index)

        with json_path.open() as f:
            data = json.load(f)

        # Register old archaeological primer video pages
        video_pages = data['videos']

        for module_entry in data['modules']:
            module = text.TextModule(
                short_name=module_entry['shortTitle'],
                long_name=module_entry['fullTitle'],
                parent=chapter,
                author=module_entry['author']
            )
            for section in module_entry['sections']:
                name = make_str_filename_safe(section['name'])
                path = dir / '{}_{}.html'.format(
                    normalize_file_page_num(section['pageNum']), name)

                this_section = PrimerPage(
                    name=section['name'],
                    path=path,
                    content=data['pages'][section['pageNum']]['content'],
                    parent=module,
                    page_num=section['pageNum'],
                    image=data['pages'][section['pageNum']]['image']
                )

                # Fix the content
                from bs4 import BeautifulSoup
                for content_obj in this_section.content:
                    if content_obj["type"] == 'paragraph':
                        soup = BeautifulSoup(content_obj["content"], 'html5lib')
                        for a in soup.find_all('a'):
                            if a['href'] in video_pages:
                                a['data-figure-caption'] = video_pages[a['href']]['caption']
                                a['href'] = video_pages[a['href']]['path'].replace('.mov', '.mp4').replace('.mpg', '.mp4')
                                a['data-is-primer'] = "yes"
                        content_obj['content'] = str(soup.body).replace('<body>', '').replace('</body>', '')

                # Add to path table for link resolution
                index.pathtable.register(
                    section['path'], this_section.path, this_section)

                # Add to page table for pagination
                index.pagetable.register(
                    this_section.page_num, this_section.path)

                for subsection in section['subsections']:
                    name = make_str_filename_safe(subsection['name'])
                    path = dir / '{}_{}.html'.format(
                        normalize_file_page_num(subsection['pageNum']), name)

                    this_subsection = PrimerPage(
                        name=subsection['name'],
                        path=path,
                        content=data['pages'][subsection['pageNum']]['content'],
                        parent=module,
                        page_num=subsection['pageNum'],
                        image=data['pages'][subsection['pageNum']]['image']
                    )

                    # Add to path table for link resolution
                    index.pathtable.register(
                        subsection['path'], this_subsection.path, this_subsection)

                    # Add to page table for pagination
                    index.pagetable.register(
                        this_subsection.page_num, this_subsection.path)

                    this_section.add_child(this_subsection)

                module.add_child(this_section)

                # Add to path table for link resolution
                index.pathtable.register(
                    module_entry['path'], module.path, module)

            # Add the module subtree as child of the chapter
            chapter.add_child(module)

            # Add to path table for link resolution
            index.pathtable.register(data['path'], chapter.path, chapter)

        return chapter


class PrimerPage(SitePage):
    """
    Object representing a section/page in the original EOT site.

    Attributes
    ----------
    name : str
        Title of this section/page.
    page_num : str
        This section's page number, held as str due to Roman-numeral prologue
        page numbers.
    path : Path
        Path to this section's html file.
    parent : TextModule
        Reference to this page's parent object. Always the parent module, even
        for subsections
    children : list of TextPage
        List containing any page children of this page ().
    content : List of dict
        Contents of a page, dictionary with keys 'type' and 'content', denoting
        the type of content ('paragraph', 'italic-title') and the actual
        content respectively.
    """

    def __init__(self, name, path, content, parent, page_num, image):
        super().__init__(name=name, path=path, content=content, parent=parent,
                         page_num=page_num)
        self.image = image

    def write(self):
        prev_href = self.parent.parent.parent.pagetable.get_prev_page_path(self.page_num)
        if prev_href is not None:
            prev_href_rel = rel_path(prev_href, self.path).as_posix()
        else:
            prev_href_rel = None
        next_href = self.parent.parent.parent.pagetable.get_next_page_path(self.page_num)
        if next_href is not None:
            next_href_rel = rel_path(next_href, self.path).as_posix()
        else:
            next_href_rel = None

        pagination = {
            'prev_page_href': prev_href_rel,
            'this_page_num': self.page_num,
            'next_page_href': next_href_rel
        }

        for content_obj in self.content:
            if content_obj['type'] == 'ul':
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content_obj['content'], 'html5lib')
                pageToImgMap = content_obj["pageToImgMap"]
                for a in soup.find_all('a'):
                    image = pageToImgMap[a['href']]
                    new_img_path = self.parent.parent.parent.pathtable.get_path(image['src'])
                    new_img_path = rel_path(new_img_path, self.path).as_posix()
                    a['data-image-path'] = new_img_path
                    a['data-image-caption'] = image['caption']
                    a['href'] = 'javascript:void(0);'
                content_obj['content'] = str(soup.body).replace('<body>', '').replace('</body>', '')
            elif 'content' in content_obj:
                content_obj['content'] = update_text_paragraph(
                    content_obj['content'],
                    self.parent.parent.parent,
                    self.path
                )
            if 'image' in content_obj:
                new_img_path = self.parent.parent.parent.pathtable.get_path(content_obj['image']['path'])
                new_img_path = rel_path(new_img_path, self.path).as_posix()
                content_obj['image']['path'] = new_img_path
            if 'mapImg' in content_obj:
                content_obj['mapImg'] = content_obj['mapImg'].replace('/html/images/', '../../imgs/')

        # Update image paths
        if self.image:
            new_img_path = self.parent.parent.parent.pathtable.get_path(self.image["path"])
            new_img_path = rel_path(new_img_path, self.path).as_posix()
            self.image["path"] = new_img_path
        # TODO

        # Open using wb and encode('utf-8') to resolve encoding issues
        with self.path.open('wb') as f:
            f.write(TEXT_TEMPLATE.render(
                chapters=self.parent.parent.parent.children,
                this_chapter_name=self.parent.parent.name,
                this_module_name=self.parent.long_name,
                this_section_name=self.name,
                this_section=self,
                pagination=pagination
            ).encode('utf-8'))

        super().write()  # Write children
