import json
from pathlib import Path

class References:
    def __init__(self, parent):
        self.references = {}
        self.old_reference_letters = {}
        self.parent = parent
    
    def register_author(self, author, references):
        self.references[author] = references
    
    def register_old_letters(self, letters, ref_info):
        self.old_reference_letters[letters] = ref_info
    
    def get_references_by_author(self, author):
        if author in self.references:
            return self.references[author]
        return None
    
    def get_reference_by_letters(self, letters):
        if letters in self.old_reference_letters:
            ref_info = self.old_reference_letters[letters]
            author = ref_info['author']
            ref_num = ref_info['refNum']
            return {
                "author": author,
                "reference": self.references[author][ref_num]
            }
        return None

    @classmethod
    def from_json(cls, refs_json_path, old_ref_letters_json_path, index):
        """
        Factory method for making a References object from a .json.

        Parameters
        ----------
        refs_json_path : Path
            Path to the json file containing the text of all the references.
        old_ref_letters_json_path : Path
            Path to the json file containing the dict of letters to their ref.
        index : Index
            Root of the site tree.

        Returns
        -------
        references: References
            A References class instance with all the references loaded.
        """
        references = References(parent=index)

        with refs_json_path.open() as f:
            all_refs = json.load(f)
        with old_ref_letters_json_path.open() as f:
            letters_to_refs = json.load(f)

        for author, reference_items in all_refs.items():
            references.register_author(author, reference_items)

        for letters, ref_info in letters_to_refs.items():
            references.register_old_letters(letters, ref_info)

        return references
