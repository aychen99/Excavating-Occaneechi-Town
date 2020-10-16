from .. import utilities


class Figure:
    """
    Object representing a figure in the original EOT site.
    Attributes
    ----------
    figure_num : int
    caption : str
    img_path : Path
        Path to the figure's image file in /dig
    figure_path : Path
        Path to the figure's original slid_***.html file
    href : Path
        Path to the new figure's html page
    orig_width : int
        Width of the original image file in pixels
    orig_height : int
        Height of the original image file in pixels
    clickable_areas : list of ClickableArea objects
        List of ClickableArea objects for this figure's image
    """

    def __init__(self, figure_num, caption, img_path,
                 figure_path, href, orig_width, orig_height):
        self.figure_num = figure_num
        self.caption = caption
        self.img_path = img_path
        self.figure_path = figure_path
        self.href = href
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

    def get_dict_with_relpaths(self, start_path, tables):
        return {
            'figure_num': self.figure_num,
            'caption': self.caption,
            'img_path': utilities.path_ops.rel_path(tables.path_table.get_path(self.img_path), start_path),
            'figure_path': self.figure_path,
            'href': utilities.path_ops.rel_path(self.href, start_path),
            'orig_width': self.orig_width,
            'orig_height': self.orig_height,
            'clickable_areas': [
                 area.get_dict_with_relpaths(start_path, tables)
                 for area in self.clickable_areas
            ]
        }


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
    href : Path
        Path to the page linked by the clickable area
    """

    def __init__(self, x1, y1, x2, y2, orig_href):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.href = orig_href

    def get_dict_with_relpaths(self, start_path, tables):
        return {
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'href': utilities.path_ops.rel_path(tables.path_table.get_path(self.href), start_path)
        }
