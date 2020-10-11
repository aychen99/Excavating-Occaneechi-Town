from src.extract_old_site.modules import image_page
from unittest import mock
import pytest

@pytest.mark.parametrize(
    "html_string,img_page_parent_dir,expected", 
    [("""<html><body><map name="hotlinks">
        <area coords="43,102,193,152" target="_top" href="exc_is.html">
        <area coords="22,151,113,219" target="_top" href="exc_is.html">
        <area coords="194,118,243,220" target="_top" href="exc_is.html">
        <area coords="16,220,237,298" target="_top" href="exc_is.html">
        <area coords="114,152,196,223" target="_top" href="exc_cl.html">
        </map><center>
        <img src="../images/x16/x6801.jpeg" usemap="#hotlinks" border=0>
        <p>Figure 1038. Structure 1 at top of subsoil (view to southwest).</center>
        </body></html>
    """, 
    "/dig/html/excavations",
    {
        "path": "/dig/html/images/x16/x6801.jpeg",
        "caption": "Figure 1038. Structure 1 at top of subsoil (view to southwest).",
        "clickableAreas": [
            {"x1": 43, "y1": 102, "x2": 193, "y2": 152},
            {"x1": 22, "y1": 151, "x2": 113, "y2": 219},
            {"x1": 194, "y1": 118, "x2": 243, "y2": 220},
            {"x1": 16, "y1": 220, "x2": 237, "y2": 298},
            {"x1": 114, "y1": 152, "x2": 196, "y2": 223}
        ],
        "originalDimensions": {
            "width": 251,
            "height": 390
        }
    })])
def test_extract_image_page(html_string, img_page_parent_dir, expected):
    def mock_get_img_dims(img_path):
        print(img_path)
        if img_path == "/content/dig/html/images/x16/x6801.jpeg":
            return {"width": 251, "height": 390}
        else:
            return None

    with mock.patch("src.extract_old_site.modules.image_page.get_image_dimensions", mock_get_img_dims):
        assert image_page.extract_image_page(html_string, img_page_parent_dir, "/content") == expected
