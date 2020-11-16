from src.extract_old_site.modules import excavation_details_page as exc_det
import pathlib
import os
from unittest import mock
import pytest

# Structure 1, /dig/html/excavations/exc_is.html
exc_is_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<frameset cols="408,*" border=1>
<frame name="image" src="slid_azt.html" marginwidth=1 marginheight=1>
<frame name="ctrl" src="ctrl_is.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

ctrl_is_html_str = """
<html><frameset rows="75%,25%" border=1>
<frame name="info" src="info_is.html" marginwidth=1 marginheight=1>
<frame name="zoom" src="zoom_is.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

info_is_html_str = """
<html><body>
<big><b>Structure 1</b></big><p>
<img align="right" src="../images/l/l240r60.gif">
Type: Structure<br>
Dimensions<br>
&nbsp;&nbsp;Length: 13.4 ft<br>
&nbsp;&nbsp;Width: 11.3 ft<br>
&nbsp;&nbsp;Depth: Unknown ft<br>
Volume: Unknown ft<sup><small>3</small></sup><br>
Area: 115.88 ft<sup><small>2</small></sup><p>
<table border=2 width="100%">
<tr><td rowspan=4>Image:<br>
<a href="slid_azt.html" target="image">1</a>
<a href="slid_bdo.html" target="image">2</a>
<a href="slid_bet.html" target="image">3</a>
</td>
<td align="center"><a href="../artifacts/art_is0.html" target="_top">Artifacts</a></td></tr>
<tr><td align="center">Description</td></tr>
<tr><td align="center"><a href="../maps/exc2.html" target="_top">Map</a></td></tr>
<tr><td align="center"><a href="../index.html" target="_top">Home</a></td></tr>
</table></body></html>
"""

zoom_is_html_str = """
<html><body><big>Zoom To:</big><p>
<a href="exc_cl.html" target="_top">Feature 9</a><br>
<a href="exc_fg.html" target="_top">Sq. 240R60</a><br>
<a href="exc_fh.html" target="_top">Sq. 240R70</a><br>
<a href="exc_ft.html" target="_top">Sq. 250R60</a><br>
<a href="exc_fu.html" target="_top">Sq. 250R70</a><br>
</body></html>
"""

slid_azt_html_str = """
<html><body><map name="hotlinks">
<area coords="144,140,224,214" target="_top" href="exc_cl.html">
<area coords="38,78,80,127" target="_top" href="exc_au.html">
<area coords="359,292,388,361" target="_top" href="exc_am.html">
<area coords="364,134,389,198" target="_top" href="exc_iy.html">
<area coords="326,155,363,190" target="_top" href="exc_iy.html">
<area coords="305,3,363,154" target="_top" href="exc_iy.html">
<area coords="364,90,388,133" target="_top" href="exc_ae.html">
<area coords="364,3,389,89" target="_top" href="exc_iy.html">
</map><center><img src="../images/s/str1.gif" usemap="#hotlinks" border=0><p>Figure 1039. Structure 1, plan view (view to north).</center></body></html>
"""

slid_bdo_html_str = """
<html><body><map name="hotlinks">
<area coords="43,102,193,152" target="_top" href="exc_is.html">
<area coords="22,151,113,219" target="_top" href="exc_is.html">
<area coords="194,118,243,220" target="_top" href="exc_is.html">
<area coords="16,220,237,298" target="_top" href="exc_is.html">
<area coords="114,152,196,223" target="_top" href="exc_cl.html">
</map><center><img src="../images/x16/x6801.jpeg" usemap="#hotlinks" border=0><p>Figure 1038. Structure 1 at top of subsoil (view to southwest).</center></body></html>
"""

slid_bet_html_str = """
<html><body><map name="hotlinks">
</map><center><img src="../images/x16/x6968.jpeg" usemap="#hotlinks" border=0><p>Figure 1037. Structure 1 after excavation (view to southwest).</center></body></html>
"""

# Sq. 240R60, /dig/html/excavations/exc_fg.html
exc_fg_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<frameset cols="408,*" border=1>
<frame name="image" src="slid_ada.html" marginwidth=1 marginheight=1>
<frame name="ctrl" src="ctrl_fg.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

ctrl_fg_html_str = """
<html><frameset rows="75%,25%" border=1>
<frame name="info" src="info_fg.html" marginwidth=1 marginheight=1>
<frame name="zoom" src="zoom_fg.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

info_fg_html_str = """
<html><body>
<big><b>Sq. 240R60</b></big><p>
<img align="right" src="../images/l/l240r60.gif">
Type: Excavation Unit<br>
Dimensions<br>
&nbsp;&nbsp;Length: 10.0 ft<br>
&nbsp;&nbsp;Width: 10.0 ft<br>
&nbsp;&nbsp;Depth: 0.6 ft<br>
Volume: 61.06 ft<sup><small>3</small></sup><br>
Area: 100.00 ft<sup><small>2</small></sup><p>
<table border=2 width="100%">
<tr><td rowspan=4>Image:<br>
<a href="slid_ada.html" target="image">1</a>
<a href="slid_bde.html" target="image">2</a>
</td>
<td align="center"><a href="../artifacts/art_fg0.html" target="_top">Artifacts</a></td></tr>
<tr><td align="center">Description</td></tr>
<tr><td align="center"><a href="../maps/exc0.html" target="_top">Map</a></td></tr>
<tr><td align="center"><a href="../index.html" target="_top">Home</a></td></tr>
</table></body></html>
"""

zoom_fg_html_str = """
<html><body><big>Zoom To:</big><p>
<a href="exc_cl.html" target="_top">Feature 9</a><br>
<a href="exc_is.html" target="_top">Structure 1</a><br>
</body></html>
"""

slid_ada_html_str = """
<html><body><map name="hotlinks">
<area coords="70,283,388,389" target="_top" href="exc_is.html">
<area coords="149,197,386,282" target="_top" href="exc_is.html">
<area coords="343,1,388,197" target="_top" href="exc_is.html">
<area coords="14,1,148,282" target="_top" href="exc_is.html">
<area coords="149,0,342,196" target="_top" href="exc_cl.html">
</map><center><img src="../images/2/240r60.gif" usemap="#hotlinks" border=0><p>Figure 860. Sq. 240R60, top of subsoil (view to north).</center></body></html>
"""

slid_bde_html_str = """
<html><body><map name="hotlinks">
<area coords="175,100,312,160" target="_top" href="exc_cl.html">
<area coords="70,93,113,215" target="_top" href="exc_is.html">
</map><center><img src="../images/x16/x6730.jpeg" usemap="#hotlinks" border=0><p>Figure 859. Sq. 240R60 at top of subsoil (view to north).</center></body></html>
"""

# Extracted
slid_azt_extracted = {
    "path": "/dig/html/images/s/str1.gif",
    "htmlPagePath": "/dig/html/excavations/slid_azt.html",
    "figureNum": "1039",
    "caption": "Structure 1, plan view (view to north).",
    "clickableAreas": [
        {"x1": 144, "y1": 140, "x2": 224, "y2": 214,
            "path": "/dig/html/excavations/exc_cl.html"},
        {"x1": 38, "y1": 78, "x2": 80, "y2": 127,
            "path": "/dig/html/excavations/exc_au.html"},
        {"x1": 359, "y1": 292, "x2": 388, "y2": 361,
            "path": "/dig/html/excavations/exc_am.html"},
        {"x1": 364, "y1": 134, "x2": 389, "y2": 198,
            "path": "/dig/html/excavations/exc_iy.html"},
        {"x1": 326, "y1": 155, "x2": 363, "y2": 190,
            "path": "/dig/html/excavations/exc_iy.html"},
        {"x1": 305, "y1": 3, "x2": 363, "y2": 154,
            "path": "/dig/html/excavations/exc_iy.html"},
        {"x1": 364, "y1": 90, "x2": 388, "y2": 133,
            "path": "/dig/html/excavations/exc_ae.html"},
        {"x1": 364, "y1": 3, "x2": 389, "y2": 89,
            "path": "/dig/html/excavations/exc_iy.html"}
    ],
    "originalDimensions": {
        "width": 390,
        "height": 390
    }
}

slid_bdo_extracted = {
    "path": "/dig/html/images/x16/x6801.jpeg",
    "htmlPagePath": "/dig/html/excavations/slid_bdo.html",
    "figureNum": "1038",
    "caption": "Structure 1 at top of subsoil (view to southwest).",
    "clickableAreas": [
        {"x1": 43, "y1": 102, "x2": 193, "y2": 152,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 22, "y1": 151, "x2": 113, "y2": 219,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 194, "y1": 118, "x2": 243, "y2": 220,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 16, "y1": 220, "x2": 237, "y2": 298,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 114, "y1": 152, "x2": 196, "y2": 223,
            "path": "/dig/html/excavations/exc_cl.html"}
    ],
    "originalDimensions": {
        "width": 251,
        "height": 390
    }
}

slid_bet_extracted = {
    "path": "/dig/html/images/x16/x6968.jpeg",
    "htmlPagePath": "/dig/html/excavations/slid_bet.html",
    "figureNum": "1037",
    "caption": "Structure 1 after excavation (view to southwest).",
    "clickableAreas": [],
    "originalDimensions": {
        "width": 390,
        "height": 347
    }
}

slid_ada_extracted = {
    "path": "/dig/html/images/2/240r60.gif",
    "htmlPagePath": "/dig/html/excavations/slid_ada.html",
    "figureNum": "860",
    "caption": "Sq. 240R60, top of subsoil (view to north).",
    "clickableAreas": [
        {"x1": 70, "y1": 283, "x2": 388, "y2": 389,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 149, "y1": 197, "x2": 386, "y2": 282,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 343, "y1": 1, "x2": 388, "y2": 197,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 14, "y1": 1, "x2": 148, "y2": 282,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 149, "y1": 0, "x2": 342, "y2": 196,
            "path": "/dig/html/excavations/exc_cl.html"}
    ],
    "originalDimensions": {
        "width": 390,
        "height": 390
    }
}

slid_bde_extracted = {
    "path": "/dig/html/images/x16/x6730.jpeg",
    "htmlPagePath": "/dig/html/excavations/slid_bde.html",
    "figureNum": "859",
    "caption": "Sq. 240R60 at top of subsoil (view to north).",
    "clickableAreas": [
        {"x1": 175, "y1": 100, "x2": 312, "y2": 160,
            "path": "/dig/html/excavations/exc_is.html"},
        {"x1": 70, "y1": 93, "x2": 113, "y2": 215,
            "path": "/dig/html/excavations/exc_is.html"}
    ],
    "originalDimensions": {
        "width": 390,
        "height": 275
    }
}

info_is_extracted = {
    "name": "Structure 1",
    "miniMapIcon": "/dig/html/images/l/l240r60.gif",
    "info": {
        "Dimensions": {
            "Length": "13.4 ft",
            "Width": "11.3 ft",
            "Depth": "Unknown ft"
        },
        "Type": "Structure",
        "Volume": "Unknown ft<sup>3</sup>",
        "Area": "115.88 ft<sup>2</sup>"
    },
    "images": [slid_azt_extracted, slid_bdo_extracted, slid_bet_extracted],
    "artifactsPath": "/dig/html/artifacts/art_is0.html",
    "descriptionPath": None
}

info_fg_extracted = {
    "name": "Sq. 240R60",
    "miniMapIcon": "/dig/html/images/l/l240r60.gif",
    "info": {
        "Dimensions": {
            "Length": "10.0 ft",
            "Width": "10.0 ft",
            "Depth": "0.6 ft"
        },
        "Type": "Excavation Unit",
        "Volume": "61.06 ft<sup>3</sup>",
        "Area": "100.00 ft<sup>2</sup>"
    },
    "images": [slid_ada_extracted, slid_bde_extracted],
    "artifactsPath": "/dig/html/artifacts/art_fg0.html",
    "descriptionPath": None
}

zoom_is_extracted = [{
    "name": "Feature 9",
    "path": "/dig/html/excavations/exc_cl.html"
}, {
    "name": "Sq. 240R60",
    "path": "/dig/html/excavations/exc_fg.html"
}, {
    "name": "Sq. 240R70",
    "path": "/dig/html/excavations/exc_fh.html"
}, {
    "name": "Sq. 250R60",
    "path": "/dig/html/excavations/exc_ft.html"
}, {
    "name": "Sq. 250R70",
    "path": "/dig/html/excavations/exc_fu.html"
}]

zoom_fg_extracted = [{
    "name": "Feature 9",
    "path": "/dig/html/excavations/exc_cl.html"
}, {
    "name": "Structure 1",
    "path": "/dig/html/excavations/exc_is.html"
}]

ctrl_is_fully_extracted = {
    "name": "Structure 1",
    "miniMapIcon": "/dig/html/images/l/l240r60.gif",
    "info": {
        "Dimensions": {
            "Length": "13.4 ft",
            "Width": "11.3 ft",
            "Depth": "Unknown ft"
        },
        "Type": "Structure",
        "Volume": "Unknown ft<sup>3</sup>",
        "Area": "115.88 ft<sup>2</sup>"
    },
    "images": [slid_azt_extracted, slid_bdo_extracted, slid_bet_extracted],
    "artifactsPath": "/dig/html/artifacts/art_is0.html",
    "descriptionPath": None,
    "relatedElements": zoom_is_extracted
}

ctrl_fg_fully_extracted = {
    "name": "Sq. 240R60",
    "miniMapIcon": "/dig/html/images/l/l240r60.gif",
    "info": {
        "Dimensions": {
            "Length": "10.0 ft",
            "Width": "10.0 ft",
            "Depth": "0.6 ft"
        },
        "Type": "Excavation Unit",
        "Volume": "61.06 ft<sup>3</sup>",
        "Area": "100.00 ft<sup>2</sup>"
    },
    "images": [slid_ada_extracted, slid_bde_extracted],
    "artifactsPath": "/dig/html/artifacts/art_fg0.html",
    "descriptionPath": None,
    "relatedElements": zoom_fg_extracted
}

# fg, then is according to how mock_iterdir is defined later on
exc_dir_fully_extracted = [{
    "name": "Sq. 240R60",
    "miniMapIcon": "/dig/html/images/l/l240r60.gif",
    "info": {
        "Dimensions": {
            "Length": "10.0 ft",
            "Width": "10.0 ft",
            "Depth": "0.6 ft"
        },
        "Type": "Excavation Unit",
        "Volume": "61.06 ft<sup>3</sup>",
        "Area": "100.00 ft<sup>2</sup>"
    },
    "images": [slid_ada_extracted, slid_bde_extracted],
    "artifactsPath": "/dig/html/artifacts/art_fg0.html",
    "descriptionPath": None,
    "relatedElements": zoom_fg_extracted,
    "path": "/dig/html/excavations/exc_fg.html"
}, {
    "name": "Structure 1",
    "miniMapIcon": "/dig/html/images/l/l240r60.gif",
    "info": {
        "Dimensions": {
            "Length": "13.4 ft",
            "Width": "11.3 ft",
            "Depth": "Unknown ft"
        },
        "Type": "Structure",
        "Volume": "Unknown ft<sup>3</sup>",
        "Area": "115.88 ft<sup>2</sup>"
    },
    "images": [slid_azt_extracted, slid_bdo_extracted, slid_bet_extracted],
    "artifactsPath": "/dig/html/artifacts/art_is0.html",
    "descriptionPath": None,
    "relatedElements": zoom_is_extracted,
    "path": "/dig/html/excavations/exc_is.html"
}]

def mock_extract_image_page(image_html_str, extra1, extra2, extra3):
    if image_html_str == slid_ada_html_str:
        return slid_ada_extracted
    elif image_html_str == slid_azt_html_str:
        return slid_azt_extracted
    elif image_html_str == slid_bde_html_str:
        return slid_bde_extracted
    elif image_html_str == slid_bdo_html_str:
        return slid_bdo_extracted
    elif image_html_str == slid_bet_html_str:
        return slid_bet_extracted

    raise Exception("did not find details for this particular img string")


def mock_readfile(filename, parent_dir_path_obj):
    resolved_path_obj = pathlib.Path(os.path.normpath(parent_dir_path_obj / filename))
    filename = resolved_path_obj.name
    parent_dir_str = resolved_path_obj.parent.as_posix()
    if parent_dir_str == "C:/dig/html/excavations":
        # Structure 1
        if filename == "slid_azt.html":
            return slid_azt_html_str
        elif filename == "slid_bdo.html":
            return slid_bdo_html_str
        elif filename == "slid_bet.html":
            return slid_bet_html_str
        elif filename == "zoom_is.html":
            return zoom_is_html_str
        elif filename == "info_is.html":
            return info_is_html_str
        elif filename == "ctrl_is.html":
            return ctrl_is_html_str
        elif filename == "exc_is.html":
            return exc_is_html_str
        # Sq. 240R60, /dig/html/excavations/exc_fg.html
        elif filename == "exc_fg.html":
            return exc_fg_html_str
        elif filename == "ctrl_fg.html":
            return ctrl_fg_html_str
        elif filename == "info_fg.html":
            return info_fg_html_str
        elif filename == "zoom_fg.html":
            return zoom_fg_html_str
        elif filename == "slid_ada.html":
            return slid_ada_html_str
        elif filename == "slid_bde.html":
            return slid_bde_html_str

    raise Exception("did not find file in mock_readfile")


@pytest.mark.parametrize("zoom_html_str,expected_result", [
    (zoom_is_html_str, zoom_is_extracted),
    (zoom_fg_html_str, zoom_fg_extracted),
    ("""
     <html><body><big>Zoom To:</big><p>
     <a href="exc_gw.html" target="_top">Sq. 270R90</a><br>
     <a href="exc_gn.html" target="_top">Sq. 270R100</a><br>
     </body></html>
     """, [{
        "name": "Sq. 270R90",
        "path": "/dig/html/excavations/exc_gw.html"
    }, {
        "name": "Sq. 270R100",
        "path": "/dig/html/excavations/exc_gn.html"
    }])
])
def test_extract_zoom_to(zoom_html_str, expected_result):
    assert exc_det.extract_zoom_to(zoom_html_str) == expected_result

@mock.patch("src.extract_old_site.modules.excavation_details_page.extract_image_page")
@pytest.mark.parametrize("info_html_str,expected_result", [
    (info_fg_html_str, info_fg_extracted),
    (info_is_html_str, info_is_extracted)
])
def test_extract_info_page(mock_ext_i_p, info_html_str, expected_result):
    mock_ext_i_p.side_effect = mock_extract_image_page
    assert exc_det.extract_info_page(
        info_html_str, "/dig/html/excavations", "C:/", mock_readfile
    ) == expected_result

@mock.patch("src.extract_old_site.modules.excavation_details_page.extract_image_page")
@pytest.mark.parametrize("ctrl_html_str,expected_result", [
    (ctrl_fg_html_str, ctrl_fg_fully_extracted),
    (ctrl_is_html_str, ctrl_is_fully_extracted)
])
def test_get_ctrl_page_contents(mock_ext_i_p, ctrl_html_str, expected_result):
    mock_ext_i_p.side_effect = mock_extract_image_page
    assert exc_det.get_ctrl_page_contents(
        ctrl_html_str, "/dig/html/excavations", "C:/", mock_readfile
    ) == expected_result

@mock.patch("src.extract_old_site.modules.excavation_details_page.extract_image_page")
@pytest.mark.parametrize("exc_html_str,expected_result", [
    (exc_fg_html_str, ctrl_fg_fully_extracted),
    (exc_is_html_str, ctrl_is_fully_extracted)
])
def test_get_exc_page_contents(mock_ext_i_p, exc_html_str, expected_result):
    mock_ext_i_p.side_effect = mock_extract_image_page
    assert exc_det.get_exc_page_contents(
        exc_html_str, "/dig/html/excavations", "C:/", mock_readfile
    ) == expected_result

@mock.patch("src.extract_old_site.modules.excavation_details_page.extract_image_page")
def test_extract_all_exc_pages(mock_ext_i_p):
    mock_ext_i_p.side_effect = mock_extract_image_page
    with mock.patch.object(pathlib.Path, "iterdir") as mock_iterdir:
        filenames_list = [
            "exc_fg.html", "exc_is.html", "info_fg.html", "info_is.html",
            "slid_ada.html", "slid_azt.html", "slid_bde.html", "slid_bdo.html", "slid_bet.html",
            "zoom_fg.html", "zoom_is.html",
        ]
        iterdir_path_objs = [(pathlib.Path("C:/dig/html/excavations") / filename)
                             for filename in filenames_list]
        mock_iterdir.return_value = iterdir_path_objs

        assert exc_det.extract_all_exc_pages("C:/", mock_readfile) == exc_dir_fully_extracted
