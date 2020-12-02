from src.generate_new_site.utilities import path_ops
from pathlib import Path
import pytest

######################
# rel_path unit test #
######################

'''
@pytest.mark.parametrize("path,start,expected_result", [
    (None, None, None),
    (None, Path("start"), None),
    (None, Path("start.txt"), None),
    (Path("https://www.google.com"), Path("/usr"), Path("https://www.google.com")),
    (Path("http://www.google.com"), Path("/usr"), Path("http://www.google.com")),
    (Path("path"), None, Path("path")),
    (Path("/usr/name/home/test.txt"), Path("/usr"), Path("name/home/test.txt")),
    (Path("/usr/name/home/test.txt"), Path("/usr/start.txt"), Path("name/home/test.txt")),
    (Path("/usr/name/home/test.txt"), Path("/usr"), Path("name/home/test.txt")),
    (Path("dir1/dir2/dir3/test.html"), Path("dir1"), Path("dir2/dir3/test.html")),
    (Path("dir1/dir2/dir3/test.html"), Path("dir1/start.html"), Path("dir2/dir3/test.html")),
    (Path("dir1/dir2/dir3/test.html"), Path("dir1/differentdir"), Path("../dir2/dir3/test.html")),
    (Path("dir1/dir2/dir3/test.html"), Path("dir1/differentdir/start.html"), Path("../dir2/dir3/test.html")),
    (Path("dir1/dir2/dir3/test.html"), Path("dir1/differentdir/diffdiffdir"), Path("../../dir2/dir3/test.html"))
])
def test_rel_path(path, start, expected_result):
    assert path_ops.rel_path(path, start) == expected_result'''
