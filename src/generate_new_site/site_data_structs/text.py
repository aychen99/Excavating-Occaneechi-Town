class Chapter:
    """
    Object representing a chapter in the original EOT site.
    Attributes
    ----------
    name : str
        Name of the chapter
    href : str
        Path to this chapter's first page
    modules : list of Module
        List containing this chapter's child Modules
    """

    def __init__(self, name, href):
        self.name = name
        self.href = href
        self.modules = []

    def add_module(self, module):
        """
        Add a Module child to this Chapter.
        Parameters
        ----------
        module : Module
            Module to be added to self.modules list.
        """
        self.modules.append(module)

    def get_module(self, module_name):
        """
        Get this Chapter's Module child with name matching arg.
        Parameters
        ----------
        module_name : str
            String containing the short or long title of the sought Module.
        """
        for module in self.modules:
            if (module_name == module.shortTitle
               or module_name == module.fullTitle):
                return module

        return None

    def set_href(self):
        """Set this Chapter's href to that of its first Module child."""
        if self.modules:
            self.href = self.modules[0].href

    def set_hrefs_r(self):
        """Set the hrefs of all Module children, then set own href."""
        for module in self.modules:
            module.set_href()

        self.set_href()


class Module:
    """
    Object representing a module in the original EOT site.
    Attributes
    ----------
    shortTitle : str
        Short form title of this module, used in sidebar in other modules.
    fullTitle : str
        Long form title of this module, used in sidebar for selected module.
    href : str
        Path to this module's first page.
    author : str
        Author of this module's pages, used in sidebar.
    sections : list of Section
        List containing this modules's child sections
    """

    def __init__(self, shortTitle, fullTitle, author):
        self.shortTitle = shortTitle
        self.fullTitle = fullTitle
        self.href = ""
        self.author = author
        self.sections = []

    def add_section(self, section):
        """
        Add a Section to this Module and set this Module's href if appropriate.
        Parameters
        ----------
        section : Section
            Section object to be added to self.sections list.
        """
        self.sections.append(section)
        if self.href == "":
            self.set_href()

    def get_section(self, section_name):
        """Get the section in a module corresponding to the passed name"""
        for section in self.sections:
            if section_name == section.pageTitle:
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
        if self.sections:
            self.href = self.sections[0].href


class Section:
    """
    Object representing a section/page in the original EOT site.
    Attributes
    ----------
    name : str
        Title of this section/page.
    pageNum : str
        This section's page number, held as str due to Roman-numeral prologue
        page numbers.
    href : str
        Path to this section's html file.
    content : List of dict
        Contents of a page, dictionary with keys 'type' and 'content', denoting
        the type of content ('paragraph', 'italic-title') and the actual
        content respectively.
    subsections : list of Section
        List containing any subsection children of this section.
    """

    def __init__(self, name, pageNum, href, content):
        self.name = name
        self.pageNum = pageNum
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
