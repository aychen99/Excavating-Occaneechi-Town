import json
import pathlib
from src.extract_old_site.extract import run_extraction
from src.generate_new_site.generate import generate_site

if __name__ == "__main__":
    script_root_dir = pathlib.Path(__file__).parent

    config = None
    with open((script_root_dir / "config.json")) as f:
        config = json.load(f)

    # Resolve any default config values
    if config["extractionOutputDirPath"] == "Default":
        config["extractionOutputDirPath"] = str(script_root_dir / "jsons")
    if config["generationOutputDirPath"] == "Default":
        config["generationOutputDirPath"] = str(script_root_dir / "newdig")
        (script_root_dir / "newdig").mkdir(parents=True, exist_ok=True)

    
    # Set up for generating the site
    dig_dir = str((pathlib.Path(config["digParentDirPath"]) / "dig").as_posix())
    input_dir = config["extractionOutputDirPath"]
    output_dir = config["generationOutputDirPath"]
    overwrite_out = config["overwriteExistingGeneratedFiles"]
    copy_images = config["copyImages"]
    
    # Run extraction and site generation
    run_extraction(config)
    generate_site(dig_dir, input_dir, output_dir, overwrite_out, copy_images)
