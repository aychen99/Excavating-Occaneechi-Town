class Figure:
    """
    Object representing a figure in the original EOT site.
    Attributes
    ----------
    figureNum : int
    caption : str
    imgPath : Path
        Path to the figure's image file in /dig
    figurePath : Path
        Path to the figure's original slid_***.html file
    href : Path
        Path to the new figure's html page
    origWidth : int
        Width of the original image file in pixels
    origHeight : int
        Height of the original image file in pixels
    clickableAreas : list of ClickableArea objects
        List of ClickableArea objects for this figure's image
    """

    def __init__(self, figureNum, caption, imgPath,
                 figurePath, href, origWidth, origHeight):
        self.figureNum = figureNum
        self.caption = caption
        self.imgPath = imgPath
        self.figurePath = figurePath
        self.href = href
        self.origWidth = origWidth
        self.origHeight = origHeight
        self.clickableAreas = []

    def add_clickable_area(self, clickableArea):
        """
        Add a ClickableArea to this Figure's clickableAreas list
        Parameters
        ----------
        clickableArea : ClickableArea
        """
        self.clickableAreas.append(clickableArea)


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
    origHref : Path
        Path to the page linked by the clickable area
    """

    def __init__(self, x1, y1, x2, y2, origHref):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.origHref = origHref
