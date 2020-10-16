from .. import utilities


class ExcavationElement:
    """
    Object representing an excavation page (square, feature, or structure) in
    the original EOT site.
    Attributes
    ----------
    name : str
        Name of the element ("Feature 4.", "Structure 2.", etc.)
    mini_map_path : Path
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
    artifacts_path : Path
        Path to to this element's original artifacts html page, if it exists
    description_path : Path
        Path to to this element's description page, if it exists
    description : dict
        Dictionary containing this element's description page data, can be
        None, contains the following k:v pairs
            name: str
            page_num: str
            content : list of dict
    related_elements : list of RelatedElement objects
    """

    def __init__(self, name, mini_map_path, href, info,
                 artifacts_path, description_path, description):
        self.name = name
        self.mini_map_path = mini_map_path
        self.href = href
        self.info = info
        self.figures = []
        self.artifacts_path = artifacts_path
        self.description_path = description_path
        self.description = description
        self.related_elements = []

    def add_figure(self, figure):
        """
        Add a Figure to this element's figures list
        Parameters
        ----------
        figure : Figure
            Pointer to existing Figure object
        """
        self.figures.append(figure)
        return

    def add_related_element(self, related_element):
        self.related_elements.append(related_element)
        return

    def get_dict_with_relpaths(self, start_path, tables):
        return {
            'name': self.name,
            'mini_map_path': utilities.path_ops.rel_path(tables.path_table.get_path(self.mini_map_path), start_path),
            'href': utilities.path_ops.rel_path(self.href, start_path),
            'info': self.info,
            'figures': [f.get_dict_with_relpaths(start_path, tables) for f in self.figures],
            'artifacts_path': utilities.path_ops.rel_path(tables.path_table.get_path(self.artifacts_path), start_path),
            'desctiption_path': self.description_path,
            'description': self.description,  # TODO relpaths in content links
            'related_elements': [re.get_dict_with_relpaths(start_path, tables) for re in self.related_elements]
        }


class RelatedElement:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_dict_with_relpaths(self, start_path, tables):
        return {
            'name': self.name,
            'path': utilities.path_ops.rel_path(tables.path_table.get_path(self.path), start_path)
        }
