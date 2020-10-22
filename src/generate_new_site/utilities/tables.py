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
    def __init__(self):
        self.pages = {}
        self.prelim_pages = {}

    def register(self, page_num, path):
        if page_num.isdigit():
            self.pages[int(page_num)] = path
        else:
            page_num = page_num_to_arabic(page_num)
            self.prelim_pages[int(page_num)] = path
        return

    def get_page_path(self, page_num):
        if page_num.isdigit() and int(page_num) in self.pages:
            return self.pages[int(page_num)]
        elif not page_num.isdigit():
            page_num = page_num_to_arabic(page_num)
            if int(page_num) in self.prelim_pages:
                return self.prelim_pages[int(page_num)]
        return None

    def get_next_page_path(self, page_num):
        if page_num.isdigit() and int(page_num)+1 in self.pages:
            return self.pages[int(page_num)+1]
        elif not page_num.isdigit():
            page_num = page_num_to_arabic(page_num)
            if int(page_num)+1 in self.prelim_pages:
                return self.prelim_pages[int(page_num)+1]
        return None

    def get_prev_page_path(self, page_num):
        if page_num.isdigit() and int(page_num)-1 in self.pages:
            return self.pages[int(page_num)-1]
        elif not page_num.isdigit():
            page_num = page_num_to_arabic(page_num)
            if int(page_num)-1 in self.prelim_pages:
                return self.prelim_pages[int(page_num)-1]
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
