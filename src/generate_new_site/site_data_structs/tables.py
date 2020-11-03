import json
from pathlib import Path

class Tables:
    def __init__(self, parent):
        self.tables = {}
        self.old_paths_to_table_nums = {}
        self.image_paths_to_figure_nums = None
        self.parent = parent
    
    def register_table(self, table_num, table_info):
        self.tables[table_num] = table_info
    
    def register_path(self, old_path, table_num):
        self.old_paths_to_table_nums[old_path] = table_num
    
    def register_image_paths(self, image_paths_to_figure_nums):
        self.image_paths_to_figure_nums = image_paths_to_figure_nums

    def get_table_by_num(self, table_num):
        if table_num in self.tables:
            return self.tables[table_num]
        return None
    
    def get_table_by_old_path(self, old_path):
        if old_path in self.old_paths_to_table_nums:
            table_num = self.old_paths_to_table_nums[old_path]
            return self.tables[table_num]
        return None
    
    def get_figure_num_by_html_path(self, image_html_path):
        if image_html_path in self.image_paths_to_figure_nums:
            return self.image_paths_to_figure_nums[image_html_path]
        return None

    @classmethod
    def from_json(
        cls,
        tables_json_path,
        old_table_dirs_json_path,
        image_paths_to_nums_json_path,
        index
    ):
        """
        Factory method for making a Tables object from a .json.

        Parameters
        ----------
        tables_json_path : Path
            Path to the json file containing the text of all the tables.
        old_table_dirs_json_path : Path
            Path to the json file with the dict of old paths to table nums.
        image_paths_to_nums_json_path : Path
            Path to the json file linking HTML page names to their figure nums.
        index : Index
            Root of the site tree.

        Returns
        -------
        tables: Tables
            A Tables class instance with all the tables loaded.
        """
        tables = Tables(parent=index)

        with tables_json_path.open() as f:
            table_objs = json.load(f)
        with old_table_dirs_json_path.open() as f:
            html_paths_to_nums = json.load(f)
        with image_paths_to_nums_json_path.open() as f:
            image_paths_to_figure_nums = json.load(f)

        for table_num, table_obj in table_objs.items():
            tables.register_table(table_num, table_obj)

        for path, table_num in html_paths_to_nums.items():
            tables.register_path(path, table_num)

        tables.register_image_paths(image_paths_to_figure_nums)

        return tables
