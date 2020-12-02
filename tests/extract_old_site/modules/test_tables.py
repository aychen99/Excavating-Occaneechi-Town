from src.extract_old_site.modules import tables
import pytest
from unittest import mock
from pathlib import Path

# Partial sample from /dig/html/tables/body3.html
body3_html_str = """
<html><body>
<pre>===================================================================================
 Vessel No. (click to view pot)
 |   % of    Rim      Neck   Shoulder            Wall
 |   Rim   Diameter Diameter Diameter  Height  Thickness       Location
===================================================================================
 <a href="tab3_0.html">1</a>   15%    16 cm    16 cm        -        -   8-10 mm   Feature 8, Cleaning Top
 <a href="tab3_1.html">2</a>    6%    28 cm        -        -        -    4-6 mm   Burial 1, Zone 1
 <a href="tab3_2.html">3</a>   12%    16 cm    13 cm    15 cm        -    2-4 mm   Burial 2, Zone 1
 <a href="tab3_3.html">4</a>    6%    34 cm        -        -        -    4-6 mm   Burial 3, Zone 1
 <a href="tab3_4.html">5</a>    9%    10 cm        -        -        -    6-8 mm   Burial 3, Zone 1
 <a href="tab3_5.html">6</a>  100%    14 cm    11 cm    12 cm    12 cm    4-6 mm   Burial 2, Association
 <a href="tab3_6.html">7</a>  100%    17 cm    14 cm    16 cm    18 cm    4-6 mm   Burial 6, Association
 <a href="tab3_7.html">8</a>  100%    14 cm    11 cm    12 cm    12 cm    4-6 mm   Burial 8, Association
 <a href="tab3_8.html">9</a>  100%    19 cm        -        -    10 cm    &gt;10 mm   Burial 11, Association
<a href="tab3_9.html">10</a>   35%    12 cm    11 cm    11 cm        -    4-6 mm   Feature 17, Zone 1
================================================================================</pre>
<p><center><hr><a href="../part1/tab3.html" target="_top">Back</a></center>
</body></html>
"""

# Partial sample from /dig/html/tables/body6.html
body6_html_str = """
<html><body>
<pre>===================================================================
 Functional Group               Plowzone and
   Class/Artifact Type            Features   Burials    Total
===================================================================

 Architecture
  (Construction Fasteners)
      Nails                          84         26       110
      Tacks                           -          3         3
      Nuts                            2          -         2
      Bolts/Spikes                    3          -         3
  (Building Materials)
      Brick Fragments               231          1       232
      Glazed Brick Fragments         17          3        20
      Window Glass Fragments         49          -        49
         Sub-Totals                 386         33       419
                        
 Totals (excluding                1,539     13,480    15,020
  unidentified artifacts)                  
=================================================================</pre>
<p><center><hr><a href="../part1/tab3.html" target="_top">Back</a></center>
</body></html>
"""

# /dig/html/tables/head3.html
head3_html_str = """
<html><body><center>Table 4. Metric attributes and contexts for whole vessels and reconstructed vessel sections from the Fredricks site.</center></body></html>
"""

# /dig/html/tables/head6.html
head6_html_str = """
<html><body><center>Table 7. Historic artifacts found at the Fredricks site.</center></body></html>
"""

# /dig/html/tables/table3.html
table3_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<frameset rows="28,*" border=1>
<frame scrolling="no" src="head3.html" marginwidth=1 marginheight=1>
<frame src="body3.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# /dig/html/tables/table6.html
table6_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<frameset rows="28,*" border=1>
<frame scrolling="no" src="head6.html" marginwidth=1 marginheight=1>
<frame src="body6.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# /dig/html/tables/tab2_4.html
tab2_4_image_page_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<body><center><img src="../images/d/d_3559.gif" border=0><p>Figure 121. Vessel 5, a Fredricks Plain bowl from Burial 3 (RLA catalog no. 2351p441/2).<p><hr><a href="body2.html">Back</a></center></body></html>
"""

# /dig/html/tables/tab2_6.html
tab2_6_image_page_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<body><center><img src="../images/d/d_3166.gif" border=0><p>Figure 107. Vessel 7, a Fredricks Check Stamped pot from Burial 6 (RLA catalog no. 2351p2240).<p><hr><a href="body2.html">Back</a></center></body></html>
"""

# /dig/html/tables/tab3_6.html
tab3_6_image_page_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<body><center><img src="../images/d/d_3166.gif" border=0><br>Figure 107. Vessel 7, a Fredricks Check Stamped pot from Burial 6 (RLA catalog no. 2351p2240).<p><hr><a href="body3.html">Back</a></center></body></html>
"""




body3_table_str = """===================================================================================
 Vessel No. (click to view pot)
 |   % of    Rim      Neck   Shoulder            Wall
 |   Rim   Diameter Diameter Diameter  Height  Thickness       Location
===================================================================================
 <a href="tab3_0.html">1</a>   15%    16 cm    16 cm        -        -   8-10 mm   Feature 8, Cleaning Top
 <a href="tab3_1.html">2</a>    6%    28 cm        -        -        -    4-6 mm   Burial 1, Zone 1
 <a href="tab3_2.html">3</a>   12%    16 cm    13 cm    15 cm        -    2-4 mm   Burial 2, Zone 1
 <a href="tab3_3.html">4</a>    6%    34 cm        -        -        -    4-6 mm   Burial 3, Zone 1
 <a href="tab3_4.html">5</a>    9%    10 cm        -        -        -    6-8 mm   Burial 3, Zone 1
 <a href="tab3_5.html">6</a>  100%    14 cm    11 cm    12 cm    12 cm    4-6 mm   Burial 2, Association
 <a href="tab3_6.html">7</a>  100%    17 cm    14 cm    16 cm    18 cm    4-6 mm   Burial 6, Association
 <a href="tab3_7.html">8</a>  100%    14 cm    11 cm    12 cm    12 cm    4-6 mm   Burial 8, Association
 <a href="tab3_8.html">9</a>  100%    19 cm        -        -    10 cm    &gt;10 mm   Burial 11, Association
<a href="tab3_9.html">10</a>   35%    12 cm    11 cm    11 cm        -    4-6 mm   Feature 17, Zone 1
================================================================================"""

body6_table_str = """===================================================================
 Functional Group               Plowzone and
   Class/Artifact Type            Features   Burials    Total
===================================================================

 Architecture
  (Construction Fasteners)
      Nails                          84         26       110
      Tacks                           -          3         3
      Nuts                            2          -         2
      Bolts/Spikes                    3          -         3
  (Building Materials)
      Brick Fragments               231          1       232
      Glazed Brick Fragments         17          3        20
      Window Glass Fragments         49          -        49
         Sub-Totals                 386         33       419
                        
 Totals (excluding                1,539     13,480    15,020
  unidentified artifacts)                  
================================================================="""

head3_extracted = {
    "tableNum": "4",
    "caption": "Metric attributes and contexts for whole vessels and reconstructed vessel sections from the Fredricks site."
}

head6_extracted = {
    "tableNum": "7",
    "caption": "Historic artifacts found at the Fredricks site."
}

tab2_4_extracted = {
    "path": "/html/images/d/d_3559.gif",
    "figureNum": "121",
    "caption": "Vessel 5, a Fredricks Plain bowl from Burial 3 (RLA catalog no. 2351p441/2)."
}

tab2_6_extracted = {
    "path": "/html/images/d/d_3166.gif",
    "figureNum": "107",
    "caption": "Vessel 7, a Fredricks Check Stamped pot from Burial 6 (RLA catalog no. 2351p2240)."
}

tab3_6_extracted = {
    "path": "/html/images/d/d_3166.gif",
    "figureNum": "107",
    "caption": "Vessel 7, a Fredricks Check Stamped pot from Burial 6 (RLA catalog no. 2351p2240)."
}

def mock_ext_t_h(header_html):
    if header_html == head3_html_str:
        return head3_extracted
    elif header_html == head6_html_str:
        return head6_extracted

def mock_ext_b_p(body_html):
    if body_html == body3_html_str:
        return body3_table_str
    elif body_html == body6_html_str:
        return body6_table_str

def mock_readfile(filename, parent_dir_path_obj):
    if parent_dir_path_obj.as_posix() != "C:/dig/html/tables":
        raise Exception("Failed test")
    if filename == "table3.html":
        return table3_html_str
    elif filename == "table6.html":
        return table6_html_str
    elif filename == "body3.html":
        return body3_html_str
    elif filename == "body6.html":
        return body6_html_str
    elif filename == "head3.html":
        return head3_html_str
    elif filename == "head6.html":
        return head6_html_str
    elif filename == "tab2_4.html":
        return tab2_4_image_page_html_str
    elif filename == "tab2_6.html":
        return tab2_6_image_page_html_str
    elif filename == "tab3_6.html":
        return tab3_6_image_page_html_str

    raise Exception("did not find filename in mock_readfile")


@pytest.mark.parametrize("body_html_str,expected_table_str", [
    (body3_html_str, body3_table_str),
    (body6_html_str, body6_table_str)
])
def test_extract_body_page(body_html_str, expected_table_str):
    assert tables.extract_body_page(body_html_str) == expected_table_str


@pytest.mark.parametrize("head_html_str,expected_header_info", [
    (head3_html_str, head3_extracted),
    (head6_html_str, head6_extracted)
])
def test_extract_table_header(head_html_str, expected_header_info):
    assert tables.extract_table_header(head_html_str) == expected_header_info


@mock.patch("src.extract_old_site.modules.tables.extract_table_header", mock_ext_t_h)
@mock.patch("src.extract_old_site.modules.tables.extract_body_page", mock_ext_b_p)
@mock.patch("src.extract_old_site.utilities.file_ops.readfile", mock_readfile)
@pytest.mark.parametrize("table_html_file_str,head_extracted,body_extracted", [
    (table3_html_str, head3_extracted, body3_table_str),
    (table6_html_str, head6_extracted, body6_table_str)
])
def test_extract_top_level_table_html(
    table_html_file_str, head_extracted, body_extracted
):
    assert tables.extract_top_level_table_html(table_html_file_str, "C:/dig", mock_readfile) == {
        "tableNum": head_extracted["tableNum"],
        "caption": head_extracted["caption"],
        "table": body_extracted
    }


@mock.patch("src.extract_old_site.utilities.file_ops.readfile", mock_readfile)
def test_extract_all_tables():
    with mock.patch.object(Path, 'iterdir') as mock_iterdir:
        filenames = [
            "table3.html", "table6.html", "body3.html", "body6.html",
            "head3.html", "head6.html"
        ]
        iterdir_paths = [(Path("C:/dig/html/tables") / filename)
                         for filename in filenames]
        mock_iterdir.return_value = iterdir_paths
        assert tables.extract_all_tables("C:/dig", mock_readfile) == {
            "tables": {
                "3": {
                    "tableNum": head3_extracted["tableNum"],
                    "caption": head3_extracted["caption"],
                    "table": body3_table_str
                },
                "6": {
                    "tableNum": head6_extracted["tableNum"],
                    "caption": head6_extracted["caption"],
                    "table": body6_table_str
                }
            },
            "htmlPathsToTableFileNums": {
                "/html/tables/table3.html": "3",
                "/html/tables/table6.html": "6"
            }
        }


@pytest.mark.parametrize("image_page_html_str,expected_result", [
    (tab2_4_image_page_html_str, tab2_4_extracted),
    (tab2_6_image_page_html_str, tab2_6_extracted),
    (tab3_6_image_page_html_str, tab3_6_extracted)
])
def test_extract_table_image(image_page_html_str, expected_result):
    assert tables.extract_table_image(image_page_html_str) == expected_result


@mock.patch("src.extract_old_site.utilities.file_ops.readfile", mock_readfile)
def test_extract_all_table_image_htmls():
    with mock.patch.object(Path, 'iterdir') as mock_iterdir:
        filenames = ["tab2_4.html", "tab2_6.html", "tab3_6.html"]
        iterdir_paths = [(Path("C:/dig/html/tables") / filename)
                         for filename in filenames]
        mock_iterdir.return_value = iterdir_paths
        assert tables.extract_all_table_image_htmls("C:/dig", mock_readfile) == {
            "tab2_4.html": "121",
            "tab2_6.html": "107",
            "tab3_6.html": "107"
        }
