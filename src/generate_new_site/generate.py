import argparse
from pathlib import Path
import json
from . import site_data_structs
from . import utilities


def generate_site(
        dig_dir, input_dir, output_dir, new_img_dir,
        overwrite_out=False, copy_images=False, copy_videos=False, copy_data=True,
        version="dig"):

    DIG_DIR = Path(dig_dir)
    INPUT_DIR = None
    OUTPUT_DIR = None
    if input_dir == "Default":
        INPUT_DIR = Path("jsons") / version
    else:
        INPUT_DIR = Path(input_dir)
    if output_dir == "Default":
        OUTPUT_DIR = Path("new" + version)
    else:
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

    if new_img_dir == "Default":
        NEW_IMG_DIR = None
    else:
        NEW_IMG_DIR = Path(new_img_dir)

    HTML_OUT_DIR = OUTPUT_DIR / "html"
    INDEX_PATH = HTML_OUT_DIR / "index.html"

    ASSETS_IN = Path(__file__).parent / "assets"
    ASSETS_OUT = OUTPUT_DIR / "assets"

    HTML_OUT_DIR.mkdir(parents=overwrite_out, exist_ok=overwrite_out)

    # Table for translation from old to new Paths
    index = site_data_structs.site.Index(INDEX_PATH)

    if copy_images:
        utilities.dig_imgs.copy_images(DIG_DIR, IMGS_IN, IMGS_OUT, index, new_img_dir=NEW_IMG_DIR)
    else:
        utilities.dig_imgs.register_images(DIG_DIR, IMGS_IN, IMGS_OUT, index, new_img_dir=NEW_IMG_DIR)

    # Copy CSS, JS, home page images, and other assets
    utilities.html_assets.copy_html_assets(
        ASSETS_IN, ASSETS_OUT, index, dig_dir
    )
    # Copy videos
    utilities.html_assets.copy_videos(
        DIG_DIR / "html/video", OUTPUT_DIR / "video",
        index, dig_dir, copy_files=copy_videos
    )
    # Copy downloadable data
    utilities.html_assets.copy_html_assets(
        DIG_DIR / 'html/data/content/files', OUTPUT_DIR / 'dataForDownload',
        index, dig_dir, copy_files=copy_data, register=True
    )

    DESCRIPTIONS_PATH = INPUT_DIR / "descriptions.json"
    EXCAVATIONS_PATH = INPUT_DIR / "excavationsElements.json"
    FIGURES_PATH = INPUT_DIR / "images.json"
    REFERENCES_PATH = INPUT_DIR / "references.json"
    OLD_REF_LETTERS_PATH = INPUT_DIR / "hrefsToRefs.json"
    TABLES_PATH = INPUT_DIR / "tables.json"
    TABLES_HTML_PATHS_TO_NUMS_PATH = INPUT_DIR / "tableHTMLPathsToNums.json"
    TABLES_IMAGE_PATHS_TO_NUMS_PATH = (
        INPUT_DIR / "tableImagePathsToFigureNums.json"
    )
    ARTIFACTS_PATH = INPUT_DIR / "artifactsByExcElementComplete.json"
    ARTIFACTS_DETAILS_PATH = INPUT_DIR / "artifactsDetails.json"

    figures = site_data_structs.figure.Figures.from_json(
        FIGURES_PATH, HTML_OUT_DIR/"figures", index)
    references = site_data_structs.references.References.from_json(
        REFERENCES_PATH, OLD_REF_LETTERS_PATH, index
    )
    tables = site_data_structs.tables.Tables.from_json(
        TABLES_PATH,
        TABLES_HTML_PATHS_TO_NUMS_PATH,
        TABLES_IMAGE_PATHS_TO_NUMS_PATH,
        index
    )

    index.add_figures(figures)
    index.add_references(references)
    index.add_tables(tables)

    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "started.json",
        name="Getting Started",
        dir=HTML_OUT_DIR / "gettingstarted",
        index=index))
    index.add_child(site_data_structs.archaeology_primer.PrimerChapter.from_json(
        json_path=INPUT_DIR / "primer.json",
        name="Archaeology Primer",
        dir=HTML_OUT_DIR / "primer",
        index=index
    ))
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
    # Save excavation chapter for easy access later
    excavation_chapter = site_data_structs.excavation.ExcavationChapter.from_json(
        exc_json_path=EXCAVATIONS_PATH,
        desc_json_path=DESCRIPTIONS_PATH,
        name="Excavations",
        dir=HTML_OUT_DIR / "excavations",
        index=index
    )
    index.add_child(excavation_chapter)

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
    index.add_child(site_data_structs.text.TextChapter.references_from_json(
        json_path=REFERENCES_PATH,
        name="References",
        dir=HTML_OUT_DIR / "references",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.appendix_a_from_json(
        json_path = ARTIFACTS_PATH,
        name="Appendix A: Artifacts by Excavation Context",
        dir=HTML_OUT_DIR / "appendixa",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.appendix_b_from_json(
        json_path = ARTIFACTS_DETAILS_PATH,
        name="Appendix B: Artifacts by Category",
        dir=HTML_OUT_DIR / "appendixb",
        index=index
    ))
    index.add_child(site_data_structs.text.TextChapter.from_json(
        json_path=INPUT_DIR / "dataChapter.json",
        name="Data Downloads",
        dir=HTML_OUT_DIR / "data",
        index=index
    ))
    index.add_child(site_data_structs.web.WebChapter(
        name="Electronic Dig", parent=index,
        path=HTML_OUT_DIR))

    index.write()  # Write the site!

    # Add the page-numbers-to-html-file-path dictionary to the JavaScript file
    # enabling navigation by page num.
    JS_PATH = ASSETS_OUT / "js"
    with (JS_PATH / "page-num-navigation-template.js").open('r') as f:
        page_num_navigation_js = f.read()
    page_num_nav_json = dict.copy(index.pagetable.roman_nums_to_prelim_pages)
    page_num_nav_json.update(index.pagetable.pages)
    page_num_nav_json.update(index.pagetable.strings_to_getting_started_pages)
    page_num_nav_json.update(index.pagetable.strings_to_archaeology_primer_pages)
    page_num_nav_json.update(index.pagetable.strings_to_appendix_a_pages)
    page_num_nav_json.update(index.pagetable.strings_to_appendix_b_pages)
    page_num_nav_json.update(index.pagetable.strings_to_data_pages)
    for pageNum, pathValue in page_num_nav_json.items():
        page_path = utilities.path_ops.rel_path(pathValue, HTML_OUT_DIR)
        page_path = str(page_path.as_posix())
        page_num_nav_json[pageNum] = page_path
    page_num_nav_json = json.dumps(page_num_nav_json, indent=2)

    page_num_navigation_js = page_num_navigation_js.replace(
        "'placeholderForJinjaGeneration'",
        page_num_nav_json
    )
    with (JS_PATH / "page-num-navigation.js").open('w') as f:
        f.write(page_num_navigation_js)

    # Add a JavaScript file containing an href lookup table for the excavation map
    # Set up paths and names for map links
    elem_data = {}
    excavation_chapter.parent.update_href(excavation_chapter.path)
    for module in excavation_chapter.children:
        for page in module.children:
            elem_data[utilities.str_ops.make_str_filename_safe(page.name)] = {
                'href': page.href,
                'name': page.name
            }

    js_file_str = "const hrefs = {};".format(json.dumps(elem_data))
    with (JS_PATH / "exc_hrefs.js").open('w') as f:
        f.write(js_file_str)

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
