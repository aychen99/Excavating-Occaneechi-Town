import json
import operator
from pathlib import Path
from . import text
from .site import SiteChapter, SitePage
from ..utilities.path_ops import rel_path
from ..utilities.str_ops import make_str_filename_safe, normalize_file_page_num
from ..utilities.process_content import update_text_paragraph
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIRECTORY = str(Path(__file__).parent.parent / "templates")
TEXT_TEMPLATE_FILENAME = "appendix_b.html.jinja"

TEXT_TEMPLATE = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    autoescape=select_autoescape(['html', 'xml']),
    line_statement_prefix='#', line_comment_prefix='##',
    trim_blocks=True, lstrip_blocks=True
).get_template(TEXT_TEMPLATE_FILENAME)


class AppendixBChapter(SiteChapter):
    """
    Essentially identical to a TextChapter except for the from_json method.
    """
    def __init__(self, name, parent, path=None):
        super().__init__(name=name, parent=parent, path=path)

    def add_child(self, child):
        """
        Add a child to this chapter, update self.path if appropriate.

        Parameters
        ----------
        child : TextModule
            Child module of this chapter.
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
        Factory method for making a ReferenceChapter and children from a .json.

        Parameters
        ----------
        json_path : Path
            Path to the json file for "artifactsByExcElementComplete.json".
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
        chapter = text.TextChapter(name=name, parent=index)

        with json_path.open() as f:
            data = json.load(f)

        # Sort modules by page number in appendix B
        def sorter_helper(elem):
            # print(elem[0])
            page_num = int(elem[1]["pageNum"])
            # print(page_num)
            return page_num
        sorted_data = {k: v for k, v in sorted(data.items(), key=sorter_helper)}#lambda item: int(item[1]["appendixAPageNum"]))#lambda elem: int(elem[1]["appendixAPageNum"]))# int(operator.itemgetter(1)["appendixAPageNum"]))

        # Add a module for each excavation element
        for exc_elem_path, apx_b_page in sorted_data.items():
            module = text.TextModule(
                short_name=apx_b_page["name"],
                long_name=apx_b_page["name"],
                parent=chapter,
                author=None
            )
            # Only one section per module in appendix A
            name = make_str_filename_safe(apx_b_page["name"])
            path = dir / '{}_{}.html'.format(
                normalize_file_page_num(str(int(apx_b_page["pageNum"])+1)), name)

            # Create the content to be inserted
            content = [{
                "type": "artifact-zone",
                "content": apx_b_page
            }]

            this_section = AppendixBPage(
                name=apx_b_page["name"],
                path=path,
                content=content,
                parent=module,
                page_num="Appendix B " + str(int(apx_b_page["pageNum"]) + 1)
            )

            # TODO: Add section to path table for link resolution

            # Add to page table for pagination
            index.pagetable.register(
                this_section.page_num, this_section.path)

            # No subsections
            module.add_child(this_section)

            # TODO: Add module to path table for link resolution

            # Add the module subtree as child of the chapter
            chapter.add_child(module)

            # TODO: Add chapter to path table for link resolution

        return chapter


class AppendixBPage(SitePage):
    """
    Identical to a TextPage except for the template it uses.
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

        '''for content_obj in self.content:
            print(self.parent.parent.parent)
            content_obj['content'] = update_text_paragraph(
                content_obj['content'],
                self.parent.parent.parent,
                self.path
            )'''

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
