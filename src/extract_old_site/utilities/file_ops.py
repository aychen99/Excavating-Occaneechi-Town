import pathlib

def readfile(filename, current_dir_path):
    """Return the contents of a file as a string given a Path object to it.
    Parameters
    ----------
    filename : str
        Name of the file to read.
    current_dir_path : Path
        pathlib.Path object for where the file is found on the system.
    """
    file_path = current_dir_path / filename
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        return f.read()
