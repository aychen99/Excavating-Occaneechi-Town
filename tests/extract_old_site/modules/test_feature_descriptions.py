from src.extract_old_site.modules import feature_descriptions as desc
import pytest
from unittest import mock
import pathlib
import os

# Test Data
# Sidebar
index0_html_str = """
<html><body>
<b>Descriptions</b><p>
<a target="body" href="../split/report53.html">Burial 1 Description</a><br>
<a target="body" href="../split/report62.html">Feature 7 (Burial 9) Description</a><br>
<a target="body" href="../split/report63.html">Feature 8 Description</a><br>
</body></html>
"""

# Topbar
tabs0_html_str = """
<html><body><b>Descriptions | <a target="_parent" href="../index.html">Home</a></b></body></html>
"""

# Burial 1
tab0_html_str = """
<html><head><title>Excavating Occaneechi Town - [Descriptions]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

body0_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report53.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

report53_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report53a.html" marginwidth=1 marginheight=1>
<frame src="report53b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report53c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report53a_html_str = """
<html><body><center><b>Burial 1 Description</b>
</center></body></html>
"""

report53b_html_str = """
<html><body bgcolor=white>
by H. Trawick Ward<p>
<p>
<i>Grave Goods</i><p>
<p>
	Over the sternum were a <a href="../excavations/slid_aho.html" target="body"><u>large shell
gorget</u></a> and a
<a href="../excavations/slid_ahp.html" target="body"><u>small shell gorget</u></a> with punctated designs.<p>
</body></html>
"""

report53c_html_str = "<html><body><center>Page 21</center></body></html>"

# Feature 7 (Burial 9)
tab0_10_html_str = """
<html><head><title>Excavating Occaneechi Town - [Descriptions]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_10.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

body0_10_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report62.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

report62_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report62a.html" marginwidth=1 marginheight=1>
<frame src="report62b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report62c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report62a_html_str = """
<html><body><center><b>Feature 7 (Burial 9) Description</b>
</center></body></html>
"""

report62b_html_str = """
<html><body bgcolor=white>
by H. Trawick Ward<p>
<p>
<i>Grave Goods</i><p>
<p>
	Associated artifacts consisted of an <a href="../excavations/slid_akr.html" target="body"><u>iron hoe</u></a> placed adjacent to and southwest of the skull
(the blade end lay under the shoulder and occipital region of the skull) and a
bone-handled <a href="../excavations/slid_aks.html" target="body"><u>iron knife</u></a> placed under the right forearm.<p>
</body></html>
"""

report62c_html_str = "<html><body><center>Page 30</center></body></html>"

# Feature 8
tab0_11_html_str = """
<html><head><title>Excavating Occaneechi Town - [Descriptions]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_11.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

body0_11_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report63.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

report63_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report63a.html" marginwidth=1 marginheight=1>
<frame src="report63b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report63c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report63a_html_str = """
<html><body><center><b>Feature 8 Description</b>
</center></body></html>
"""

report63b_html_str = """
<html><body bgcolor=white>
by R. P. Stephen Davis, Jr.<p>
<p>
	Feature 8 was located just east of Structure 7 at 290.0R58.0.  At the top of
subsoil, this feature appeared as an irregular patch of brown loam, about 2.0
ft in diameter, that contained bits of charcoal, animal bone, fired clay, and a
large net-impressed rimsherd.<p>
</body></html>
"""

report63c_html_str = "<html><body><center>Page 31</center></body></html>"


# Extracted data
report53a_extracted = "Burial 1 Description"
report62a_extracted = "Feature 7 (Burial 9) Description"
report63a_extracted = "Feature 8 Description"

# Also removes all the double spaces in the paragraphs
reports53_62_63_fully_extracted = {
    "module": {
        "author": None,
        "shortTitle": "Feature Descriptions",
        "fullTitle": "Feature Descriptions",
        "path": "/dig/html/descriptions/tab0.html",
        "sections": [{
            "name": "Burial 1 Description",
            "path": "/dig/html/split/report53.html",
            "pageNum": "21",
            "subsections": []
        }, {
            "name": "Feature 7 (Burial 9) Description",
            "path": "/dig/html/split/report62.html",
            "pageNum": "30",
            "subsections": []
        }, {
            "name": "Feature 8 Description",
            "path": "/dig/html/split/report63.html",
            "pageNum": "31",
            "subsections": []
        }]
    },
    "pages": {
        "21": {
            "pageTitle": "Burial 1 Description",
            "parentModuleShortTitle": "Feature Descriptions",
            "content": [{
                "type": "italic-title",
                "content": "Grave Goods"    
            }, {
                "type": "paragraph",
                "content": ('Over the sternum were a <a href="/dig/html/excavations/slid_aho.html" target="body">'
                            '<u>large shell gorget</u></a> and a '
                            '<a href="/dig/html/excavations/slid_ahp.html" target="body"><u>'
                            'small shell gorget</u></a> with punctated designs.')
            }]
        },
        "30": {
            "pageTitle": "Feature 7 (Burial 9) Description",
            "parentModuleShortTitle": "Feature Descriptions",
            "content": [{
                "type": "italic-title",
                "content": "Grave Goods"
            }, {
                "type": "paragraph",
                "content": ('Associated artifacts consisted of an <a href="/dig/html/excavations/slid_akr.html" target="body">'
                            '<u>iron hoe</u></a> placed adjacent to and southwest of the skull '
                            '(the blade end lay under the shoulder and occipital region of the skull) and a '
                            'bone-handled <a href="/dig/html/excavations/slid_aks.html" target="body">'
                            '<u>iron knife</u></a> placed under the right forearm.')
            }]
        },
        "31": {
            "pageTitle": "Feature 8 Description",
            "parentModuleShortTitle": "Feature Descriptions",
            "content": [{
                "type": "paragraph",
                "content": ('Feature 8 was located just east of Structure 7 at 290.0R58.0. At the top of '
                            'subsoil, this feature appeared as an irregular patch of brown loam, about 2.0 '
                            'ft in diameter, that contained bits of charcoal, animal bone, fired clay, and a '
                            'large net-impressed rimsherd.')
            }]
        }
    }
}

report53c_extracted = "21"
report62c_extracted = "30"
report63c_extracted = "31"



def mock_readfile(filename, parent_dir_path_obj):
    resolved_path_obj = pathlib.Path(os.path.normpath(parent_dir_path_obj / filename))
    filename = resolved_path_obj.name
    parent_dir_str = resolved_path_obj.parent.as_posix()
    if parent_dir_str == "C:/dig/html/descriptions":
        if filename == "index0.html":
            return index0_html_str
        elif filename == "tabs0.html":
            return tabs0_html_str
        elif filename == "tab0.html":
            return tab0_html_str
        elif filename == "tab0_10.html":
            return tab0_10_html_str
        elif filename == "tab0_11.html":
            return tab0_11_html_str
        elif filename == "body0.html":
            return body0_html_str
        elif filename == "body0_10.html":
            return body0_10_html_str
        elif filename == "body0_11.html":
            return body0_11_html_str
    elif parent_dir_str == "C:/dig/html/split":
        if filename == "report53.html":
            return report53_html_str
        if filename == "report53a.html":
            return report53a_html_str
        if filename == "report53b.html":
            return report53b_html_str
        if filename == "report53c.html":
            return report53c_html_str
        elif filename == "report62.html":
            return report62_html_str
        elif filename == "report62a.html":
            return report62a_html_str
        elif filename == "report62b.html":
            return report62b_html_str
        elif filename == "report62c.html":
            return report62c_html_str
        elif filename == "report63.html":
            return report63_html_str
        elif filename == "report63a.html":
            return report63a_html_str
        elif filename == "report63b.html":
            return report63b_html_str
        elif filename == "report63c.html":
            return report63c_html_str

    raise Exception("did not find file in mock_readfile")


def test_extract_sidebar_sections():
    assert desc.extract_sidebar_sections(index0_html_str) == [{
        "name": "Burial 1 Description",
        "path": "/dig/html/split/report53.html",
        "subsections": []
    }, {
        "name": "Feature 7 (Burial 9) Description",
        "path": "/dig/html/split/report62.html",
        "subsections": []
    }, {
        "name": "Feature 8 Description",
        "path": "/dig/html/split/report63.html",
        "subsections": []
    }]

@pytest.mark.parametrize("report_a_html_str,expected_result", [
    (report53a_html_str, report53a_extracted),
    (report62a_html_str, report62a_extracted),
    (report63a_html_str, report63a_extracted)
])
def test_extract_page_title(report_a_html_str, expected_result):
    assert desc.extract_page_title(report_a_html_str) == expected_result

def test_extract_descriptions():
    with mock.patch.object(pathlib.Path, "iterdir") as mock_iterdir:
        filenames_list = [
            "body0.html", "body0_10.html", "body0_11.html", "index0.html",
            "tab0.html", "tab0_10.html", "tab0_11.html", "tabs0.html"
        ]
        iterdir_path_objs = [(pathlib.Path("C:/dig/html/descriptions") / filename)
                             for filename in filenames_list]
        mock_iterdir.return_value = iterdir_path_objs

        assert desc.extract_descriptions("C:/", mock_readfile) == reports53_62_63_fully_extracted
