from .. import utilities
import json
from pathlib import Path


class Figures:
    def __init__(self, parent):
        self.figures = {}
        self.parent = parent

    def register(self, figure):
        self.figures[figure.figure_num] = figure

    def get_figure(self, figure_num):
        if figure_num in self.figures:
            return self.figures[figure_num]
        return None

    @classmethod
    def from_json(cls, json_path, dir, index):
        """
        Factory method for making a TextChapter and its children from a .json.

        Parameters
        ----------
        json_path : Path
            Path to the json file containing chapter data.
        index : Index
            Root of the site tree.

        Returns
        -------
        figures : Figures
        """
        figures = Figures(parent=index)

        with json_path.open() as f:
            data = json.load(f)

        for figure_data in data.values():
            figure = Figure(
                figure_num=figure_data['figureNum'],
                caption=figure_data['caption'],
                img_orig_path=Path(figure_data['path']),
                parent=figures,
                figure_path=None,  # TODO
                path=dir/"figure_{:0>4}.html".format(figure_data['figureNum']),
                orig_width=figure_data['originalDimensions']['width'],
                orig_height=figure_data['originalDimensions']['height']
            )
            for clickable_area in figure_data['clickableAreas']:
                figure.add_clickable_area(ClickableArea(
                    x1=clickable_area['x1'],
                    y1=clickable_area['y1'],
                    x2=clickable_area['x2'],
                    y2=clickable_area['y2'],
                    orig_href=clickable_area['path'],
                    parent=figure
                ))
            figures.register(figure)

        return figures


class Figure:
    """
    Object representing a figure in the original EOT site.

    Attributes
    ----------
    figure_num : int
    caption : str
    img_orig_path : Path
        Path to the figure's image file in /dig
    figure_path : Path
        Path to the figure's original slid_***.html file
    path : Path
        Path to the new figure's html page
    parent : Figures
    orig_width : int
        Width of the original image file in pixels
    orig_height : int
        Height of the original image file in pixels
    clickable_areas : list of ClickableArea objects
        List of ClickableArea objects for this figure's image

    Fluid Attributes
    -------------------
    These attributes contain relative paths that are frequently updated during
    the site writing phase.

    href : str
        PosixPath-like string containing the relative path to this file.
    img_path : str
        PosixPath-like string containing the relative path to this figure's
        image file in the new site directory.
    """

    def __init__(self, figure_num, caption, img_orig_path,
                 figure_path, path, parent, orig_width, orig_height):
        self.figure_num = figure_num
        self.caption = caption
        self.img_orig_path = img_orig_path
        self.figure_path = figure_path
        self.path = path
        self.parent = parent
        self.orig_width = orig_width
        self.orig_height = orig_height
        self.clickable_areas = []

    def add_clickable_area(self, clickable_area):
        """
        Add a ClickableArea to this Figure's clickableAreas list

        Parameters
        ----------
        clickable_area : ClickableArea
        """
        self.clickable_areas.append(clickable_area)

    def update_href(self, start_path):
        for area in self.clickable_areas:
            area.update_href(start_path)

        new_href = utilities.path_ops.rel_path(
            self.path, start_path)
        if new_href is not None:
            self.href = new_href.as_posix()
        else:
            self.href = None

        new_img_path = utilities.path_ops.rel_path(
            self.parent.parent.pathtable.get_path(
                self.img_orig_path), start_path)
        if new_img_path is not None:
            self.img_path = new_img_path.as_posix()
        else:
            self.img_path = None


class ClickableArea:
    """
    Object containing the information for the clickable links mapped to regions
    of the figure's image.

    Attributes
    ----------
    x1 : int
        X coordinate of the first point defining a bounding box
    y1 : int
        Y coordinate of the first point defining a bounding box
    x2 : int
        X coordinate of the second point defining a bounding box
    y2 : int
        Y coordinate of the second point defining a bounding box
    orig_href : Path
        Path to the page linked by the clickable area

    Fluid Attributes
    -------------------
    These attributes contain relative paths that are frequently updated during
    the site writing phase.

    href : str
        PosixPath-like string containing the relative path to the linked page.
    """

    def __init__(self, x1, y1, x2, y2, orig_href, parent):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.orig_href = orig_href
        self.parent = parent

    def update_href(self, start_path):
        new_href = utilities.path_ops.rel_path(
            self.parent.parent.parent.pathtable.get_path(
                self.orig_href), start_path)
        if new_href is not None:
            self.href = new_href.as_posix()
        else:
            self.href = None
