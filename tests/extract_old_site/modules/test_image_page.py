from src.extract_old_site.modules import image_page
from unittest import mock
import pytest
import pathlib
from PIL import Image
import os


# Test data: image slid.html's from Structure 1 (exc_is.html)
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


# Expected results
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


def mock_readfile(orig_filename, parent_dir_path_obj):
    resolved_path_obj = pathlib.Path(os.path.normpath(pathlib.Path(parent_dir_path_obj) / orig_filename))
    path_str = resolved_path_obj.as_posix()
    if path_str == "C:/dig/html/excavations/slid_azt.html":
        return slid_azt_html_str
    elif path_str == "C:/dig/html/excavations/slid_bdo.html":
        return slid_bdo_html_str
    elif path_str == "C:/dig/html/excavations/slid_bet.html":
        return slid_bet_html_str


@pytest.mark.parametrize("html_string,img_page_parent_dir,current_page_name,expected", [
    (slid_azt_html_str, "/dig/html/excavations", "slid_azt.html", slid_azt_extracted),
    (slid_bdo_html_str, "/dig/html/excavations", "slid_bdo.html", slid_bdo_extracted),
    (slid_bet_html_str, "/dig/html/excavations", "slid_bet.html", slid_bet_extracted)
])
def test_extract_image_page(html_string, img_page_parent_dir, current_page_name, expected):
    with mock.patch.object(Image, "open") as mock_PIL_Image:
        def mock_create_image_with_proper_size(image_path_obj):
            resolved_image_path_obj = pathlib.Path(os.path.normpath(image_path_obj))
            image_path_str = resolved_image_path_obj.as_posix()
            if image_path_str == "C:/dig/html/images/s/str1.gif":
                return Image.new("1", (390, 390))
            elif image_path_str == "C:/dig/html/images/x16/x6801.jpeg":
                return Image.new("1", (251, 390))
            elif image_path_str == "C:/dig/html/images/x16/x6968.jpeg":
                return Image.new("1", (390, 347))
            
            raise Exception("didn't find image")
                 
        mock_PIL_Image.side_effect = mock_create_image_with_proper_size
        assert image_page.extract_image_page(
            html_string, img_page_parent_dir, "C:/", current_page_name
        ) == expected

# TODO
# def test_get_image_dimensions():
#     pass

# TODO
# def test_extract_video_image_page():
#     pass

def test_extract_all_images():
    with mock.patch.object(pathlib.Path, "iterdir") as mock_iterdir:
        iterdir_path_objs = ["slid_azt.html", "slid_bdo.html", "slid_bet.html"]
        iterdir_path_objs = [(pathlib.Path("C:/dig/html/excavations") / filename)
                            for filename in iterdir_path_objs]
        mock_iterdir.return_value = iterdir_path_objs

        with mock.patch.object(Image, "open") as mock_PIL_Image:
            def mock_create_image_with_proper_size(image_path_obj):
                resolved_image_path_obj = pathlib.Path(os.path.normpath(image_path_obj))
                image_path_str = resolved_image_path_obj.as_posix()
                if image_path_str == "C:/dig/html/images/s/str1.gif":
                    return Image.new("1", (390, 390))
                elif image_path_str == "C:/dig/html/images/x16/x6801.jpeg":
                    return Image.new("1", (251, 390))
                elif image_path_str == "C:/dig/html/images/x16/x6968.jpeg":
                    return Image.new("1", (390, 347))
            
                raise Exception("didn't find image")

            mock_PIL_Image.side_effect = mock_create_image_with_proper_size

            assert image_page.extract_all_images("C:/", mock_readfile) == {
                slid_azt_extracted["path"]: slid_azt_extracted,
                slid_bdo_extracted["path"]: slid_bdo_extracted,
                slid_bet_extracted["path"]: slid_bet_extracted
            }

def test_generate_metadata_dicts():
    extracted_images = {
        slid_azt_extracted["path"]: slid_azt_extracted,
        slid_bdo_extracted["path"]: slid_bdo_extracted,
        slid_bet_extracted["path"]: slid_bet_extracted
    }
    assert image_page.generate_metadata_dicts(extracted_images) == {
        "imagePathToFigureNum": {
            slid_azt_extracted["path"]: slid_azt_extracted["figureNum"],
            slid_bdo_extracted["path"]: slid_bdo_extracted["figureNum"],
            slid_bet_extracted["path"]: slid_bet_extracted["figureNum"]
        },
        "slidPathToFigureNum": {
            slid_azt_extracted["htmlPagePath"]: slid_azt_extracted["figureNum"],
            slid_bdo_extracted["htmlPagePath"]: slid_bdo_extracted["figureNum"],
            slid_bet_extracted["htmlPagePath"]: slid_bet_extracted["figureNum"]
        },
        "figureNumToImagePath": {
            slid_azt_extracted["figureNum"]: slid_azt_extracted["path"],
            slid_bdo_extracted["figureNum"]: slid_bdo_extracted["path"],
            slid_bet_extracted["figureNum"]: slid_bet_extracted["path"]
        },
        "figureNumToSlidPath": {
            slid_azt_extracted["figureNum"]: slid_azt_extracted["htmlPagePath"],
            slid_bdo_extracted["figureNum"]: slid_bdo_extracted["htmlPagePath"],
            slid_bet_extracted["figureNum"]: slid_bet_extracted["htmlPagePath"]
        }
    }
