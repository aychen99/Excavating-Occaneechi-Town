from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from ..utilities.path_ops import rel_path
from ..utilities.str_ops import make_str_filename_safe, normalize_file_page_num
from ..utilities.process_content import update_text_paragraph
from .site import SiteChapter, SiteModule, SitePage
from ..utilities.dig_imgs import high_res_images
import json


TEMPLATES_DIRECTORY = str(Path(__file__).parent.parent / "templates")
TEXT_TEMPLATE_FILENAME = "textpage.html.jinja"
APPENDIX_A_TEMPLATE_FILENAME = "appendix_a.html.jinja"
APPENDIX_B_TEMPLATE_FILENAME = "appendix_b.html.jinja"

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    autoescape=select_autoescape(['html', 'xml']),
    line_statement_prefix='#', line_comment_prefix='##',
    trim_blocks=True, lstrip_blocks=True
)
TEXT_TEMPLATE = jinja_env.get_template(TEXT_TEMPLATE_FILENAME)
APPENDIX_A_TEMPLATE = jinja_env.get_template(APPENDIX_A_TEMPLATE_FILENAME)
APPENDIX_B_TEMPLATE = jinja_env.get_template(APPENDIX_B_TEMPLATE_FILENAME)


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

    @classmethod
    def references_from_json(cls, json_path, name, dir, index):
        """
        Factory method for making a ReferenceChapter and children from a .json.

        Parameters
        ----------
        json_path : Path
            Path to the json file containing a dict of references by author.
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
        # This implies you don't even need a new ReferencesChapter class, you need a new from_json
        chapter = TextChapter(name=name, parent=index)

        with json_path.open() as f:
            data = json.load(f)

        # Sort reference keys

        # Add one module for each of A-G, H-R, and S-Z in References
        a_g_module = TextModule(
            short_name="A-G",
            long_name="A-G",
            parent=chapter,
            author=None
        )
        h_r_module = TextModule(
            short_name="H-R",
            long_name="H-R",
            parent=chapter,
            author=None
        )
        s_z_module = TextModule(
            short_name="S-Z",
            long_name="S-Z",
            parent=chapter,
            author=None
        )

        # Three sections: A-G, H-R, S-Z
        a_g_content = []
        h_r_content = []
        s_z_content = []
        authors_sorted = sorted(list(data), key=str.casefold)
        for author in authors_sorted:
            first_letter = author[0].upper()
            content = author
            for reference in data[author]:
                content += '\n<p class="reference">' + reference + '</p>'
            content = {
                "type": "div",
                "content": content
            }
            if first_letter <= "G":
                a_g_content.append(content)
            elif first_letter >= "H" and first_letter <= "R":
                h_r_content.append(content)
            elif first_letter >= "S" and first_letter <= "Z":
                s_z_content.append(content)
            else:
                raise Exception("First letter of author " + author
                                + " out of bounds.")

        # Should be just 250, 251, and 252.
        # Assuming references is added last, as it should be.
        first_page_num = max(index.pagetable.pages.keys()) + 1
        second_page_num = first_page_num + 1
        third_page_num = second_page_num + 1
        # Convert to strings as needed for the code
        first_page_num = str(first_page_num)
        second_page_num = str(second_page_num)
        third_page_num = str(third_page_num)

        a_g_section = TextPage(
            name="A-G",
            path=dir / '{}_{}.html'.format(
                normalize_file_page_num(first_page_num),
                make_str_filename_safe("A-G")
            ),
            content=a_g_content,
            parent=a_g_module,
            page_num=first_page_num
        )

        h_r_section = TextPage(
            name="H-R",
            path=dir / '{}_{}.html'.format(
                normalize_file_page_num(first_page_num),
                make_str_filename_safe("H-R")
            ),
            content=h_r_content,
            parent=h_r_module,
            page_num=second_page_num
        )

        s_z_section = TextPage(
            name="S-Z",
            path=dir / '{}_{}.html'.format(
                normalize_file_page_num(first_page_num),
                make_str_filename_safe("S-Z")
            ),
            content=s_z_content,
            parent=s_z_module,
            page_num=third_page_num
        )

        # Add sections to path table for link resolution
        index.pathtable.register(old_path="/html/part6/tab0.html", new_path=a_g_section.path, entity=a_g_section)
        index.pathtable.register(old_path="/html/part6/tab1.html", new_path=h_r_section.path, entity=h_r_section)
        index.pathtable.register(old_path="/html/part6/tab2.html", new_path=s_z_section.path, entity=s_z_section)

        # Add to page table for pagination
        index.pagetable.register(
            a_g_section.page_num, a_g_section.path
        )
        index.pagetable.register(
            h_r_section.page_num, h_r_section.path
        )
        index.pagetable.register(
            s_z_section.page_num, s_z_section.path
        )

        # No subsections, can safely ignore
        a_g_module.add_child(a_g_section)
        h_r_module.add_child(h_r_section)
        s_z_module.add_child(s_z_section)

        # TODO: Add module to path table for link resolution

        # Add the modules as children of the chapter
        chapter.add_child(a_g_module)
        chapter.add_child(h_r_module)
        chapter.add_child(s_z_module)

        # TODO: Add chapter to path table for link resolution

        return chapter

    @classmethod
    def appendix_a_from_json(cls, json_path, name, dir, index):
        """
        Factory method for making a TextChapter for Appendix A from a .json.

        Parameters
        ----------
        json_path : Path
            Path to the json file for artifacts in Appendix A. The json file
            may also include details from Appendix B.
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

        '''
        # Sort modules by page number in appendix A
        def sorter_helper(elem):
            # print(elem[0])
            page_num = int(elem[1]["appendixAPageNum"])
            # print(page_num)
            return page_num
        sorted_data = {k: v for k, v in sorted(data.items(), key=sorter_helper)}#lambda item: int(item[1]["appendixAPageNum"]))#lambda elem: int(elem[1]["appendixAPageNum"]))# int(operator.itemgetter(1)["appendixAPageNum"]))
        '''

        # Similar to what's in excavation.py
        # Sort appendix A pages by feature/square/structure numbers before
        # adding them in, in order to make the sidebar display
        # Feature 1, 2, 3, ..., etc. rather than Feature 1, 10, 11, ...
        # while keeping the old page numbers for pagination purposes.
        def exc_sorter(elem):
            elem_name_parts = elem[1]['excavationElement'].split(' ')
            elem_type = elem_name_parts[0]
            elem_num = elem_name_parts[1]
            if elem_type == 'Burial':
                return -1000 + int(elem_num)
            elif elem_type == 'Feature':
                return int(elem_num)
            elif elem_type == 'Sq.':
                sq_num = elem_num
                if 'L' in sq_num:
                    sq_num_parts = [int(part) for part in sq_num.split('L')]
                    return (sq_num_parts[0] * 100) + (-1 * sq_num_parts[1])
                elif 'R' in sq_num:
                    sq_num_parts = [int(part) for part in sq_num.split('R')]
                    return (sq_num_parts[0] * 100) + sq_num_parts[1]
            elif elem_type == 'Structure':
                return 1000000 + int(elem_num)
            else:
                raise Exception('Unknown Exc Context found: ' + elem['name'])

        sorted_data = {k: v for k, v in sorted(data.items(), key=exc_sorter)}

        # Add a module for Features, Squares, and Structures
        features = TextModule(
            short_name="Features",
            long_name="Features",
            parent=chapter
        )
        squares = TextModule(
            short_name="Squares",
            long_name="Squares",
            parent=chapter
        )
        structures = TextModule(
            short_name="Structures",
            long_name="Structures",
            parent=chapter
        )
        
        # Add a section for each excavation element and insert into the modules
        for artifacts_obj in sorted_data.values():
            name = make_str_filename_safe(artifacts_obj["excavationElement"])
            path = dir / '{}_{}.html'.format(
                normalize_file_page_num(artifacts_obj["appendixAPageNum"]), name)

            # Create the content to be inserted
            content = [{
                "type": "artifact-zone",
                "content": artifacts_obj["zones"]
            }]
            for zone in content[0]["content"]:
                for artifact in zone["artifacts"]:
                    if artifact["Photo"]:
                        figure_num = artifact["Photo"]
                        lookup = index.figuretable
                        figure = lookup.get_figure(figure_num)
                        artifact["Photo"] = figure

            if ("feature" in name.lower()
                    or "burial" in name.lower()):
                parent = features
            elif "structure" in name.lower():
                parent = structures
            else:
                parent = squares

            exc_element = index.pathtable.get_entity(artifacts_obj["parentExcPage"])
            this_section = TextPage(
                name=artifacts_obj["excavationElement"],
                path=path,
                content=content,
                parent=parent,
                page_num="Appendix A " + artifacts_obj["appendixAPageNum"],
                other_info={
                    # "parentExcElem": exc_element,
                    "parentExcPath": rel_path(exc_element.path, path).as_posix()
                },
                template=APPENDIX_A_TEMPLATE
            )
            # exc_element.artifacts_page = this_section
            exc_element.artifacts_path = rel_path(path, index.pathtable.get_path(exc_element.path))

            # Add section to path table for link resolution
            # HOTFIX: hardcode old_path based on exc_XX.html
            oldpath = artifacts_obj['parentExcPage'].replace("/excavations/", "/artifacts/").replace("exc_", "art_").replace(".html", "0.html")
            index.pathtable.register(old_path=oldpath, new_path=this_section.path, entity=this_section)

            # Add to page table for pagination
            index.pagetable.register(
                this_section.page_num, this_section.path)

            # No subsections
            parent.add_child(this_section)

            # TODO: Add module to path table for link resolution

        # Add the module subtree as child of the chapter
        chapter.add_child(features)
        chapter.add_child(squares)
        chapter.add_child(structures)

        # TODO: Add chapter to path table for link resolution

        return chapter

    @classmethod
    def appendix_b_from_json(cls, json_path, name, dir, index):
        """
        Factory method for making a TextChapter for Appendix A from a .json.

        Parameters
        ----------
        json_path : Path
            Path to the json file for artifacts in Appendix B.
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

        # Sort modules by page number in appendix B
        def sorter_helper(elem):
            # print(elem[0])
            page_num = int(elem[1]["pageNum"])
            # print(page_num)
            return page_num
        sorted_data = {k: v for k, v in sorted(data.items(), key=sorter_helper)}#lambda item: int(item[1]["appendixAPageNum"]))#lambda elem: int(elem[1]["appendixAPageNum"]))# int(operator.itemgetter(1)["appendixAPageNum"]))

        # Add a module for each excavation element
        for apx_b_page in sorted_data.values():
            module = TextModule(
                short_name=apx_b_page["name"],
                long_name=apx_b_page["name"],
                parent=chapter,
                author=None
            )
            # Make only one section per module in appendix B
            name = make_str_filename_safe(apx_b_page["name"])
            path = dir / '{}_{}.html'.format(
                normalize_file_page_num(str(int(apx_b_page["pageNum"])+1)), name)

            # Create the content to be inserted
            content = [{
                "type": "artifact-zone",
                "content": apx_b_page
            }]

            this_section = TextPage(
                name=apx_b_page["name"],
                path=path,
                content=content,
                parent=module,
                page_num="Appendix B " + str(int(apx_b_page["pageNum"]) + 1),
                template=APPENDIX_B_TEMPLATE
            )

            # Add section to path table for link resolution
            # HOTFIX: dict of paths from names. Only 7 pages... This isn't that
            #         bad right? Definitely fix this in extract later
            oldpathtable = {
                'Beads': "/html/dbs/page0.html",
                'Ceramics': "/html/dbs/page1.html",
                'Faunal Remains': "/html/dbs/page2.html",
                'Historic Artifacts': "/html/dbs/page3.html",
                'Historic Ceramics': "/html/dbs/page4.html",
                'Lithics': "/html/dbs/page5.html",
                'Pipes': "/html/dbs/page6.html"
            }
            index.pathtable.register(old_path=oldpathtable[apx_b_page["name"]], new_path=this_section.path, entity=this_section)

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

    def __init__(self, name, path, content, parent, page_num, other_info=None, template=TEXT_TEMPLATE):
        super().__init__(name=name, path=path, content=content, parent=parent,
                         page_num=page_num)
        self.other_info = other_info
        self.template = template

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

        # Only update text paragraphs for regular text pages, not Appendix A/B
        if self.template == TEXT_TEMPLATE:
            for content_obj in self.content:
                content_obj['content'] = update_text_paragraph(
                    content_obj['content'],
                    self.parent.parent.parent,
                    self.path
                )

        # Open using wb and encode('utf-8') to resolve encoding issues
        with self.path.open('wb') as f:
            f.write(self.template.render(
                chapters=self.parent.parent.parent.children,
                this_chapter_name=self.parent.parent.name,
                this_module_name=self.parent.long_name,
                this_section_name=self.name,
                this_section=self,
                other_info=self.other_info,
                pagination=pagination,
                high_res_images=high_res_images
            ).encode('utf-8'))

        super().write()  # Write children
