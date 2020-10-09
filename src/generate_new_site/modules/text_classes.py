class Chapter:

    def __init__(self, name, href):
        self.name = name
        self.href = href
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)

    def get_module(self, module_name):
        for module in self.modules:
            if (module_name == module.shortTitle
               or module_name == module.fullTitle):
                return module

        return None

    def set_href(self):
        if self.modules:
            self.href = self.modules[0].href

    def set_hrefs_r(self):
        for module in self.modules:
            module.set_href()

        self.set_href()


class Module:

    def __init__(self, shortTitle, fullTitle, author):
        self.shortTitle = shortTitle
        self.fullTitle = fullTitle
        self.href = ""
        self.author = author
        self.sections = []

    def add_section(self, section):
        """Add a Section to a module"""
        self.sections.append(section)

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
        if self.sections:
            self.href = self.sections[0].href


class Section:

    def __init__(self, name, pageNum, href, content):
        self.name = name
        self.pageNum = pageNum
        self.href = href
        self.content = content
        self.subsections = []

    def add_subsection(self, subsection):
        self.subsections.append(subsection)

    def get_subsection(self, subsection_name):
        for section in self.subsections:
            if subsection_name == section.name:
                return section

        return None
