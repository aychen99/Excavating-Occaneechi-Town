from .. import utilities


class Chapter:
    """
    Object representing a chapter in the original EOT site.
    Attributes
    ----------
    name : str
        Name of the chapter
    path : Path
        Path to this chapter's desired output directory
    href : Path
        Path to this chapter's first page
    modules : list of Module
        List containing this chapter's child Modules
    """

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.href = None
        self.modules = []

    def add_module(self, module):
        """
        Add a Module child to this Chapter, update self.href if appropriate.
        Parameters
        ----------
        module : Module
            Module to be added to self.modules list.
        """
        self.modules.append(module)
        if self.href is None:
            self.set_href()

        return

    def get_module(self, module_name):
        """
        Get this Chapter's Module child with name matching arg.
        Parameters
        ----------
        module_name : str
            String containing the short or long title of the sought Module.
        """
        for module in self.modules:
            if (module_name == module.short_title
               or module_name == module.full_title):
                return module

        return None

    def set_href(self, href=None):
        """Set this Chapter's href, manually or automatically."""
        # Set manually
        if href is not None:
            self.href = href
        # Set to first module's href by default
        elif len(self.modules) > 0:
            self.href = self.modules[0].href

        return

    def get_dict_with_relpaths(self, start_path):
        if self.href is not None:
            rel_href = utilities.path_ops.rel_path(self.href, start_path)
        else:
            rel_href = None
        return {
            'name': self.name,
            'path': self.path,
            'href': rel_href,
            'modules': [
                 module.get_dict_with_relpaths(start_path)
                 for module in self.modules
            ]
        }


class Module:
    """
    Object representing a module in the original EOT site.
    Attributes
    ----------
    short_title : str
        Short form title of this module, used in sidebar in other modules.
    full_title : str
        Long form title of this module, used in sidebar for selected module.
    href : Path
        Path to this module's first page.
    author : str
        Author of this module's pages, used in sidebar.
    sections : list of Section
        List containing this modules's child sections
    """

    def __init__(self, short_title, full_title, author):
        self.short_title = short_title
        self.full_title = full_title
        self.href = None
        self.author = author
        self.sections = []

    def add_section(self, section):
        """
        Add a Section to this Module, update Module's href if appropriate.
        Parameters
        ----------
        section : Section
            Section object to be added to self.sections list.
        """
        self.sections.append(section)
        if self.href is None:
            self.set_href()

    def get_section(self, section_name):
        """Get the section in a module corresponding to the passed name"""
        for section in self.sections:
            if section_name == section.page_title:
                return section

    def get_section_r(self, section_name):
        """Same as get_section, but recursively search through subsections"""
        target = self.get_section(section_name)
        if not target:
            for section in self.sections:
                target = section.get_subsection
                if target:
                    return target

        return None

    def set_href(self):
        """Set this Module's href to the href of its first Section child."""
        if len(self.sections) > 0:
            self.href = self.sections[0].href

    def get_dict_with_relpaths(self, start_path):
        return {
            'short_title': self.short_title,
            'full_title': self.full_title,
            'href': utilities.path_ops.rel_path(self.href, start_path),
            'author': self.author,
            'sections': [
                 section.get_dict_with_relpaths(start_path)
                 for section in self.sections
            ]
        }


class Section:
    """
    Object representing a section/page in the original EOT site.
    Attributes
    ----------
    name : str
        Title of this section/page.
    page_num : str
        This section's page number, held as str due to Roman-numeral prologue
        page numbers.
    href : Path
        Path to this section's html file.
    content : List of dict
        Contents of a page, dictionary with keys 'type' and 'content', denoting
        the type of content ('paragraph', 'italic-title') and the actual
        content respectively.
    subsections : list of Section
        List containing any subsection children of this section.
    """

    def __init__(self, name, page_num, href, content):
        self.name = name
        self.page_num = page_num
        self.href = href
        self.content = content
        self.subsections = []

    def add_subsection(self, subsection):
        """
        Add a Section as a child of this section.
        Parameters
        ----------
        subsection : Section
            Section to be added to self.subsections list.
        """
        self.subsections.append(subsection)

    def get_subsection(self, subsection_name):
        """
        Return the Section child of this section that matches passedname arg.
        Parameters
        ----------
        subsection_name: str
            Name of Section child of this section.
        """
        for section in self.subsections:
            if subsection_name == section.name:
                return section

        return None

    def get_dict_with_relpaths(self, start_path):
        return {
            'name': self.name,
            'page_num': self.page_num,
            'href': utilities.path_ops.rel_path(self.href, start_path),
            'content': self.content,
            'subsections': [
                 subsection.get_dict_with_relpaths(start_path)
                 for subsection in self.subsections
            ]
        }
