from src.extract_old_site.utilities import file_ops
from unittest import mock
import pathlib
import pytest


index_html_mock_content = "<b>Excavating Occaneechi Town</b>"
version_html_mock_content = """
<html>
<head>
<title>Excavating Occaneechi Town - [Version Information]</title>
</head>

<body bgcolor="#ffffff">
</body>
</html>
"""

def mock_open(path_obj, open_type='r', encoding='utf-8'):
    if path_obj.as_posix() == "C:/dig/index.html":
        return index_html_mock_content
    elif path_obj.as_posix() == "C:/dig/html/version.html":
        return version_html_mock_content


def test_readfile():#filename, parent_dir_path_obj, expected_file_contents):
    with mock.patch("builtins.open", mock.mock_open(read_data=index_html_mock_content)) as mock_file:
        assert file_ops.readfile("index.html", pathlib.Path("C:/dig")) == index_html_mock_content
        mock_file.assert_called_with(pathlib.Path("C:/dig/index.html"), 'r', encoding='ISO-8859-1')
    with mock.patch("builtins.open", mock.mock_open(read_data=version_html_mock_content)) as mock_file:
        assert file_ops.readfile("version.html", pathlib.Path("C:/dig/html")) == version_html_mock_content
        mock_file.assert_called_with(pathlib.Path("C:/dig/html/version.html"), 'r', encoding='ISO-8859-1')
