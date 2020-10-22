import argparse
from pathlib import Path
from . import site_data_structs
from . import utilities


def generate_site(
        dig_dir, input_dir, output_dir,
        overwrite_out=False, copy_images=False):

    DIG_DIR = Path(dig_dir)
    INPUT_DIR = Path(input_dir)
    OUTPUT_DIR = Path(output_dir)

    # Terminate execution if dig_dir or input_dir don't exist
    if not INPUT_DIR.exists():
        print('Input directory: {} does not exist. Site generation aborted.'
              .format(str(INPUT_DIR)))
        return
    if not DIG_DIR.exists():
        print('Dig directory: {} does not exist. Site generation aborted.'
              .format(str(DIG_DIR)))
        return

    # Terminate execution if output_dir exists and not set to overwrite
    if OUTPUT_DIR.exists() and not overwrite_out:
        print(("Output directory: {} already exists, and overwrite_out is "
               "set to 'False'.").format(str(OUTPUT_DIR)))
        return

    OUTPUT_DIR.mkdir(parents=overwrite_out, exist_ok=overwrite_out)

    IMGS_IN = DIG_DIR / "html" / "images"
    IMGS_OUT = OUTPUT_DIR / "imgs"

    HTML_OUT_DIR = OUTPUT_DIR / "html"
    INDEX_PATH = HTML_OUT_DIR / "index.html"

    HTML_OUT_DIR.mkdir(parents=overwrite_out, exist_ok=overwrite_out)

    # Table for translation from old to new Paths
    index = site_data_structs.site.Index(INDEX_PATH)

    if copy_images:
        utilities.dig_imgs.copy_images(DIG_DIR, IMGS_IN, IMGS_OUT, index)
    else:
        utilities.dig_imgs.register_images(DIG_DIR, IMGS_IN, IMGS_OUT, index)

    DESCRIPTIONS_PATH = INPUT_DIR / "descriptions.json"
    EXCAVATIONS_PATH = INPUT_DIR / "excavationsElements.json"
    FIGURES_PATH = INPUT_DIR / "images.json"

    figures = site_data_structs.figure.Figures.from_json(
        FIGURES_PATH, HTML_OUT_DIR/"figures", index)

    index.add_figures(figures)

    # Dummy objects for unimplemented chapters
    index.add_child(site_data_structs.site.SiteChapter(
        name="Getting Started", parent=index))
    index.add_child(site_data_structs.site.SiteChapter(
        name="Archaeology Primer", parent=index))

    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "part0.json",
        name="Introduction",
        dir=HTML_OUT_DIR / "introduction",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "part1.json",
        name="Contents",
        dir=HTML_OUT_DIR / "contents",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "part2.json",
        name="Background",
        dir=HTML_OUT_DIR / "background",
        index=index
    ))
    # Excavation chapter interleaved here
    index.add_child(site_data_structs.excavation.ExcavationChapter.from_json(
        exc_json_path=EXCAVATIONS_PATH,
        desc_json_path=DESCRIPTIONS_PATH,
        name="Excavations",
        dir=HTML_OUT_DIR / "excavations",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "part3.json",
        name="Artifacts",
        dir=HTML_OUT_DIR / "artifacts",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "part4.json",
        name="Food Remains",
        dir=HTML_OUT_DIR / "foodremains",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "part5.json",
        name="Interpretations",
        dir=HTML_OUT_DIR / "interpretations",
        index=index
    ))
    index.add_child(site_data_structs.site.SiteChapter(
        name="Electronic Dig", parent=index,
        path=Path("https://electronicdig.sites.oasis.unc.edu/")))

    index.write()  # Write the site!

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
