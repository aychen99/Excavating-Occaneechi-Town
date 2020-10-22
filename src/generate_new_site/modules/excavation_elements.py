import json
from ..site_data_structs import excavation as exc
from ..site_data_structs import text
from .. import utilities


def process_excavation_elements(excavation_file, description_file,
                                out_dir, exc_chapter, tables):
    """
    Process raw excavation element data, register Paths in translation table.
    Populates lists of features, squares and structures with data from the
    site's excavations chapter.
    Parameters
    ----------
    excavation_file : Path
        Path to the excavation elements data file.
    Returns
    -------
    exc_elems : List of 'ExcavationElement' objects
        Data for all excavation element pages.
    """

    print("Processing excavation element data.")

    features = []
    squares = []
    structures = []

    # This makes me want to vomit, sidebar structuring needs universalization
    features_module = text.Module("Features", "Features", None)
    squares_module = text.Module("Squares", "Squares", None)
    structures_module = text.Module("Structures", "Structures", None)

    with excavation_file.open() as f:
        excavation_data = json.load(f)

    with description_file.open() as f:
        description_data = json.load(f)

    descriptions = [{
        'name': desc['name'],
        'page_num': desc['pageNum'],
        'content': description_data['pages'][desc['pageNum']]
    } for desc in description_data['module']['sections']]

    for element in excavation_data:
        this_elem = process_element(element, descriptions, out_dir, tables)
        this_elem_name = this_elem.name.lower()
        if "feature" in this_elem_name or "burial" in this_elem_name:
            features.append(this_elem)
            features_module.add_section(
                text.Section(this_elem.name, None, this_elem.href, None))
        elif "structure" in this_elem_name:
            structures.append(this_elem)
            structures_module.add_section(
                text.Section(this_elem.name, None, this_elem.href, None))
        else:
            squares.append(this_elem)
            squares_module.add_section(
                text.Section(this_elem.name, None, this_elem.href, None))

    # Yuck, ctrl-f 'vomit'
    exc_chapter.add_module(features_module)
    exc_chapter.add_module(squares_module)
    exc_chapter.add_module(structures_module)

    print("Finished processing excavation element data.")

    return {
        'features': features,
        'squares': squares,
        'structures': structures
    }


def process_element(element_data, descriptions, out_dir, tables):
    """
    Returns an ExcavationElement decorated with the data in element_data.
    Parameters
    ----------
    element_data : dict
        Dictionary containing all data for this excavation element
    Returns
    -------
    element : ExcavationElement
        ExcavaionElement object populated with all element data
    """

    # Find description by name
    description = None
    for desc in descriptions:
        # TODO Probably breaks
        if desc['name'].find(element_data['name']) > -1:
            description = desc

    info = {
        'dimensions': {
            'length': element_data['info']['Dimensions']['Length'],
            'width': element_data['info']['Dimensions']['Width'],
            'depth': element_data['info']['Dimensions']['Depth']
        },
        'type': element_data['info']['Type'],
        'volume': element_data['info']['Volume'],
        'area': element_data['info']['Area'],
    }

    if description is not None:
        elem_filename = generate_element_filename(
            element_data['name'], description['page_num'])
    else:
        elem_filename = generate_element_filename(element_data['name'])

    element = exc.ExcavationElement(
        name=element_data['name'],
        mini_map_path=element_data['miniMapIcon'],
        href=out_dir / "excavations" / elem_filename,
        info=info,
        artifacts_path=element_data['artifactsPath'],
        description_path=element_data['descriptionPath'],
        description=description
    )

    # Add figures
    for fig in element_data['images']:
        element.add_figure(tables.figure_table.get_figure(fig['figureNum']))

    if description is not None:
        tables.page_table.register(
            element.description['page_num'], element.href)

    # TODO check name in JSON
    tables.path_table.register(element_data['path'], element.href, element)
    return element


def generate_element_filename(elem_name, page_num=None):
    """
    Creates an output Path for an element page.
    Format is 'XXX_elem_name.html' with page number, 'elem_name.html' without.
    Parameters
    ----------
    elem_name : str
        Element name (ex. 'Feature 1')
    page_num : str
        Description page number, if applicable. Defaults to None.
    Returns
    -------
    filename : str
    """
    elem_name = utilities.str_ops.make_str_filename_safe(elem_name)

    if page_num is not None:
        filename = '{}_{}.html'.format(
            utilities.str_ops.normalize_file_page_num(page_num), elem_name)
    else:
        filename = '{}.html'.format(elem_name)
    return filename
