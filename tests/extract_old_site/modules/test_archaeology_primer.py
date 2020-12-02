from src.extract_old_site.modules import archaeology_primer as primer
import pytest

# Incomplete sample of the full contents.html file
contents_html_str = """
<html>
<head><title>Excavating Occaneechi Town - [Archaeology Primer]</title></head>
<body bgcolor="#ffffff">

<table width="670" border="0" align="center">
<tr><td>
<b>
<a href="../index.html">Home</a> |
<a href="../copyright.html">Copyright</a>
</b>
</td></tr>
</table>

<center><h1>Archaeology Primer Contents</h1></center>

<table width="670" border="0" align="center">
<tr>
<td> 

<font size="+1">Introduction</font> 
<br>&nbsp;&nbsp;&nbsp;&nbsp;1.  <a href="primer01.html">An Archaeology Primer</a>
<br>&nbsp;&nbsp;&nbsp;&nbsp;2. <a href="primer02.html">Basic Excavation Steps</a>

<br><font size="+1">The Site Grid</font> 
<br>&nbsp;&nbsp;&nbsp;&nbsp;3. <a href="primer03.html">Establishing the Site Grid</a>
<br>&nbsp;&nbsp;&nbsp;&nbsp;4. <a href="primer04.html">The Excavation Grid</a>
<br>&nbsp;&nbsp;&nbsp;&nbsp;5. <a href="primer05.html">Excavation Units</a>

</td>
    
<td valign="top">

<br><font size="+1">Backfilling</font> 
<br>&nbsp;&nbsp;&nbsp;&nbsp;24. <a href="primer24.html">Backfilling the Excavation</a>

<br><font size="+1">Conclusion</font> 
<br>&nbsp;&nbsp;&nbsp;&nbsp;25. <a href="primer25.html">Exploring Archaeology Further</a>

</td>
</tr>
</table>


</body>
</html>
"""

primer01_html_str = """
<html>
<head><title>Excavating Occaneechi Town - [Archaeology Primer]</title></head>
<body bgcolor="#ffffff">

<table width="670" border="0" align="center">
<tr>
<td width="370">
<b>
Previous | 
<a href="primer02.html">Next</a> | 
<a href="contents.html">Contents</a> |
<a href="../index.html">Home</a> |
<a href="../copyright.html">Copyright</a>
</b>
</td>
<td>
<div align="right"><b>Page 1 of 25</b></div>
</td>
</tr>
</table>

<center><h1>An Archaeology Primer</h1></center>

<table width="670" border="0" align="center"><tr><td> 

<table align="right"><tr><td><img src="../images/primer/x6947.gif"></td></tr>
<tr><th><font size=-1>An excavation block at Occaneechi Town with plowed soil
removed.<br>The dark stains are archaeological features.</font></th></tr></table>

<p>This primer will introduce the methods of archaeology, so you can
better understand how Occaneechi Town was excavated and how the
Electronic Dig works.  All the examples and photographs you'll see
come from the actual excavations at Occaneechi Town (also called the
Fredricks site) and nearby sites in Hillsborough, North Carolina.  The
real digging was done by archaeologists and students from the
University of North Carolina at Chapel Hill between 1983 and 1995,
with the active participation of members of the modern Occaneechi Band
of the Saponi Nation.</p>

<p>&nbsp;</p>
<p>&nbsp;</p>

</td></tr></table>
</body>
</html> 
"""

plowzone_html_str = """
<html>
<head>
<title>Video</title>
</head>
<body>

<center>
<embed src="../video/plowzone.mov" width="360" height="256" BGCOLOR="black" SCALE="aspect" autoplay="true" PLUGINSPAGE="http://www.apple.com/quicktime/download/"> </embed>
<p><b>Students digging and screening plowed soil.</b></p>
</center>

</body>
</html>
"""

trowel_html_str = """
<html>
<head>
<title>Video</title>
</head>
<body>

<center>
<embed src="../video/trowel.mov" width="360" height="256" BGCOLOR="black" SCALE="aspect" autoplay="true" PLUGINSPAGE="http://www.apple.com/quicktime/download/"> </embed>
<p><b>Students troweling the subsoil surface.</b></p>
</center>

</body>
</html>
"""

primer01_html_extracted = {
    "image": {
        "path": "/html/images/primer/x6947.gif",
        "caption": ("An excavation block at Occaneechi Town with plowed soil "
                    "removed. The dark stains are archaeological features.")
    },
    "map": None,
    "content": [{
        "type": "paragraph",
        "content": (
            "This primer will introduce the methods of archaeology, so you can "
            "better understand how Occaneechi Town was excavated and how the "
            "Electronic Dig works. All the examples and photographs you'll see "
            "come from the actual excavations at Occaneechi Town (also called the "
            "Fredricks site) and nearby sites in Hillsborough, North Carolina. The "
            "real digging was done by archaeologists and students from the "
            "University of North Carolina at Chapel Hill between 1983 and 1995, "
            "with the active participation of members of the modern Occaneechi Band "
            "of the Saponi Nation.")
    }],
    "title": "An Archaeology Primer",
    "pageNum": "AP1"
}

contents_html_extracted = [{
    "path": "/html/primer/primer01.html",
    "shortTitle": "Introduction",
    "fullTitle": "Introduction",
    "author": None,
    "sections": [{
        "name": "An Archaeology Primer",
        "path": "/html/primer/primer01.html",
        "subsections": [],
        "pageNum": "AP1"
    }, {
        "name": "Basic Excavation Steps",
        "path": "/html/primer/primer02.html",
        "subsections": [],
        "pageNum": "AP2"
    }]
}, {
    "path": "/html/primer/primer03.html",
    "shortTitle": "The Site Grid",
    "fullTitle": "The Site Grid",
    "author": None,
    "sections": [{
        "name": "Establishing the Site Grid",
        "path": "/html/primer/primer03.html",
        "subsections": [],
        "pageNum": "AP3"
    }, {
        "name": "The Excavation Grid",
        "path": "/html/primer/primer04.html",
        "subsections": [],
        "pageNum": "AP4"
    }, {
        "name": "Excavation Units",
        "path": "/html/primer/primer05.html",
        "subsections": [],
        "pageNum": "AP5"
    }]
}, {
    "path": "/html/primer/primer24.html",
    "shortTitle": "Backfilling",
    "fullTitle": "Backfilling",
    "author": None,
    "sections": [{
        "name": "Backfilling the Excavation",
        "path": "/html/primer/primer24.html",
        "subsections": [],
        "pageNum": "AP24"
    }]
}, {
    "path": "/html/primer/primer25.html",
    "shortTitle": "Conclusion",
    "fullTitle": "Conclusion",
    "author": None,
    "sections": [{
        "name": "Exploring Archaeology Further",
        "path": "/html/primer/primer25.html",
        "subsections": [],
        "pageNum": "AP25"
    }]
}]

plowzone_html_extracted = {
    "path": "/html/video/plowzone.mov",
    "caption": "Students digging and screening plowed soil."
}

trowel_html_extracted = {
    "path": "/html/video/trowel.mov",
    "caption": "Students troweling the subsoil surface."
}

@pytest.mark.parametrize("html_string,current_page_name,expected_result", [
    (primer01_html_str, "primer01.html", primer01_html_extracted)
])
def test_extract_primer_page(html_string, current_page_name, expected_result):
    assert primer.extract_primer_page(html_string, "C:/", "primer01.html", None) == expected_result

@pytest.mark.parametrize("html_string,expected_result", [
    (plowzone_html_str, plowzone_html_extracted),
    (trowel_html_str, trowel_html_extracted)
])
def test_extract_video_page(html_string, expected_result):
    assert primer.extract_video_page(html_string) == expected_result

@pytest.mark.parametrize("html_string,expected_result", [
    (contents_html_str, contents_html_extracted)
])
def test_extract_table_of_contents(html_string, expected_result):
    assert primer.extract_table_of_contents(html_string) == expected_result
