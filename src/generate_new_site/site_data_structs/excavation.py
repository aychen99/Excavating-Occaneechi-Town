class ExcavationElement:
    """
    Object representing an excavation page (square, feature, or structure) in
    the original EOT site.
    Attributes
    ----------
    name : str
        Name of the element ("Feature 4.", "Structure 2.", etc.)
    miniMapPath : Path
        Path to the minimap image file
    href : Path
        Path to this element's new html file
    info : dict
        Dictionary of data about this element, contains the following k:v pairs
            dimensions : dict
                length : str
                width : str
                depth : str
            type : str
            volume : str
            area : str
    figures : list of Figure objects
        List of Figures, all figures linked on this elements page
    artifactsPath : Path
        Path to to this element's original artifacts html page, if it exists
    descriptionPath : Path
        Path to to this element's description page, if it exists
    """

    def __init__(self, name, miniMapPath, href, info,
                 artifactsPath, descriptionPath):
        self.name = name
        self.miniMapPath = miniMapPath
        self.href = href
        self.info = info
        self.artifactsPath = artifactsPath
        self.descriptionPath = descriptionPath

    def addFigure(self, figure):
        """
        Add a Figure to this element's figures list
        Parameters
        ----------
        figure : Figure
            Pointer to existing Figure object
        """
        self.figures.append(figure)

#   def addFigureByNum(self, figureNum):
#       pass
