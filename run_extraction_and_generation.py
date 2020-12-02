import json
import pathlib
from src.extract_old_site.extract import run_extraction
from src.generate_new_site.generate import generate_site

if __name__ == "__main__":
    script_root_dir = pathlib.Path(__file__).parent

    config = None
    with open((script_root_dir / "config.json")) as f:
        config = json.load(f)

    # Leave resolving of default config values to extract.py and generate.py

    # Set up for generating the site
    dig_dir = (pathlib.Path(config["digParentDirPath"]) / "dig").as_posix()
    digpro_dir = (pathlib.Path(config["digParentDirPath"]) / "digpro").as_posix()
    input_dir = config["extractionOutputDirPath"]
    output_dir = config["generationOutputDirPath"]
    overwrite_out = config["overwriteExistingGeneratedFiles"]
    copy_images = config["copyImages"]
    copy_videos = config["copyVideos"]
    copy_data = config["copyData"]

    # Run extraction and site generation
    if config['runExtraction']:
        print("\n-----------------------------------\n"
              "Extracting old site data.\n")
        run_extraction(config, version="dig")
        if config['runDigPro']:
            run_extraction(config, version="digpro")
    else:
        print("\n-----------------------------------\n"
              "SKIPPING extracting old site data.\n")
    if config['runGeneration']:
        print("\n-----------------------------------\n"
              "Generating new site files.\n")
        generate_site(dig_dir, input_dir, output_dir, overwrite_out, copy_images, copy_videos, copy_data, version="dig")
        if config['runDigPro']:
            generate_site(digpro_dir, input_dir, output_dir, overwrite_out, copy_images, copy_videos, copy_data, version="digpro")
    else:
        print("\n-----------------------------------\n"
              "SKIPPING generating new site files.\n")
