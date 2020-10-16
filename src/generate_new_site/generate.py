import argparse
import pathlib
from . import modules
from . import utilities


def generate_site(
        dig_dir, input_dir, output_dir,
        overwrite_out=False, copy_images=False):

    dig_dir = pathlib.Path(dig_dir)
    input_dir = pathlib.Path(input_dir)
    output_dir = pathlib.Path(output_dir)

    # Terminate execution if dig_dir or input_dir don't exist
    if not input_dir.exists():
        print('Input directory: {} does not exist. Site generation aborted.'
              .format(str(input_dir)))
        return
    if not dig_dir.exists():
        print('Dig directory: {} does not exist. Site generation aborted.'
              .format(str(dig_dir)))
        return

    # Terminate execution if output_dir exists and not set to overwrite
    if output_dir.exists() and not overwrite_out:
        print(("Output directory: {} already exists, and overwrite_out is "
               "set to 'False'.").format(str(output_dir)))
        return

    output_dir.mkdir(parents=overwrite_out, exist_ok=overwrite_out)

    imgs_in = dig_dir / "html" / "images"
    imgs_out = output_dir / "imgs"

    # Table for translation from old to new Paths
    tables = utilities.tables.Tables()

    if copy_images:
        utilities.copy_images(dig_dir, imgs_in, imgs_out, tables)
    else:
        utilities.register_images(dig_dir, imgs_in, imgs_out, tables)

    excavation_path = input_dir / "excavationsElements.json"
    descriptions_path = input_dir / "descriptions.json"
    chapter_paths = [input_dir / "part{}.json".format(i) for i in range(6)]
    figures_path = input_dir / "images.json"

    html_out_dir = output_dir / "html"
    index_path = html_out_dir / "index.html"

    figures = modules.process_figures(
        figures_path, html_out_dir, tables)
    chapters = modules.process_chapters(
        chapter_paths, html_out_dir, tables)
    for chapter in chapters:
        if chapter.name == "Excavations":
            exc_chapter = chapter
    exc_elems = modules.process_excavation_elements(
        excavation_path, descriptions_path,
        html_out_dir, exc_chapter, tables)

    # modules.figs.write_figure_pages(figures, path_table)  # TODO make figures
    modules.write_text_pages(chapters, tables)
    modules.write_excavation_pages(
        exc_elems, chapters, exc_chapter, tables)
    modules.write_homepage(chapters, index_path)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="generate new Excavating Occaneechi Town static site directory")
    parser.add_argument(
        "dig-directory",
        type=str,
        help="directory containing old site (dig or digpro)"
    )
    parser.add_argument(
        "input-directory",
        type=str,
        help="directory containing extracted site data"
    )
    parser.add_argument(
        "-o", "--output-directory", type=str, default="newdig",
        help="target directory for new site")
    parser.add_argument(
        "-p", "--parents", action="store_true",
        help="make parent directories for out, no error if existing")
    parser.add_argument(
        "-c", "--copy-images", action="store_true",
        help="copy images from /dig to proper location in target directory")
    args = parser.parse_args()
    args = vars(args)
    generate_site(
        args['dig-directory'],
        args['input-directory'],
        args['output_directory'],
        args['parents'],
        args['copy_images']
    )
