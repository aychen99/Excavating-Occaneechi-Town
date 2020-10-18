from .modules import standard_text_chapter, excavation_details_page, image_page, feature_descriptions
from .utilities import file_ops
import pathlib
import json
import datetime

def run_extraction(config):
    # Set up variables from config
    dig_parent_dir = config['digParentDirPath']
    output_dir_path = config['extractionOutputDirPath']
    output_dir_path_obj = None
    if output_dir_path == "Default":
        output_dir_path_obj = pathlib.Path(__file__).parent / "jsons"
    else:
        output_dir_path_obj = pathlib.Path(output_dir_path)
    output_dir_path_obj.mkdir(parents=True, exist_ok=True)
    overwrite_files = config['overwriteExistingExtractedData']

    def write_file(data, filename_path_obj, sort_keys):
        if not overwrite_files and filename_path_obj.is_file():
            pass
        else:
            with open(filename_path_obj, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=sort_keys)

    # Run text chapter extraction
    print("Extracting text chapters... ...")
    text_partnames = config['standardTextChapterPartnames']
    for partname in text_partnames:
        output_filename = output_dir_path_obj / (partname + ".json")
        data = standard_text_chapter.extract_standard_part(partname, dig_parent_dir, file_ops.readfile)
        write_file(data, output_filename, False)
    
    # Run excavations element pages extraction
    print("Extracting excavations element pages... ...")
    excavations_pages = excavation_details_page.extract_all_exc_pages(dig_parent_dir, file_ops.readfile)
    excavations_output_filename = output_dir_path_obj / "excavationsElements.json"
    write_file(excavations_pages, excavations_output_filename, False)
    
    # Run image pages extraction
    print("Extracting image pages... ...")
    images = image_page.extract_all_images(dig_parent_dir, file_ops.readfile)
    image_metadata_dicts = image_page.generate_metadata_dicts(images)
    images_output_filename = output_dir_path_obj / "images.json"
    write_file(images, images_output_filename, False)
    for dict_name, data in image_metadata_dicts.items():
        output_filename = output_dir_path_obj / (dict_name + ".json")
        write_file(data, output_filename, True)

    # Run feature description extraction
    print("Extracting feature descriptions... ...")
    descriptions = feature_descriptions.extract_descriptions(dig_parent_dir, file_ops.readfile)
    descriptions_output_filename = output_dir_path_obj / "descriptions.json"
    write_file(descriptions, descriptions_output_filename, True)
