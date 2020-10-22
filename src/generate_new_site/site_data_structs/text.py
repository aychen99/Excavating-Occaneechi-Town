from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from ..utilities.path_ops import rel_path
from ..utilities.str_ops import make_str_filename_safe, normalize_file_page_num
from .site import SiteChapter, SiteModule, SitePage
import json


TEMPLATES_DIRECTORY = str(Path(__file__).parent.parent / "templates")
TEXT_TEMPLATE_FILENAME = "textpage.html.jinja"

TEXT_TEMPLATE = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    autoescape=select_autoescape(['html', 'xml']),
    line_statement_prefix='#', line_comment_prefix='##', trim_blocks=True
).get_template(TEXT_TEMPLATE_FILENAME)


class TextChapter(SiteChapter):
    """
    Object representing a chapter in the original EOT site.

    Attributes
    ----------
    name : str
        Name of the chapter
    path : Path, optional
        Path to this SiteChapter's landing file (i.e. the file to which this
        SiteChapter's href links to)
    parent : Index
    children : list of TextModule
        List containing this chapter's child TextModules
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
        """
        Factory method for making a TextChapter and its children from a .json.

        Parameters
        ----------
        json_path : Path
            Path to the json file containing chapter data.
        name : str
            Name of the chapter.
        dir : Path
            Directory in the new site that will contain this chapter's pages.
        index : Index
            Root of the site tree.

        Returns
        -------
        chapter : TextChapter
        """
        chapter = TextChapter(name=name, parent=index)

        with json_path.open() as f:
            data = json.load(f)

        for module_entry in data['modules']:
            module = TextModule(
                short_name=module_entry['module']['shortTitle'],
                long_name=module_entry['module']['fullTitle'],
                parent=chapter,
                author=module_entry['module']['author']
            )
            for section in module_entry['module']['sections']:
                name = make_str_filename_safe(section['name'])
                path = dir / '{}_{}.html'.format(
                    normalize_file_page_num(section['pageNum']), name)

                this_section = TextPage(
                    name=section['name'],
                    path=path,
                    content=data['pages'][section['pageNum']]['content'],
                    parent=module,
                    page_num=section['pageNum']
                )

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

                    this_subsection = TextPage(
                        name=subsection['name'],
                        path=path,
                        content=data['pages'][subsection['pageNum']]['content'],
                        parent=module,
                        page_num=subsection['pageNum']
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
                    module_entry['module']['path'], module.path, module)

            # Add the module subtree as child of the chapter
            chapter.add_child(module)

            # Add to path table for link resolution
            index.pathtable.register(data['path'], chapter.path, chapter)

        return chapter


class TextModule(SiteModule):
    """
    Object representing a module in the original EOT site.

    Attributes
    ----------
    short_name : str
        Short form title of this module, used in sidebar in other modules.
    long_name : str
        Long form title of this module, used in sidebar for selected module.
    author : str, optional
        Author of this module's pages, used in sidebar.
    path : Path, optional
        Path to this module's landing file (i.e. the file to which an href to
        this module links)
    parent : TextChapter
    sections : list of Section
        List containing this text modules's child text pages
    """

    def __init__(self, short_name, long_name, parent, author=None, path=None):
        super().__init__(short_name=short_name, long_name=long_name,
                         parent=parent, author=author, path=path)

    def add_child(self, child):
        """
        Add a child to this TextModule, update self.path if appropriate.

        Parameters
        ----------
        child : TextPage
            Child page of this text module.
        """
        super().add_child(child)
        if self.path is None:
            self.set_path()

    def set_path(self):
        """Set this Module's href to the href of its first Section child."""
        if len(self.children) > 0:
            self.path = self.children[0].path


class TextPage(SitePage):
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

    def __init__(self, name, path, content, parent, page_num):
        super().__init__(name=name, path=path, content=content, parent=parent,
                         page_num=page_num)

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

        with self.path.open('w') as f:
            f.write(TEXT_TEMPLATE.render(
                chapters=self.parent.parent.parent.children,
                this_chapter_name=self.parent.parent.name,
                this_module_name=self.parent.long_name,
                this_section_name=self.name,
                this_section=self,
                pagination=pagination
            ))

        super().write()  # Write children
