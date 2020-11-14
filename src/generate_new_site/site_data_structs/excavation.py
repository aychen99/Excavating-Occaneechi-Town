from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import json
from ..utilities.path_ops import rel_path
from ..utilities.str_ops import make_str_filename_safe, normalize_file_page_num
from ..utilities.process_content import update_text_paragraph
from .site import SiteChapter, SiteModule, SitePage

TEMPLATES_DIRECTORY = str(Path(__file__).parent.parent / "templates")
EXCAVATION_TEMPLATE_FILENAME = "excavation.html.jinja"
EXC_ELEM_TEMPLATE_FILENAME = "exc_elem.html.jinja"
EXC_DESC_TEMPLATE_FILENAME = "exc_elem_desc.html.jinja"
JINJA_ENV = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    autoescape=select_autoescape(['html', 'xml']),
    line_statement_prefix='#', line_comment_prefix='##', trim_blocks=True
)

EXCAVATION_TEMPLATE = JINJA_ENV.get_template(EXCAVATION_TEMPLATE_FILENAME)
EXC_ELEM_TEMPLATE = JINJA_ENV.get_template(EXC_ELEM_TEMPLATE_FILENAME)
EXC_DESC_TEMPLATE = JINJA_ENV.get_template(EXC_DESC_TEMPLATE_FILENAME)


class ExcavationChapter(SiteChapter):
    """
    Object representing the excavation chapter of the EOT site.

    Attributes
    ----------
    name : str
    path : Path
        Path to this chapter's landing file (the Excavation map page)
    parent : Index
    children : list of SiteModule
        List of all of the chapter's modules
    """

    def __init__(self, name, parent, path=None):
        super().__init__(name=name, parent=parent, path=path)

    def write(self):
        print("Writing '{}' pages... ".format(self.name), end='', flush=True)

        self.path.parent.mkdir(parents=True, exist_ok=True)

        # As of right now, only one directory, only one update_href call needed
        self.parent.update_href(self.path)
        for child in self.children:
            child.write()

        with self.path.open('w') as f:
            f.write(EXCAVATION_TEMPLATE.render(
                excavation_element=self,
                chapters=self.parent.children,
                this_chapter_name="Excavations",
                this_module_name=None,
                this_section_name=None
            ))
        print("Done.")

    # Remove once Excavation chapter has separate chapter level page
    def add_child(self, child):
        """
        Add a child to this ExcavationChapter, update self.path if appropriate.

        Parameters
        ----------
        child : TextPage
            Child page of this text module.
        """
        super().add_child(child)
        if self.path is None:
            self.set_path()

    # Remove once Excavation chapter has separate chapter level page
    def set_path(self):
        """Set this Chapter's href to the href of its first Module child."""
        if len(self.children) > 0:
            self.path = self.children[0].path

    @classmethod
    def from_json(cls, exc_json_path, desc_json_path, name, dir, index):
        """
        Factory method for making the ExcavationChapter from a .json.

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
        excavations : ExcavationChapter
        """
        exc_page_path = dir / "excavations.html"
        excavations = ExcavationChapter(name=name, parent=index, path=exc_page_path)
        features = ExcavationModule(
            short_name="Features", parent=excavations)
        squares = ExcavationModule(
            short_name="Squares", parent=excavations)
        structures = ExcavationModule(
            short_name="Structures", parent=excavations)

        with exc_json_path.open() as f:
            exc_data = json.load(f)

        with desc_json_path.open() as f:
            desc_data = json.load(f)

        # Get desc_data into better format
        descriptions = [{
            'name': desc['name'],
            'page_num': desc['pageNum'],
            'content': desc_data['pages'][desc['pageNum']]
        } for desc in desc_data['module']['sections']]

        # Parse out each element
        for element in exc_data:
            # Find description if it exists
            description = None
            for desc in descriptions:
                # TODO Probably breaks
                if desc['name'].strip(" Description") == element['name']:
                    description = desc

            info = {
                'dimensions': {
                    'length': element['info']['Dimensions']['Length'],
                    'width': element['info']['Dimensions']['Width'],
                    'depth': element['info']['Dimensions']['Depth']
                },
                'type': element['info']['Type'],
                'volume': element['info']['Volume'],
                'area': element['info']['Area'],
            }

            # Filename format depends on whether or not there is a page num
            name = make_str_filename_safe(element['name'])
            if description is not None:
                elem_filename = '{}_{}.html'.format(
                    normalize_file_page_num(description['page_num']), name)
            else:
                elem_filename = '{}.html'.format(name)

            # Figure out which module is parent
            if ("feature" in element['name'].lower()
                    or "burial" in element['name'].lower()):
                parent = features
            elif "structure" in element['name'].lower():
                parent = structures
            else:
                parent = squares

            #
            page_num = None
            if description is not None:
                page_num = description['page_num']

            elem = ExcavationPage(
                name=element['name'],
                path=dir / elem_filename,
                parent=parent,
                mini_map_orig_path=element['miniMapIcon'],
                info=info,
                artifacts_path=element['artifactsPath'],
                description_path=element['descriptionPath'],
                content=description,
                page_num=page_num
            )

            for re in element['relatedElements']:
                elem.add_related_element(RelatedElement(
                    name=re['name'],
                    parent=elem,
                    path=re['path']
                ))

            # TODO sort excavation elements for correct sidebar order

            # Add to corresponding module
            elem.parent.add_child(elem)

            # Add figures
            for fig in element['images']:
                elem.add_figure(index.figuretable.get_figure(fig['figureNum']))

            # If the element has a desc, it has a page num; register it
            if page_num is not None:
                index.pagetable.register(
                    elem.content['page_num'], elem.path)

            # Add to pathtable so this element can be looked up by its old link
            index.pathtable.register(element['path'], elem.path, elem)

        excavations.add_child(features)
        excavations.add_child(squares)
        excavations.add_child(structures)

        return excavations


class ExcavationModule(SiteModule):
    """
    Object representing a module in the Excavations chapter of the EOT site.
    Excavation modules are 'Features', 'Squares', and 'Structures'

    Attributes
    ----------
    short_name : str
    long_name : str, optional
    author : str, optional
    path : Path, optional
        Path to this module's landing file (i.e. the file to which an href to
        this module links).
    parent : ExcavationChapter
    children : list of ExcavationPage
        List containing this modules' child pages.

    Fluid Attributes
    -------------------
    These attributes contain relative paths that are frequently updated during
    the site writing phase.

    href : str
        PosixPath-like string containing the relative path to this file.
    """

    def __init__(self, short_name, parent,
                 long_name=None, author=None, path=None):

        super().__init__(short_name=short_name, long_name=long_name,
                         parent=parent, author=author, path=path)

    def add_child(self, child):
        """
        Add a child to this ExcavationModule, update self.path if appropriate.

        Parameters
        ----------
        child : TextPage
            Child page of this text chapter.
        """
        super().add_child(child)
        if self.path is None:
            self.set_path()

    def set_path(self):
        """Set this Module's href to the href of its first Page child."""
        if len(self.children) > 0:
            self.path = self.children[0].path


class ExcavationPage(SitePage):
    """
    Object representing an excavation page (square, feature, or structure) in
    the original EOT site.

    Attributes
    ----------
    name : str
        Name of the element ("Feature 4.", "Structure 2.", etc.)
    page_num : str, optional
        This page description's number, if applicable.
    path : Path
        Path to this element's new html file
    parent : ExcavationModule
        Reference to this page's parent object.
    mini_map_orig_path : Path
        Path to the minimap image file
    info : dict
        Dictionary of data about this element, formatted as:
        {
            'dimensions' : {'length' : str, 'width' : str, 'depth' : str},
            'type' : str,
            'volume' : str,
            'area' : str
        }
    figures : list of Figure
        List of Figures, all figures linked on this elements page
    artifacts_path : Path, optional
        Path to to this element's original artifacts html page, if it exists
    description_path : Path, optional
        Path to to this element's description page, if it exists
    content : dict, optional
        Description content
    related_elements : list of RelatedElement

    Fluid Attributes
    -------------------
    These attributes contain relative paths that can be frequently updated
    during the site writing phase.

    href : str
        PosixPath-like string containing the relative path to this file.
    rel_content : list of dict
        Same as 'content', but with all links updated to be relative.
    """

    def __init__(self, name, path, parent, mini_map_orig_path, info,
                 artifacts_path=None, description_path=None, content=None,
                 page_num=None):

        super().__init__(name=name, path=path, parent=parent,
                         content=content, page_num=page_num)
        self.mini_map_orig_path = mini_map_orig_path
        self.info = info
        self.figures = []
        self.artifacts_path = artifacts_path
        self.description_path = description_path
        self.related_elements = []

    def add_figure(self, figure):
        """
        Add a Figure to this element's figures list

        Parameters
        ----------
        figure : Figure
        """
        if figure not in self.figures:
            self.figures.append(figure)

    def add_related_element(self, related_element):
        if related_element not in self.related_elements:
            self.related_elements.append(related_element)

    def write(self):
        if self.page_num is not None:
            this_template = EXC_DESC_TEMPLATE
            pagination = {
                'prev_page_href': rel_path(
                    self.parent.parent.parent.pagetable.get_prev_page_path(
                        self.page_num), self.path),  # TODO as_posix()?
                'this_page_num': self.page_num,
                'next_page_href': rel_path(
                    self.parent.parent.parent.pagetable.get_next_page_path(
                        self.page_num), self.path)  # TODO as_posix()?
            }
        else:
            this_template = EXC_ELEM_TEMPLATE
            pagination = {}

        if self.content:
            # TODO: Extra content key exists here, needs to be removed
            # earlier on in extraction/generation
            for content_obj in self.content['content']['content']:
                content_obj['content'] = update_text_paragraph(
                    content_obj['content'],
                    self.parent.parent.parent,
                    self.path
                )

        with self.path.open('w') as f:
            f.write(this_template.render(
                excavation_element=self,
                chapters=self.parent.parent.parent.children,
                this_chapter_name="Excavations",
                this_module_name=self.parent.long_name,
                this_section_name=self.name,
                pagination=pagination
            ))

        super().write()  # Write children

    def update_href(self, start_path):
        for re in self.related_elements:
            re.update_href(start_path)
        for f in self.figures:
            f.update_href(start_path)

        self.href = rel_path(self.path, start_path).as_posix()

        self.mini_map_path = rel_path(
            self.parent.parent.parent.pathtable.get_path(
                self.mini_map_orig_path), start_path).as_posix()

        new_artifacts_href = rel_path(
            self.parent.parent.parent.pathtable.get_path(
                self.artifacts_path), start_path)
        if new_artifacts_href is not None:
            self.artifacts_href = new_artifacts_href.as_posix()
        else:
            self.artifacts_href = None


class RelatedElement:
    def __init__(self, name, path, parent):
        self.name = name
        self.path = path
        self.parent = parent

    def update_href(self, start_path):
        self.href = rel_path(
            self.parent.parent.parent.parent.pathtable.get_path(
                self.path), start_path).as_posix()
