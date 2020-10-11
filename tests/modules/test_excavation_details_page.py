from src.extract_old_site.modules import excavation_details_page as exc_det

def test_extract_zoom_to():
    test_data = """
    <html><body><big>Zoom To:</big><p>
    <a href="exc_gw.html" target="_top">Sq. 270R90</a><br>
    <a href="exc_gn.html" target="_top">Sq. 270R100</a><br>
    </body></html>
    """
    assert exc_det.extract_zoom_to(test_data) == [{
        "name": "Sq. 270R90",
        "path": "/dig/html/excavations/exc_gw.html"
    }, {
        "name": "Sq. 270R100",
        "path": "/dig/html/excavations/exc_gn.html"
    }]
