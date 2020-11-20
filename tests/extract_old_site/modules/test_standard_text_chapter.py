from src.extract_old_site.modules import standard_text_chapter as text
import pathlib
import pytest
import os
from unittest import mock


# Define example data for tests
# Modules, Sections, and Pages for a single Example Part, sampled from
# /dig/html/part2
#
# Section 0
# /dig/html/split/report33.html (pg. 1)
# /dig/html/split/report34.html (pg. 2)
# /dig/html/split/report35.html (pg. 3)
# /dig/html/split/report36.html (pg. 4)
# /dig/html/split/report37.html (pg. 5)
# /dig/html/split/report38.html (pg. 6)
# Section 1
# /dig/html/split/report39.html (pg. 7)
# /dig/html/split/report40.html (pg. 8)

report33_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report33a.html" marginwidth=1 marginheight=1>
<frame src="report33b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report33c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report34_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report34a.html" marginwidth=1 marginheight=1>
<frame src="report34b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report34c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report35_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report35a.html" marginwidth=1 marginheight=1>
<frame src="report35b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report35c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report36_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report36a.html" marginwidth=1 marginheight=1>
<frame src="report36b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report36c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report37_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report37a.html" marginwidth=1 marginheight=1>
<frame src="report37b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report37c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report38_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report38a.html" marginwidth=1 marginheight=1>
<frame src="report38b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report38c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report39_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report39a.html" marginwidth=1 marginheight=1>
<frame src="report39b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report39c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report40_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report40a.html" marginwidth=1 marginheight=1>
<frame src="report40b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report40c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report41_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report41a.html" marginwidth=1 marginheight=1>
<frame src="report41b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report41c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report42_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report42a.html" marginwidth=1 marginheight=1>
<frame src="report42b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report42c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report43_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report43a.html" marginwidth=1 marginheight=1>
<frame src="report43b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report43c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report44_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report44a.html" marginwidth=1 marginheight=1>
<frame src="report44b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report44c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

report45_html_str = """
<html><frameset rows="28,*,28" border=1>
<frame scrolling="no" src="report45a.html" marginwidth=1 marginheight=1>
<frame src="report45b.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="report45c.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# report**a.html strings
report33a_html_str = """
<html><body><center><i>Historical Background</i>
</center></body></html>
"""

report34a_html_str = """
<html><body><center><i>Siouan Archaeology</i>
</center></body></html>
"""

report35a_html_str = """
<html><body><center><i>Fredricks Site Discovery</i>
</center></body></html>
"""

report36a_html_str = """
<html><body><center><i>Fredricks Site Excavation</i>
</center></body></html>
"""

report37a_html_str = """
<html><body><center><i>List of Figures</i>
</center></body></html>
"""

report38a_html_str = """
<html><body><center><i>Sources</i>
</center></body></html>
"""

report39a_html_str = """
<html><body><center><i>Introduction</i>
</center></body></html>
"""

report40a_html_str = """
<html><body><center><i>The Invisible Invaders</i>
</center></body></html>
"""

# report**b.html strings
report33b_html_str = """
<html><body bgcolor=white>
<p>
 	Bacon then attacked the Occaneechis (<a href="../part6/ref_ac.html" target="_top"><u>Billings
1975</u></a>:267-269).<p>
</body></html>
"""

report34b_html_str = """
<html><body bgcolor=white>
<p>
 	Although the need to approach Siouan archaeology.<p>
</body></html>
"""

report35b_html_str = """
<html><body bgcolor=white>
<p>
<i>A Second Look at the Wall Site</i><p>
<p>
	In the summer of 1983, excavations were resumed at the Wall site.<p>
</body></html>
"""

report36b_html_str = """
    <html><body bgcolor=white>
    <p>
        Because the Fredricks site was discovered late in the 1983 field
    season, investigations that summer were relatively brief.  A limited
    excavation of 800 sq ft revealed a portion of a cemetery lying just outside
    the village (see
    <a href="../excavations/slid_bbd.html" target="body"><u>photo</u></a>) and
    a segment of the village palisade (see
    <a href="../excavations/slid_bba.html" target="body"><u>photo</u></a>).
      Three human burials within the cemetery were excavated.  All three pits
    were rectangular with sharp corners (indicating that they probably were
    excavated with metal tools) and contained numerous artifacts of
    Euroamerican manufacture.  A fourth pit excavated within the cemetery
    contained neither human remains nor grave associations (see photos of
    <a href="../excavations/slid_bbv.html" 
    target="body"><u>sifting plowed soil</u></a>, <a 
    href="../excavations/slid_bbf.html" 
    target="body"><u>burial excavation</u></a>).<p>
    <p>
    <i>Field Methods</i><p>
    <p>
        Following completion of each field season, the excavation was
    immediately backfilled using a front-end loader.<p>
    </body></html>
    """

report37b_html_str = """
<html><body bgcolor=white>
<p>
<i>Figures: General</i><p>
<p>
<a href="../excavations/slid_azn.html" target="body"><u>Figure 1</u></a>.
Distribution of Siouan-speaking peoples in eastern North America (based on
Mooney 1894). <p>
</body></html>
"""

report38b_html_str = """
<html><body bgcolor=white>
<p>
	This article was adapted from the following sources:<p>
</body></html>
"""

report39b_html_str = """
<html><body bgcolor=white>
<p>
	On January 26, 1701.<p>
</body></html>
"""

report40b_html_str = """
<html><body bgcolor=white>
<p>
	By far the most drastic upheavals.<p>
</body></html>
"""

# report**c.html strings
report33c_html_str = """
<html><body><center>Page 1</center></body></html>
"""

report34c_html_str = """
<html><body><center>Page 2</center></body></html>
"""

report35c_html_str = """
<html><body><center>Page 3</center></body></html>
"""

report36c_html_str = """
<html><body><center>Page 4</center></body></html>
"""

report37c_html_str = """
<html><body><center>Page 5</center></body></html>
"""

report38c_html_str = """
<html><body><center>Page 6</center></body></html>
"""

report39c_html_str = """
<html><body><center>Page 7</center></body></html>
"""

report40c_html_str = """
<html><body><center>Page 8</center></body></html>
"""

# index*_*.html pages, i.e. sidebars
index0_1_html_str = """
<html><body><p>
<b>Archaeological Background</b><br><p>
by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.<p>
Historical Background<br>
<a target="main" href="body0_2.html">Siouan Archaeology</a><br>
<a target="main" href="body0_3.html">Fredricks Site Discovery</a><br>
<a target="main" href="body0_4.html">Fredricks Site Excavation</a><br>
<a target="main" href="body0_5.html">List of Figures</a><br>
<a target="main" href="body0_6.html">Sources</a><br>
</body></html>
"""

index0_2_html_str = """
<html><body><p>
<b>Archaeological Background</b><br><p>
by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.<p>
<a target="main" href="body0_1.html">Historical Background</a><br>
Siouan Archaeology<br>
<a target="main" href="body0_3.html">Fredricks Site Discovery</a><br>
<a target="main" href="body0_4.html">Fredricks Site Excavation</a><br>
<a target="main" href="body0_5.html">List of Figures</a><br>
<a target="main" href="body0_6.html">Sources</a><br>
</body></html>
"""

index0_3_html_str = """
<html><body><p>
<b>Archaeological Background</b><br><p>
by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.<p>
<a target="main" href="body0_1.html">Historical Background</a><br>
<a target="main" href="body0_2.html">Siouan Archaeology</a><br>
Fredricks Site Discovery<br>
<a target="main" href="body0_4.html">Fredricks Site Excavation</a><br>
<a target="main" href="body0_5.html">List of Figures</a><br>
<a target="main" href="body0_6.html">Sources</a><br>
</body></html>
"""

index0_4_html_str = """
<html><body><p>
<b>Archaeological Background</b><br><p>
by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.<p>
<a target="main" href="body0_1.html">Historical Background</a><br>
<a target="main" href="body0_2.html">Siouan Archaeology</a><br>
<a target="main" href="body0_3.html">Fredricks Site Discovery</a><br>
Fredricks Site Excavation<br>
<a target="main" href="body0_5.html">List of Figures</a><br>
<a target="main" href="body0_6.html">Sources</a><br>
</body></html>
"""

index0_5_html_str = """
<html><body><p>
<b>Archaeological Background</b><br><p>
by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.<p>
<a target="main" href="body0_1.html">Historical Background</a><br>
<a target="main" href="body0_2.html">Siouan Archaeology</a><br>
<a target="main" href="body0_3.html">Fredricks Site Discovery</a><br>
<a target="main" href="body0_4.html">Fredricks Site Excavation</a><br>
List of Figures<br>
<a target="main" href="body0_6.html">Sources</a><br>
</body></html>
"""

index0_6_html_str = """
<html><body><p>
<b>Archaeological Background</b><br><p>
by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.<p>
<a target="main" href="body0_1.html">Historical Background</a><br>
<a target="main" href="body0_2.html">Siouan Archaeology</a><br>
<a target="main" href="body0_3.html">Fredricks Site Discovery</a><br>
<a target="main" href="body0_4.html">Fredricks Site Excavation</a><br>
<a target="main" href="body0_5.html">List of Figures</a><br>
Sources<br>
</body></html>
"""

index1_1_html_str = """
<html><body><p>
<b>"This Western World": The Evolution of the Piedmont, 1525-1725</b><br>
<p>by James H. Merrell<p>
Introduction<br>
<a target="main" href="body1_2.html">The Invisible Invaders</a><br>
"""

index1_2_html_str = """
<html><body><p>
<b>"This Western World": The Evolution of the Piedmont, 1525-1725</b><br>
<p>by James H. Merrell<p>
<a target="main" href="body1_1.html">Introduction</a><br>
The Invisible Invaders<br>
</body></html>
"""

# tabs*.html pages, i.e. top-level headers
tabs0_html_str = """
<html><body><b>
Archaeology |
<a target="_parent" href="tab1.html">History (1525-1725)</a> |
<a target="_parent" href="../index.html">Home</a> |
<a target="_parent" href="../copyright.html">Copyright</a>
</b></body></html>
"""

tabs1_html_str = """
<html><body><b>
<a target="_parent" href="tab0.html">Archaeology</a> |
History (1525-1725) |
<a target="_parent" href="../index.html">Home</a> |
<a target="_parent" href="../copyright.html">Copyright</a>
</b></body></html>
"""

# body*_*.html pages, i.e. frame containers for the sidebar, title, content, and page number
body0_1_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0_1.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report33.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

body0_2_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0_2.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report34.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

body0_3_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0_3.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report35.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

body0_4_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0_4.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report36.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

body0_5_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0_5.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report37.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

body0_6_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index0_6.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report38.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

body1_1_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index1_1.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report39.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

body1_2_html_str = """
<html><frameset cols="240,*" border=1>
<frame name="choice" src="index1_2.html" marginwidth=1 marginheight=1>
<frame name="body" src="../split/report40.html" marginwidth=1 marginheight=1>
</frameset></html>
"""

# tab*_*.html pages, i.e. highest level frame container for an entire text page
tab0_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_1.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

tab0_2_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_2.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

tab0_3_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_3.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

tab0_4_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_4.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

tab0_5_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_5.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

tab0_6_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
<frame name="main" src="body0_6.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

tab1_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs1.html" marginwidth=1 marginheight=1>
<frame name="main" src="body1_1.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

tab1_2_html_str = """
<html><head><title>Excavating Occaneechi Town - [Background]</title></head>
<frameset rows="28,*">
<frame name="tabs" scrolling="no" src="tabs1.html" marginwidth=1 marginheight=1>
<frame name="main" src="body1_2.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# Define expected data from running functions

# Extracted titles
report33a_extracted = "Historical Background"
report34a_extracted = "Siouan Archaeology"
report35a_extracted = "Fredricks Site Discovery"
report36a_extracted = "Fredricks Site Excavation"
report37a_extracted = "List of Figures"
report38a_extracted = "Sources"
report39a_extracted = "Introduction"
report40a_extracted = "The Invisible Invaders"

# Extracted page content
# Note: all double spaces, '  ', are removed in the extracted data,
# as are all "target" attributes of <a> tags.
report33b_extracted = [{
    "type": "paragraph",
    "content": ('Bacon then attacked the Occaneechis (<a href="/dig/html/part6/ref_ac.html">'
                '<u>Billings 1975</u></a>:267-269).')
}]

report34b_extracted = [{
    "type": "paragraph",
    "content": "Although the need to approach Siouan archaeology."
}]

report35b_extracted = [{
    "type": "italic-title",
    "content": "A Second Look at the Wall Site"
}, {
    "type": "paragraph",
    "content": "In the summer of 1983, excavations were resumed at the Wall site."
}]

report36b_extracted = [{
    "type": "paragraph",
    "content": 'Because the Fredricks site was discovered late in the '
               '1983 field season, investigations that summer were '
               'relatively brief. A limited excavation of 800 sq ft '
               'revealed a portion of a cemetery lying just outside the '
               'village (see '
               '<a href="/dig/html/excavations/slid_bbd.html">'
               '<u>photo</u></a>) and a segment of the '
               'village palisade '
               '(see <a href="/dig/html/excavations/slid_bba.html">'
               '<u>photo</u></a>). Three human burials '
               'within the cemetery were excavated. All three pits were '
               'rectangular with sharp corners (indicating that they '
               'probably were excavated with metal tools) and contained '
               'numerous artifacts of Euroamerican manufacture. A fourth '
               'pit excavated within the cemetery contained neither human '
               'remains nor grave associations (see photos of '
               '<a href="/dig/html/excavations/slid_bbv.html">'
               '<u>sifting plowed soil</u></a>, '
               '<a href="/dig/html/excavations/slid_bbf.html">'
               '<u>burial excavation</u></a>).'
    }, {
        "type": "italic-title",
        "content": "Field Methods"
    }, {
        "type": "paragraph",
        "content": 'Following completion of each field season, the excavation '
                   'was immediately backfilled using a front-end loader.'
}]

report37b_extracted = [{
    "type": "italic-title",
    "content": "Figures: General"
}, {
    "type": "paragraph",
    "content": ('<a href="/dig/html/excavations/slid_azn.html"><u>Figure 1</u></a>. '
                'Distribution of Siouan-speaking peoples in eastern North America (based on Mooney 1894).')
}]

report38b_extracted = [{
    "type": "paragraph",
    "content": "This article was adapted from the following sources:"
}]

report39b_extracted = [{
    "type": "paragraph",
    "content": "On January 26, 1701."
}]

report40b_extracted = [{
    "type": "paragraph",
    "content": "By far the most drastic upheavals."
}]

# Extracted Page Numbers
report33c_extracted = "1"
report34c_extracted = "2"
report35c_extracted = "3"
report36c_extracted = "4"
report37c_extracted = "5"
report38c_extracted = "6"
report39c_extracted = "7"
report40c_extracted = "8"

# Extracted sidebars
index0_extracted = {
    "currentModuleFullName": "Archaeological Background",
    "moduleAuthor": "by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.",
    "sections": [{
        'name': 'Historical Background',
        'path': '/dig/html/part2/body0_1.html',
        'subsections': []
    }, {
        'name': 'Siouan Archaeology',
        'path': '/dig/html/part2/body0_2.html',
        'subsections': []
    }, {
        'name': 'Fredricks Site Discovery',
        'path': '/dig/html/part2/body0_3.html',
        'subsections': []
    }, {
        'name': 'Fredricks Site Excavation',
        'path': '/dig/html/part2/body0_4.html',
        'subsections': []
    }, {
        'name': 'List of Figures',
        'path': '/dig/html/part2/body0_5.html',
        'subsections': []
    }, {
        'name': 'Sources',
        'path': '/dig/html/part2/body0_6.html',
        'subsections': []
    }]
}

index0_extracted_with_page_nums = {
    "currentModuleFullName": "Archaeological Background",
    "moduleAuthor": "by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.",
    "sections": [{
        'name': 'Historical Background',
        'path': '/dig/html/part2/body0_1.html',
        'subsections': [],
        "pageNum": "1"
    }, {
        'name': 'Siouan Archaeology',
        'path': '/dig/html/part2/body0_2.html',
        'subsections': [],
        "pageNum": "2"
    }, {
        'name': 'Fredricks Site Discovery',
        'path': '/dig/html/part2/body0_3.html',
        'subsections': [],
        "pageNum": "3"
    }, {
        'name': 'Fredricks Site Excavation',
        'path': '/dig/html/part2/body0_4.html',
        'subsections': [],
        "pageNum": "4"
    }, {
        'name': 'List of Figures',
        'path': '/dig/html/part2/body0_5.html',
        'subsections': [],
        "pageNum": "5"
    }, {
        'name': 'Sources',
        'path': '/dig/html/part2/body0_6.html',
        'subsections': [],
        "pageNum": "6"
    }]
}

index1_extracted = {
    "currentModuleFullName": '"This Western World": The Evolution of the Piedmont, 1525-1725',
    "moduleAuthor": "by James H. Merrell",
    "sections": [{
        "name": "Introduction",
        "path": "/dig/html/part2/body1_1.html",
        "subsections": []
    }, {
        "name": "The Invisible Invaders",
        "path": "/dig/html/part2/body1_2.html",
        "subsections": []
    }]
}

index1_extracted_with_page_nums = {
    "currentModuleFullName": '"This Western World": The Evolution of the Piedmont, 1525-1725',
    "moduleAuthor": "by James H. Merrell",
    "sections": [{
        "name": "Introduction",
        "path": "/dig/html/part2/body1_1.html",
        "subsections": [],
        "pageNum": "7"
    }, {
        "name": "The Invisible Invaders",
        "path": "/dig/html/part2/body1_2.html",
        "subsections": [],
        "pageNum": "8"
    }]
}

# Extracted topbar
tabs_extracted = {
    "modules": [{
        "moduleShortName": "Archaeology",
        "path": "/dig/html/part2/tab0.html"
    }, {
        "moduleShortName": "History (1525-1725)",
        "path": "/dig/html/part2/tab1.html"
    }]
}

def mock_readfile(orig_filename, parent_dir_path_obj):
    resolved_path = os.path.normpath(parent_dir_path_obj / orig_filename)
    filename = pathlib.Path(resolved_path).name
    resolved_parent_dir_path_obj = pathlib.Path(resolved_path).parent
    if resolved_parent_dir_path_obj.as_posix() == "C:/dig/html/part2":
        if filename == "index0_1.html":
            return index0_1_html_str
        elif filename == "index0_2.html":
            return index0_2_html_str
        elif filename == "index0_3.html":
            return index0_3_html_str
        elif filename == "index0_4.html":
            return index0_4_html_str
        elif filename == "index0_5.html":
            return index0_5_html_str
        elif filename == "index0_6.html":
            return index0_6_html_str
        elif filename == "index1_1.html":
            return index1_1_html_str
        elif filename == "index1_2.html":
            return index1_2_html_str
        elif filename == "body0_1.html":
            return body0_1_html_str
        elif filename == "body0_2.html":
            return body0_2_html_str
        elif filename == "body0_3.html":
            return body0_3_html_str
        elif filename == "body0_4.html":
            return body0_4_html_str
        elif filename == "body0_5.html":
            return body0_5_html_str
        elif filename == "body0_6.html":
            return body0_6_html_str
        elif filename == "body1_1.html":
            return body1_1_html_str
        elif filename == "body1_2.html":
            return body1_2_html_str
        elif filename == "tab0.html":
            return tab0_html_str
        elif filename == "tab0_2.html":
            return tab0_2_html_str
        elif filename == "tab0_3.html":
            return tab0_3_html_str
        elif filename == "tab0_4.html":
            return tab0_4_html_str
        elif filename == "tab0_5.html":
            return tab0_5_html_str
        elif filename == "tab0_6.html":
            return tab0_6_html_str
        elif filename == "tab1.html":
            return tab1_html_str
        elif filename == "tab1_2.html":
            return tab1_2_html_str
        elif filename == "tabs0.html":
            return tabs0_html_str
        elif filename == "tabs1.html":
            return tabs1_html_str
    elif resolved_parent_dir_path_obj.as_posix() == "C:/dig/html/split":
        if filename == "report33.html":
            return report33_html_str
        elif filename == "report34.html":
            return report34_html_str
        elif filename == "report35.html":
            return report35_html_str
        elif filename == "report36.html":
            return report36_html_str
        elif filename == "report37.html":
            return report37_html_str
        elif filename == "report38.html":
            return report38_html_str
        elif filename == "report39.html":
            return report39_html_str
        elif filename == "report40.html":
            return report40_html_str
        elif filename == "report33a.html":
            return report33a_html_str
        elif filename == "report34a.html":
            return report34a_html_str
        elif filename == "report35a.html":
            return report35a_html_str
        elif filename == "report36a.html":
            return report36a_html_str
        elif filename == "report37a.html":
            return report37a_html_str
        elif filename == "report38a.html":
            return report38a_html_str
        elif filename == "report39a.html":
            return report39a_html_str
        elif filename == "report40a.html":
            return report40a_html_str
        elif filename == "report33b.html":
            return report33b_html_str
        elif filename == "report34b.html":
            return report34b_html_str
        elif filename == "report35b.html":
            return report35b_html_str
        elif filename == "report36b.html":
            return report36b_html_str
        elif filename == "report37b.html":
            return report37b_html_str
        elif filename == "report38b.html":
            return report38b_html_str
        elif filename == "report39b.html":
            return report39b_html_str
        elif filename == "report40b.html":
            return report40b_html_str
        elif filename == "report33c.html":
            return report33c_html_str
        elif filename == "report34c.html":
            return report34c_html_str
        elif filename == "report35c.html":
            return report35c_html_str
        elif filename == "report36c.html":
            return report36c_html_str
        elif filename == "report37c.html":
            return report37c_html_str
        elif filename == "report38c.html":
            return report38c_html_str
        elif filename == "report39c.html":
            return report39c_html_str
        elif filename == "report40c.html":
            return report40c_html_str

    raise Exception("did not find file in mock_readfile")


@pytest.mark.parametrize("html_string,folder_path_str,expected_content", [
    (report36b_html_str, "/dig/html/split", report36b_extracted)
])
def test_extract_page_content(html_string, folder_path_str, expected_content):
    extracted_content = text.extract_page_content(html_string, folder_path_str)
    assert extracted_content == expected_content


@pytest.mark.parametrize("html_string,expected_title", [
    ("<html><body><center><i>Historical Background</i></center></body></html>",
     "Historical Background"),
    ("""<html><body><center><i>Fredricks Site Excavation</i>
        </center></body></html>""", "Fredricks Site Excavation")
])
def test_extract_page_title(html_string, expected_title):
    assert text.extract_page_title(html_string) == expected_title


@pytest.mark.parametrize("html_string,expected_page_num", [
    ("<html><body><center>Page i</center></body></html>", "i"),
    ("<html><body><center>Page 51</center></body></html>", "51")
])
def test_extract_page_number(html_string, expected_page_num):
    assert text.extract_page_number(html_string) == expected_page_num


def test_extract_sidebar():
    test_data1 = """
        <html><body><p>
        <b>Archaeological Background</b><br><p>
        by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.<p>
        <a target="main" href="body0_1.html">Historical Background</a><br>
        Siouan Archaeology<br>
        <a target="main" href="body0_3.html">Fredricks Site Discovery</a><br>
        <a target="main" href="body0_4.html">Fredricks Site Excavation</a><br>
        <a target="main" href="body0_5.html">List of Figures</a><br>
        <a target="main" href="body0_6.html">Sources</a><br>
        </body></html>"""
    test1_sections = [{
        'name': 'Historical Background',
        'path': '/dig/html/part2/body0_1.html',
        'subsections': []
    }, {
        'name': 'Siouan Archaeology',
        'path': '/dig/html/part2/body0_2.html',
        'subsections': []
    }, {
        'name': 'Fredricks Site Discovery',
        'path': '/dig/html/part2/body0_3.html',
        'subsections': []
    }, {
        'name': 'Fredricks Site Excavation',
        'path': '/dig/html/part2/body0_4.html',
        'subsections': []
    }, {
        'name': 'List of Figures',
        'path': '/dig/html/part2/body0_5.html',
        'subsections': []
    }, {
        'name': 'Sources',
        'path': '/dig/html/part2/body0_6.html',
        'subsections': []
    }]
    extracted = text.extract_sidebar(test_data1, '/dig/html/part2', 'body0_2.html')
    assert extracted['currentModuleFullName'] == 'Archaeological Background'
    assert extracted['moduleAuthor'] == 'by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.'
    assert extracted['sections'] == test1_sections
    assert extracted['currentSection'] == extracted['sections'][1]

    test_data2 = """
        <html><body><p>
        <b>Animal Remains: 1983-1984 Excavations</b><br><p>
        by Mary Ann Holm<p>
        <a target="main" href="body0_01.html">Research Questions</a><br>
        <a target="main" href="body0_02.html">Ethnohistoric Accounts of Animal Use</a><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="main" href="body0_03.html">Mammals</a><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="main" href="body0_04.html">Birds</a><br>
        &nbsp;&nbsp;&nbsp;&nbsp;Reptiles<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="main" href="body0_06.html">Amphibians</a><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="main" href="body0_07.html">Fish</a><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="main" href="body0_08.html">Summary</a><br>
        <a target="main" href="body0_09.html">Recovery Techniques</a><br>
        <a target="main" href="body0_10.html">Analytical Procedures</a><br>
        <a target="main" href="body0_11.html">Animals from the Wall Site</a><br>
        <a target="main" href="body0_12.html">Animals from the Fredricks Site</a><br>
        <a target="main" href="body0_13.html">Comparison of the Sites</a><br>
        <a target="main" href="body0_14.html">Habitat Preference and Seasonality</a><br>
        <a target="main" href="body0_15.html">Species Diversity</a><br>
        <a target="main" href="body0_16.html">Conclusions</a><br>
        <a target="main" href="body0_17.html">List of Tables and Figures</a><br>
        <a target="main" href="body0_18.html">Source</a><br>
        </body></html>"""
    test2_sections = [{
        'name': 'Research Questions',
        'path': '/dig/html/part4/body0_01.html',
        'subsections': []
    }, {
        'name': 'Ethnohistoric Accounts of Animal Use',
        'path': '/dig/html/part4/body0_02.html',
        'subsections': [{
            'name': 'Mammals',
            'path': '/dig/html/part4/body0_03.html',
            'subsections': []
        }, {
            'name': 'Birds',
            'path': '/dig/html/part4/body0_04.html',
            'subsections': []
        }, {
            'name': 'Reptiles',
            'path': '/dig/html/part4/body0_05.html',
            'subsections': []
        }, {
            'name': 'Amphibians',
            'path': '/dig/html/part4/body0_06.html',
            'subsections': []
        }, {
            'name': 'Fish',
            'path': '/dig/html/part4/body0_07.html',
            'subsections': []
        }, {
            'name': 'Summary',
            'path': '/dig/html/part4/body0_08.html',
            'subsections': []
        }]
    }, {
        'name': 'Recovery Techniques',
        'path': '/dig/html/part4/body0_09.html',
        'subsections': []
    }, {
        'name': 'Analytical Procedures',
        'path': '/dig/html/part4/body0_10.html',
        'subsections': []
    }, {
        'name': 'Animals from the Wall Site',
        'path': '/dig/html/part4/body0_11.html',
        'subsections': []
    }, {
        'name': 'Animals from the Fredricks Site',
        'path': '/dig/html/part4/body0_12.html',
        'subsections': []
    }, {
        'name': 'Comparison of the Sites',
        'path': '/dig/html/part4/body0_13.html',
        'subsections': []
    }, {
        'name': 'Habitat Preference and Seasonality',
        'path': '/dig/html/part4/body0_14.html',
        'subsections': []
    }, {
        'name': 'Species Diversity',
        'path': '/dig/html/part4/body0_15.html',
        'subsections': []
    }, {
        'name': 'Conclusions',
        'path': '/dig/html/part4/body0_16.html',
        'subsections': []
    }, {
        'name': 'List of Tables and Figures',
        'path': '/dig/html/part4/body0_17.html',
        'subsections': []
    }, {
        'name': 'Source',
        'path': '/dig/html/part4/body0_18.html',
        'subsections': []
    }]
    extracted = text.extract_sidebar(test_data2, '/dig/html/part4', 'body0_05.html')
    assert extracted['currentModuleFullName'] == 'Animal Remains: 1983-1984 Excavations'
    assert extracted['moduleAuthor'] == 'by Mary Ann Holm'
    assert extracted['sections'] == test2_sections
    assert extracted['currentSection'] == extracted['sections'][1]['subsections'][2]


def test_extract_topbar():
    test_data = """<html><body><b>
                   Archaeology |
                   <a target="_parent" href="tab1.html">History (1525-1725)</a> |
                   <a target="_parent" href="tab2.html">History (1725-present)</a> |
                   <a target="_parent" href="../index.html">Home</a> |
                   <a target="_parent" href="../copyright.html">Copyright</a>
                   </b></body></html>"""
    results = text.extract_topbar(test_data, '/dig/html/part2', 'tab0.html')
    assert results['modules'] == [{
        "moduleShortName": "Archaeology",
        "path": "/dig/html/part2/tab0.html"
    }, {
        "moduleShortName": "History (1525-1725)",
        "path": "/dig/html/part2/tab1.html"
    }, {
        "moduleShortName": "History (1725-present)",
        "path": "/dig/html/part2/tab2.html"
    }]
    assert results['currentModule'] == results['modules'][0]


def test_extract_frames():
    def readfile(filename, full_current_dir_path):
        if filename == 'report33a.html':
            return "a"
        elif filename == 'report33b.html':
            return "b"
        elif filename == 'report33c.html':
            return "c"
    
    test_data = """ <html><frameset rows="28,*,28" border=1>
                    <frame scrolling="no" src="report33a.html" marginwidth=1 marginheight=1>
                    <frame src="report33b.html" marginwidth=1 marginheight=1>
                    <frame scrolling="no" src="report33c.html" marginwidth=1 marginheight=1>
                    </frameset><noframes>you need frames</noframes></html>"""
    assert text.extract_frames(test_data, 'n/a', readfile) == ["a", "b", "c"]


def test_get_body_page_html_contents():
    test_data = """
        <html><frameset cols="240,*" border=1>
        <frame name="choice" src="index0_6.html" marginwidth=1 marginheight=1>
        <frame name="body" src="../split/report38.html" marginwidth=1 marginheight=1>
        </frameset></html>
        """
    results = text.get_body_page_html_contents(test_data,
                                               '/dig/html/part2',
                                               pathlib.Path('C:/'),
                                               mock_readfile)
    assert results == {
        'sidebar_html': index0_6_html_str,
        'reporta_html': report38a_html_str,
        'reportb_html': report38b_html_str,
        'reportc_html': report38c_html_str
    }

def test_get_tab_page_html_contents():
    test_data = """
    <html><head><title>Excavating Occaneechi Town - [Background]</title></head>
    <frameset rows="28,*">
    <frame name="tabs" scrolling="no" src="tabs0.html" marginwidth=1 marginheight=1>
    <frame name="main" src="body0_6.html" marginwidth=1 marginheight=1>
    </frameset><noframes>you need frames</noframes></html>
    """
    
    results = text.get_tab_page_html_contents(test_data,
                                              '/dig/html/part2',
                                              pathlib.Path('C:/'),
                                              mock_readfile)
    assert results == {
        'topbar_html': tabs0_html_str,
        'sidebar_html': index0_6_html_str,
        'reporta_html': report38a_html_str,
        'reportb_html': report38b_html_str,
        'reportc_html': report38c_html_str,
        'body_page_name': 'body0_6.html'
    }

def test_process_tab_html_contents():
    html_strings = {
        "reporta_html": report36a_html_str,
        "reportb_html": report36b_html_str,
        "reportc_html": report36c_html_str,
        "sidebar_html": index0_4_html_str,
        "topbar_html": tabs0_html_str,
        "body_page_name": "body0_4.html"
    }

    assert text.process_tab_html_contents(
        html_strings, "tab0_4.html", "/dig/html/part2", "C:/", mock_readfile
    ) == {
        "page": {
            "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
            "pageNum": report36c_extracted,
            "pageTitle": report36a_extracted,
            "content": report36b_extracted
        },
        "module": {
            "path": tabs_extracted["modules"][0]['path'],
            "shortTitle": tabs_extracted["modules"][0]['moduleShortName'],
            "fullTitle": index0_extracted['currentModuleFullName'],
            "author": index0_extracted['moduleAuthor'],
            "sections": index0_extracted["sections"]
        },
        "additionalSectionInfo": {
            "currentSection": index0_extracted["sections"][3],
            "pageNum": report36c_extracted
        }
    }

# TODO
# def test_validate_tab_html_extraction_results():
#     pass

def test_extract_full_module():
    # Try extracting module 1
    module_file_names = ["tab0.html", "tab0_2.html", "tab0_3.html",
                         "tab0_4.html", "tab0_5.html", "tab0_6.html"]
    assert text.extract_full_module(module_file_names, "/dig/html/part2", pathlib.Path("C:/"), mock_readfile) == {
        "module": {
            "path": tabs_extracted["modules"][0]['path'],
            "shortTitle": tabs_extracted["modules"][0]['moduleShortName'],
            "fullTitle": index0_extracted['currentModuleFullName'],
            "author": index0_extracted['moduleAuthor'],
            "sections": index0_extracted_with_page_nums["sections"]
        },
        "pages": {
            "1": {
                "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                "pageTitle": report33a_extracted,
                "content": report33b_extracted
            },
            "2": {
                "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                "pageTitle": report34a_extracted,
                "content": report34b_extracted
            },
            "3": {
                "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                "pageTitle": report35a_extracted,
                "content": report35b_extracted
            },
            "4": {
                "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                "pageTitle": report36a_extracted,
                "content": report36b_extracted
            },
            "5": {
                "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                "pageTitle": report37a_extracted,
                "content": report37b_extracted
            },
            "6": {
                "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                "pageTitle": report38a_extracted,
                "content": report38b_extracted
            }
        }
    }

def test_extract_full_chapter():
    pass

def test_extract_standard_part():
    with mock.patch.object(pathlib.Path, "iterdir") as mock_iterdir:
        iterdir_filename_paths = [
            "tab0.html", "tab0_2.html", "tab0_3.html",
            "tab0_4.html", "tab0_5.html", "tab0_6.html",
            "tab1.html", "tab1_2.html",
            "body0_1.html", "body0_2.html", "body0_3.html",
            "body0_4.html", "body0_5.html", "body0_6.html",
            "body1_1.html", "body1_2.html",
            "index0_1.html", "index0_2.html", "index0_3.html",
            "index0_4.html", "index0_5.html", "index0_6.html",
            "index1_1.html", "index1_2.html",
            "tabs0.html", "tabs1.html"
        ]
        iterdir_filename_paths = [pathlib.Path(filename) for filename in iterdir_filename_paths]
        mock_iterdir.return_value = iterdir_filename_paths
        assert text.extract_standard_part("part2", "C:/", mock_readfile) == {
            "path": "/dig/html/part2",
            "modules": [{
                "module": {
                    "path": tabs_extracted["modules"][0]['path'],
                    "shortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                    "fullTitle": index0_extracted['currentModuleFullName'],
                    "author": index0_extracted['moduleAuthor'],
                    "sections": index0_extracted_with_page_nums["sections"]
                }
            }, {
                "module": {
                    "path": tabs_extracted["modules"][1]['path'],
                    "shortTitle": tabs_extracted["modules"][1]['moduleShortName'],
                    "fullTitle": index1_extracted['currentModuleFullName'],
                    "author": index1_extracted['moduleAuthor'],
                    "sections": index1_extracted_with_page_nums["sections"]
                }
            }],
            "pages": {
                "1": {
                    "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                    "pageTitle": report33a_extracted,
                    "content": report33b_extracted
                },
                "2": {
                    "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                    "pageTitle": report34a_extracted,
                    "content": report34b_extracted
                },
                "3": {
                    "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                    "pageTitle": report35a_extracted,
                    "content": report35b_extracted
                },
                "4": {
                    "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                    "pageTitle": report36a_extracted,
                    "content": report36b_extracted
                },
                "5": {
                    "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                    "pageTitle": report37a_extracted,
                    "content": report37b_extracted
                },
                "6": {
                    "parentModuleShortTitle": tabs_extracted["modules"][0]['moduleShortName'],
                    "pageTitle": report38a_extracted,
                    "content": report38b_extracted
                },
                "7": {
                    "parentModuleShortTitle": tabs_extracted["modules"][1]['moduleShortName'],
                    "pageTitle": report39a_extracted,
                    "content": report39b_extracted
                },
                "8": {
                    "parentModuleShortTitle": tabs_extracted["modules"][1]['moduleShortName'],
                    "pageTitle": report40a_extracted,
                    "content": report40b_extracted
                }
            }
        }
