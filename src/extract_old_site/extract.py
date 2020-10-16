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

    # Run text chapter extraction
    text_partnames = config['standardTextChapterPartnames']
    for partname in text_partnames:
        output_filename = output_dir_path_obj / (partname + ".json")
        data = standard_text_chapter.extract_standard_part(partname, dig_parent_dir, file_ops.readfile)
        with open(output_filename, 'w') as f:
            json.dump(data, f, indent=4)
    
    # Run excavations element pages extraction
    excavations_pages = excavation_details_page.extract_all_exc_pages(dig_parent_dir, file_ops.readfile)
    excavations_output_filename = output_dir_path_obj / "excavationsElements.json"
    with open(excavations_output_filename, 'w') as f:
        json.dump(excavations_pages, f, indent=4)
    
    # Run image pages extraction
    images = image_page.extract_all_images(dig_parent_dir, file_ops.readfile)
    image_metadata_dicts = image_page.generate_metadata_dicts(images)
    images_output_filename = output_dir_path_obj / "images.json"
    with open(images_output_filename, 'w') as f:
        json.dump(images, f, indent=4)
    for dict_name, data in image_metadata_dicts.items():
        output_filename = output_dir_path_obj / (dict_name + ".json")
        with open(output_filename, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    # Run feature description extraction
    descriptions = feature_descriptions.extract_descriptions(dig_parent_dir, file_ops.readfile)
    descriptions_output_filename = output_dir_path_obj / "descriptions.json"
    with open(descriptions_output_filename, 'w') as f:
        json.dump(descriptions, f, indent=4, sort_keys=True)
