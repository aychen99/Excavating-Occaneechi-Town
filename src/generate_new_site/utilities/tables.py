from .str_ops import page_num_to_arabic
import pathlib


class PathTable:
    """
    Object for retrieving paths and entities based on paths in /dig.
    Attributes
    ----------
    path_table : dict
        Dictionary containing the entity to which a path pointed in /dig. This
        is a dict with the following keys:
            path : Path
                Path object containing the path in the new site directory.
            entity : object
                Some object representing a page, figure, etc. Can be None.
    """

    def __init__(self):
        self.path_table = {}

    def get_path(self, old_path):
        """Return the new path for something in /dig based on its old path."""

        if old_path is None:
            return old_path

        if old_path in self.path_table:
            return self.path_table[old_path]['path']

        # Temporary workaround for abs/rel path weirdness
        old_path = pathlib.Path('/') / old_path

        if old_path in self.path_table:
            return self.path_table[old_path]['path']

        return old_path

    def get_entity(self, old_path):
        """Return the entity refered to by a path in /dig."""

        if old_path is None:
            return old_path

        if old_path in self.path_table:
            return self.path_table[old_path]['entity']

        # Temporary workaround for abs/rel path weirdness
        old_path = pathlib.Path('/') / old_path

        if old_path in self.path_table:
            return self.path_table[old_path]['entity']

        return None

    def register(self, old_path, new_path, entity=None):
        """
        Register a path or entity in the translation table.
        If no entity is passed, it defaults to None.
        """

        if old_path not in self.path_table:
            self.path_table[old_path] = {
                'path': new_path,
                'entity': entity
            }

        return


class PageTable:
    def __init__(self, link_chapters=True):
        self.pages = {}
        self.prelim_pages = {}
        self.roman_nums_to_prelim_pages = {}
        self.getting_started_pages = {}
        self.strings_to_getting_started_pages = {}
        self.archaeology_primer_pages = {}
        self.strings_to_archaeology_primer_pages = {}
        self.appendix_a_pages = {}
        self.strings_to_appendix_a_pages = {}
        self.appendix_b_pages = {}
        self.strings_to_appendix_b_pages = {}
        self.data_pages = {}
        self.strings_to_data_pages = {}
        self.link_chapters = link_chapters

    def register(self, page_num, path):
        int_page_num = None
        int_page_dict = None
        strings_page_dict = None



        if page_num.isdigit():
            self.pages[int(page_num)] = path
        elif "GS" in page_num:
            self.strings_to_getting_started_pages[page_num] = path
            page_num = int(page_num.replace("GS", ""))
            self.getting_started_pages[page_num] = path
        elif "AP" in page_num:
            self.strings_to_archaeology_primer_pages[page_num] = path
            page_num = int(page_num.replace("AP", ""))
            self.archaeology_primer_pages[page_num] = path
        elif "Appendix A " in page_num:
            self.strings_to_appendix_a_pages[page_num] = path
            page_num = int(page_num.replace("Appendix A ", ""))
            self.appendix_a_pages[page_num] = path
        elif "Appendix B " in page_num:
            self.strings_to_appendix_b_pages[page_num] = path
            page_num = int(page_num.replace("Appendix B ", ""))
            self.appendix_b_pages[page_num] = path
        elif "Data " in page_num:
            self.strings_to_data_pages[page_num] = path
            page_num = int(page_num.replace("Data ", ""))
            self.data_pages[page_num] = path
        else:
            arabic_page_num = page_num_to_arabic(page_num)
            self.prelim_pages[int(arabic_page_num)] = path
            self.roman_nums_to_prelim_pages[page_num] = path
        return

    def get_page_path(self, page_num):
        if page_num.isdigit() and int(page_num) in self.pages:
            return self.pages[int(page_num)]
        elif "GS" in page_num:
            page_num = int(page_num.replace("GS", ""))
            if int(page_num) in self.getting_started_pages:
                return self.getting_started_pages[int(page_num)]
        elif "AP" in page_num:
            page_num = int(page_num.replace("AP", ""))
            if int(page_num) in self.archaeology_primer_pages:
                return self.archaeology_primer_pages[int(page_num)]
        elif "Appendix A " in page_num:
            page_num = int(page_num.replace("Appendix A ", ""))
            if int(page_num) in self.appendix_a_pages:
                return self.appendix_a_pages[int(page_num)]
        elif "Appendix B " in page_num:
            page_num = int(page_num.replace("Appendix B ", ""))
            if int(page_num) in self.appendix_b_pages:
                return self.appendix_b_pages[int(page_num)]
        elif "Data " in page_num:
            page_num = int(page_num.replace("Data ", ""))
            if int(page_num) in self.data_pages:
                return self.data_pages[int(page_num)]
        elif not page_num.isdigit():
            page_num = page_num_to_arabic(page_num)
            if int(page_num) in self.prelim_pages:
                return self.prelim_pages[int(page_num)]
        return None

    def get_next_page_path(self, page_num):
        if page_num.isdigit() and int(page_num)+1 in self.pages:
            return self.pages[int(page_num)+1]
        elif page_num.isdigit() and self.link_chapters:
            return self.appendix_a_pages[1]
        elif "GS" in page_num:
            page_num = int(page_num.replace("GS", ""))
            if int(page_num)+1 in self.getting_started_pages:
                return self.getting_started_pages[int(page_num)+1]
            elif self.link_chapters:
                return self.archaeology_primer_pages[1]
        elif "AP" in page_num:
            page_num = int(page_num.replace("AP", ""))
            if int(page_num)+1 in self.archaeology_primer_pages:
                return self.archaeology_primer_pages[int(page_num)+1]
            elif self.link_chapters:
                return self.prelim_pages[1]
        elif "Appendix A " in page_num:
            page_num = int(page_num.replace("Appendix A ", ""))
            if int(page_num)+1 in self.appendix_a_pages:
                return self.appendix_a_pages[int(page_num)+1]
            elif self.link_chapters:
                return self.appendix_b_pages[1]
        elif "Appendix B " in page_num:
            page_num = int(page_num.replace("Appendix B ", ""))
            if int(page_num)+1 in self.appendix_b_pages:
                return self.appendix_b_pages[int(page_num)+1]
            elif self.link_chapters:
                return self.data_pages[1]
        elif "Data " in page_num:
            page_num = int(page_num.replace("Data ", ""))
            if int(page_num)+1 in self.data_pages:
                return self.data_pages[int(page_num)+1]
        elif not page_num.isdigit():
            page_num = page_num_to_arabic(page_num)
            if int(page_num)+1 in self.prelim_pages:
                return self.prelim_pages[int(page_num)+1]
            elif (
                int(page_num) == 4
                and 6 in self.prelim_pages
                and 5 not in self.prelim_pages
            ):
                # Special case for when page v is missing in original site data
                return self.prelim_pages[6]
            elif self.link_chapters:
                return self.pages[1]
        return None

    def get_prev_page_path(self, page_num):
        def get_max_page_of_chapter(pages):
            return pages[max(pages.keys())]

        if page_num.isdigit() and int(page_num)-1 in self.pages:
            return self.pages[int(page_num)-1]
        elif self.link_chapters and page_num.isdigit():
            return get_max_page_of_chapter(self.prelim_pages)
        elif "GS" in page_num:
            page_num = int(page_num.replace("GS", ""))
            if int(page_num)-1 in self.getting_started_pages:
                return self.getting_started_pages[int(page_num)-1]
        elif "AP" in page_num:
            page_num = int(page_num.replace("AP", ""))
            if int(page_num)-1 in self.archaeology_primer_pages:
                return self.archaeology_primer_pages[int(page_num)-1]
            elif self.link_chapters:
                return get_max_page_of_chapter(self.getting_started_pages)
        elif "Appendix A " in page_num:
            page_num = int(page_num.replace("Appendix A ", ""))
            if int(page_num)-1 in self.appendix_a_pages:
                return self.appendix_a_pages[int(page_num)-1]
            elif self.link_chapters:
                return get_max_page_of_chapter(self.pages)
        elif "Appendix B " in page_num:
            page_num = int(page_num.replace("Appendix B ", ""))
            if int(page_num)-1 in self.appendix_b_pages:
                return self.appendix_b_pages[int(page_num)-1]
            elif self.link_chapters:
                return get_max_page_of_chapter(self.appendix_a_pages)
        elif "Data " in page_num:
            page_num = int(page_num.replace("Data ", ""))
            if int(page_num)-1 in self.data_pages:
                return self.data_pages[int(page_num)-1]
            elif self.link_chapters:
                return get_max_page_of_chapter(self.appendix_b_pages)
        elif not page_num.isdigit():
            page_num = page_num_to_arabic(page_num)
            if int(page_num)-1 in self.prelim_pages:
                return self.prelim_pages[int(page_num)-1]
            elif (
                int(page_num) == 6
                and 4 in self.prelim_pages
                and 5 not in self.prelim_pages
            ):
                # Special case for when page v is missing in original site data
                return self.prelim_pages[4]
            elif self.link_chapters:
                return get_max_page_of_chapter(self.archaeology_primer_pages)
        return None


class FigureTable:
    def __init__(self):
        self.figures = {}

    def register(self, figure):
        self.figures[figure.figure_num] = figure

    def get_figure(self, figure_num):
        if figure_num in self.figures:
            return self.figures[figure_num]
        return None
