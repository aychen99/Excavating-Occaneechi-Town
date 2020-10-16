from jinja2 import Environment, FileSystemLoader, select_autoescape
from os.path import relpath
import json
import pathlib
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
        tables.page_table.register(element.description['page_num'], element.href)

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


def write_excavation_pages(excavation_elements, chapters,
                           exc_chapter, tables):
    """
    Generate all excavation element pages.
    Parameters
    ----------
    excavation_elements : list of 'ExcavationElement' objects
        Data for all excavation element pages.
    """

    print("Writing excavation element pages.")

    # Jinja setup
    templates_path = str((pathlib.Path(__file__).parent.parent / "templates"))
    jinja_env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(['html', 'xml']),
        line_statement_prefix='#',
        line_comment_prefix='##',
        trim_blocks=True
    )
    exc_template = jinja_env.get_template('exc_elem.html.jinja')
    exc_desc_template = jinja_env.get_template('exc_elem_desc.html.jinja')

    for module in exc_chapter.modules:
        chapters_rel = [
            c.get_dict_with_relpaths(module.href) for c in chapters
        ]

        for element in excavation_elements[module.full_title.lower()]:
            # Use correct template for description or lack thereof
            if element.description is not None:
                this_template = exc_desc_template
                pagination = {
                    'prev_page_href': utilities.path_ops.rel_path(
                        tables.page_table.get_prev_page_href(element.description['page_num']), element.href),
                    'this_page_num': element.description['page_num'],
                    'next_page_href': utilities.path_ops.rel_path(
                        tables.page_table.get_next_page_href(element.description['page_num']), element.href)
                }
            else:
                this_template = exc_template
                pagination = {}

            element.href.parent.mkdir(parents=True, exist_ok=True)
            with element.href.open('w') as f:
                f.write(this_template.render(
                    excavation_element=element.get_dict_with_relpaths(
                        element.href, tables),
                    chapters=chapters_rel,
                    this_chapter_name="Excavations",
                    this_module_name=module.full_title,
                    this_section_name=element.name,
                    pagination=pagination
                ))

    print("Finished writing excavation element pages.")

    return
