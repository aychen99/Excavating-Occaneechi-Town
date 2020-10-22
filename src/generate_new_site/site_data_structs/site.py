from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..utilities.path_ops import rel_path
from ..utilities.tables import PathTable, PageTable
from pathlib import Path

TEMPLATES_DIRECTORY = str(Path(__file__).parent.parent / "templates")
INDEX_TEMPLATE_FILENAME = "index.html.jinja"

INDEX_TEMPLATE = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    autoescape=select_autoescape(['html', 'xml']),
    line_statement_prefix='#', line_comment_prefix='##', trim_blocks=True
).get_template(INDEX_TEMPLATE_FILENAME)


class Index:
    """
    Root of the site tree.

    Attributes
    ----------
    path : Path
        Path to the site's index.html file.
    children : list of SiteChapter
        List of all of the site's subdivisions, represented by SiteChapters
    figures : list of Figure
        List of all of the site's figures (img and caption)
    pathtable : PathTable
        Table allowing retrieval of site elements by their location in /dig
    figuretable : FigureTable
        Table allowing retrieval of a Figure by its number
    pagetable : PageTable
        Table allowing retrieval of a Page's path by its number

    Fluid Attributes
    -------------------
    These attributes contain relative paths that are frequently updated during
    the site writing phase.

    href : str
        PosixPath-like string containing the relative path to this file
    """

    def __init__(self, path):
        self.path = path
        self.children = []
        self.pathtable = PathTable()
        self.pagetable = PageTable()
        self.figuretable = None

    def add_child(self, child):
        """Adds 'child' to this Index's list of children."""
        if child not in self.children:  # Probably just a waste of time
            self.children.append(child)

    def add_figures(self, figures):
        """Adds the passed Figures object as an attribute."""
        self.figuretable = figures

    def write(self):
        """
        Write the files to which this object and its children correspond.
        """
        print("Writing index.html... ", end='', flush=True)
        self.update_href(self.path)
        # Write index.html
        with self.path.open('w') as f:
            f.write(INDEX_TEMPLATE.render(
                children=self.children
            ))
        print("Done.")
        for child in self.children:
            child.write()

    def update_href(self, start_path):
        """
        Update the href variables for this object and all children.
        Recursively sets the href attributes of this and all child objects to
        be PosixPath-like strings, relative from the starting location
        'start_path'.
        """
        self.href = rel_path(self.path, start_path).as_posix()

        for child in self.children:
            child.update_href(start_path)


class SiteChapter:
    """
    Object representing a chapter (top level division) in the EOT site.

    Attributes
    ----------
    name : str
    path : Path, optional
        Path to this SiteChapter's landing file (i.e. the file to which this
        SiteChapter's href links)
    parent : Index
    children : list of SiteModule
        List of all of the chapter's modules

    Fluid Attributes
    -------------------
    These attributes contain relative paths that are frequently updated during
    the site writing phase.

    href : str
        PosixPath-like string containing the relative path to this file.
    """

    def __init__(self, name, parent, path=None):
        self.name = name
        self.path = path
        self.parent = parent
        self.children = []

    def add_child(self, child):
        """Adds 'child' to this Index's list of children."""
        if child not in self.children:
            self.children.append(child)

    def write(self):
        """
        Write the files to which this object and its children correspond.
        """
        if self.children:
            print("Writing '{}' pages... ".format(self.name), end='', flush=True)
        for child in self.children:
            # Make sure all Site objects know how they would be referenced
            # within this module; pages can link anywhere
            self.parent.update_href(child.path)
            # Make sure that the parent directory exists; some directories are
            # per chapter, some are per module
            child.path.parent.mkdir(parents=True, exist_ok=True)

            child.write()
        if self.children:
            print("Done.")

    def update_href(self, start_path):
        """
        Update the href variables for this object and all children.
        Recursively sets the href attributes of this and all child objects to
        be PosixPath-like strings, relative from the starting location
        'start_path'.
        """
        self.href = None
        if self.path is not None:
            self.href = rel_path(self.path, start_path).as_posix()
        for child in self.children:
            child.update_href(start_path)


class SiteModule:
    """
    Object representing a module (second level division) in the EOT site.

    Attributes
    ----------
    short_name : str
    long_name : str, optional
    author : str, optional
    path : Path, optional
        Path to this module's landing file (i.e. the file to which an href to
        this module links)
    parent : SiteChapter
    children : list of SitePage
        List containing this modules' child pages

    Fluid Attributes
    -------------------
    These attributes contain relative paths that are frequently updated during
    the site writing phase.

    href : str
        PosixPath-like string containing the relative path to this file.
    """

    def __init__(self, short_name, parent, long_name=None, author=None, path=None):
        self.short_name = short_name
        self.long_name = long_name if long_name is not None else short_name
        self.author = author
        self.path = path
        self.parent = parent
        self.children = []

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def write(self):
        for child in self.children:
            child.write()

    def update_href(self, start_path):
        """
        Update the href variables for this object and all children.
        Recursively sets the href attributes of this and all child objects to
        be PosixPath-like strings, relative from the starting location
        'start_path'.
        """
        self.href = None
        if self.path is not None:
            self.href = rel_path(self.path, start_path).as_posix()
        for child in self.children:
            child.update_href(start_path)


class SitePage:
    """
    Object representing a page in the original EOT site.

    Attributes
    ----------
    name : str
        Title of this page.
    page_num : str, optional
        This page's number, if applicable.
    path : Path
        Path to this SitePage's file in the new site.
    parent : SiteModule
        Reference to this page's parent module. Note that even though a page
        can have page children, the parent of those pages is still the module.
    children : list of SitePage
        List containing any child pages of this page.
    content : list of dict
        List of dictionaries containing this page's original content. Dict
        format is {'type': str, 'content': str}.

    Fluid Attributes
    -------------------
    These attributes contain relative paths that can be frequently updated
    during the site writing phase.

    href : str
        PosixPath-like string containing the relative path to this file.
    rel_content : list of dict
        Same as 'content', but with all links updated to be relative.
    """

    def __init__(self, name, path, content, parent, page_num=None):
        self.name = name
        self.page_num = page_num
        self.path = path
        self.parent = parent
        self.children = []
        self.content = content

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parent = self.parent

    def write(self):
        # Inheriting classes will extend this method to actually write pages
        for child in self.children:
            child.write()

    def update_href(self, start_path):
        """
        Update the href variables for this object and all children.
        Recursively sets the href attributes of this and all child objects to
        be PosixPath-like strings, relative from the starting location
        'start_path'.
        """
        self.href = rel_path(self.path, start_path).as_posix()
        for child in self.children:
            child.update_href(start_path)
