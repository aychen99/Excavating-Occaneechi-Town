from modules import standard_text_chapter
from utilities import file_ops
import pathlib
import json
import datetime

if __name__ == "__main__":
    # Demo: Run full extraction code for Part 2
    # TODO: Load path of folder containing /dig from config file
    output_filename = ("Part 2 Extraction on "
                       + datetime.datetime.now().strftime("%Y-%m-%d at %H%M%S")
                       + ".txt")
    dig_parent_dir = "C:/" # Change on local machine to proper path
    data = standard_text_chapter.extract_standard_part("part2", dig_parent_dir, file_ops.readfile)
    with open(output_filename, 'w') as f:
        json.dump(data, f, indent=4)