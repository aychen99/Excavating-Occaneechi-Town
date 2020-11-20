from .modules import (
    standard_text_chapter,
    getting_started,
    archaeology_primer,
    data_downloads,
    excavation_details_page,
    image_page,
    feature_descriptions,
    references,
    tables,
    artifacts
)
from .utilities import file_ops
import pathlib
import json


def run_extraction(config):
    # Set up variables from config
    dig_parent_dir = config['digParentDirPath']
    output_dir_path = config['extractionOutputDirPath']
    shrinkJsons = config['shrinkExtractionJsons']
    output_dir_path_obj = None
    if output_dir_path == "Default":
        output_dir_path_obj = pathlib.Path(__file__).parent / "jsons"
    else:
        output_dir_path_obj = pathlib.Path(output_dir_path)
    output_dir_path_obj.mkdir(parents=True, exist_ok=True)
    overwrite_files = config['overwriteExistingExtractedData']

    def write_file(data, filename_path_obj, sort_keys=False, prettify=True):
        if not overwrite_files and filename_path_obj.is_file():
            pass
        else:
            indent = None
            if prettify and not shrinkJsons:
                indent = 4
            with open(filename_path_obj, 'w') as f:
                json.dump(data, f, sort_keys=sort_keys, indent=indent)

    # Run text chapter extraction
    print("Extracting text chapters... ...")
    text_partnames = ['part0', 'part1', 'part2', 'part3', 'part4', 'part5']
    for partname in text_partnames:
        print("    Extracting " + partname)
        output_filename = output_dir_path_obj / (partname + ".json")
        data = standard_text_chapter.extract_standard_part(partname, dig_parent_dir, file_ops.readfile)
        if partname == 'part0':
            data = standard_text_chapter.reextract_title_page(data, dig_parent_dir, file_ops.readfile)
        write_file(data, output_filename)

    # Run getting started extraction
    print("Extracting Getting Started... ...")
    getting_started_data = getting_started.extract_getting_started(dig_parent_dir, file_ops.readfile)
    write_file(getting_started_data, output_dir_path_obj / "started.json")

    # Run archaeology primer extraction
    print("Extracting Archaeology Primer... ...")
    primer_data = archaeology_primer.extract_entire_primer(dig_parent_dir, file_ops.readfile)
    write_file(primer_data, output_dir_path_obj / "primer.json")

    # Run excavations element pages extraction
    print("Extracting excavations element pages... ...")
    excavations_pages = excavation_details_page.extract_all_exc_pages(dig_parent_dir, file_ops.readfile)
    excavations_output_filename = output_dir_path_obj / "excavationsElements.json"
    write_file(excavations_pages, excavations_output_filename)

    # Run image pages extraction
    print("Extracting image pages... ...")
    images = image_page.extract_all_images(dig_parent_dir, file_ops.readfile)
    image_metadata_dicts = image_page.generate_metadata_dicts(images)
    images_output_filename = output_dir_path_obj / "images.json"
    write_file(images, images_output_filename)
    for dict_name, data in image_metadata_dicts.items():
        output_filename = output_dir_path_obj / (dict_name + ".json")
        write_file(data, output_filename, True)

    # Run feature description extraction
    print("Extracting feature descriptions... ...")
    descriptions = feature_descriptions.extract_descriptions(dig_parent_dir, file_ops.readfile)
    descriptions_output_filename = output_dir_path_obj / "descriptions.json"
    write_file(descriptions, descriptions_output_filename, True)

    # Run references extraction
    print("Extracting references... ...")
    refs = references.extract_all_references(dig_parent_dir, file_ops.readfile)
    write_file(refs['refs'], output_dir_path_obj / "references.json", True)
    write_file(refs['hrefsToRefs'], output_dir_path_obj / "hrefsToRefs.json", True)

    # Run data downloads chapter extraction
    print("Extracting data for download chapter... ...")
    data_downloads_data = data_downloads.extract_data_downloads(dig_parent_dir, file_ops.readfile)
    write_file(data_downloads_data, output_dir_path_obj / "dataChapter.json")

    # Run tables extraction
    print("Extracting tables... ...")
    table_info = tables.extract_all_tables(dig_parent_dir, file_ops.readfile)
    table_strings = table_info['tables']
    table_html_paths_to_nums = table_info['htmlPathsToTableFileNums']
    table_image_paths_to_figure_nums = tables.extract_all_table_image_htmls(dig_parent_dir, file_ops.readfile)
    write_file(table_strings, output_dir_path_obj / "tables.json")
    write_file(table_html_paths_to_nums, output_dir_path_obj / "tableHTMLPathsToNums.json")
    write_file(table_image_paths_to_figure_nums, output_dir_path_obj / "tableImagePathsToFigureNums.json")

    # Run artifacts extraction
    print("Extracting artifacts... ...")
    artifacts_summary = artifacts.extract_all_of_artifacts_dir(dig_parent_dir, file_ops.readfile)
    artifacts_details = artifacts.extract_appendix_b(dig_parent_dir, file_ops.readfile)
    art_images = artifacts.extract_all_artifacts_images(dig_parent_dir, file_ops.readfile)
    artifacts_by_cat_num = artifacts.generate_cat_num_to_artifacts_dict(artifacts_summary, artifacts_details, True)
    artifacts_full = artifacts.insert_details_into_summary_dict(artifacts_summary, artifacts_by_cat_num)
    artifacts_full = artifacts.replace_figure_paths_with_nums_in_summary_dict(artifacts_full, art_images)
    # Ignore artifacts_summary as it's currently mutated by the insert_details call
    # write_file(artifacts_summary, output_dir_path_obj / "artifactsSummary.json")
    write_file(artifacts_details, output_dir_path_obj / "artifactsDetails.json")
    write_file(art_images, output_dir_path_obj / "artifactsImages.json", True)
    write_file(artifacts_by_cat_num, output_dir_path_obj / "artifactsByCatNum.json", True)
    write_file(artifacts_full, output_dir_path_obj / "artifactsByExcElementComplete.json", True, True)
