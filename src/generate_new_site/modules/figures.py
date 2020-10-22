import json
import pathlib
from ..site_data_structs import figure as fig


def process_figures(figures_file, out_dir, tables):
    """
    Process raw figure data, register Paths in translation table.
    Populates a list of figures with objects containing the image path,
    caption, number, etc.
    Parameters
    ----------
    figure_dir : Path
        Path to the directory with the figure data file(s).
    Returns
    -------
    figures : List of 'Figure' objects
        Data for all figure pages.
    """

    print("Processing figure data.")

    figures = []

    with figures_file.open() as f:
        figures_data = json.load(f)

    # Add figures to list in order
    for key, figure_data in figures_data.items():
        figures.append(process_figure(figure_data, out_dir))

    # Register figures in tables for figure lookup
    for figure in figures:
        tables.figure_table.register(figure)

    print("Finished processing figure data.")

    return figures


def process_figure(figure_data, out_dir):
    """
    Returns a Figure populated with the data in figure_data.
    Parameters
    ----------
    figure_data : dict
        Dictionary containing a figure's data
    Returns
    -------
    figure : Figure
        Figure populated with relevant data.
    """
    figure = fig.Figure(
        figure_num=figure_data['figureNum'],
        caption=figure_data['caption'],
        img_path=pathlib.Path(figure_data['path']),
        figure_path=None,  # TODO
        href=out_dir / generate_figure_filename(figure_data['figureNum']),
        orig_width=figure_data['originalDimensions']['width'],
        orig_height=figure_data['originalDimensions']['height']
    )
    for clickable_area in figure_data['clickableAreas']:
        figure.add_clickable_area(fig.ClickableArea(
            x1=clickable_area['x1'],
            y1=clickable_area['y1'],
            x2=clickable_area['x2'],
            y2=clickable_area['y2'],
            orig_href=clickable_area['path']
        ))

    return figure


def generate_figure_filename(figure_num):
    """
    Creates a output Path for a figure page.
    Format is 'figure_XXXX.html'.
    Parameters
    ----------
    figure_num : int
    Returns
    -------
    figure_path : Path
    """

    path_str = 'figure_{:0>4}.html'.format(figure_num)
    return pathlib.Path(path_str)
