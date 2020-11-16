from src.extract_old_site.modules import artifacts
import pathlib
import os
import pytest
from unittest import mock

# Extract zones of artifacts
# Extract artifacts in a zone
# Extract page number of appendix A

# Extract appendix B frame
# Extract entire appendix B page from multiple files
# Extract multiple appendix B pages

# Test data from Sq. 240R60 (/dig/html/artifacts/art_fg0.html)
# Parent page for component frames
art_fg0_html_str = """
<html><head><title>Excavating Occaneechi Town - [Artifacts]</title></head>
<frameset rows="50%,50%" border=1>
<frame name="ctrl" src="ctrl_fg.html" marginwidth=1 marginheight=1>
<frame name="info" src="info_fg0.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# List of zones
ctrl_fg_html_str = """
<html><body><center><big><b>Sq. 240R60</b></big><br>Artifact Inventory, Appendix A, Page 135<br></center>
<table align="right" border=2>
<tr><td align="center"><a href="../excavations/exc_fg.html" target="_top">Master</a></td></tr>
<tr><td align="center">Description</td></tr>
<tr><td align="center"><a href="../maps/exc0.html" target="_top">Map</a></td></tr>
<tr><td align="center"><a href="../index.html" target="_top">Home</a></td></tr>
</table>
<a href="info_fg0.html" target="info">Plow Zone</a><br>
<a href="info_fg1.html" target="info">Plow Zone, 20-liter Waterscreen Sample</a><br>
<a href="info_fg2.html" target="info">Flatshoveling Top of Subsoil</a><br>
<a href="info_fg3.html" target="info">Troweling Top of Subsoil</a><br>
</body></html>
"""

# Artifacts per zone
info_fg0_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Animal Bone</td><td>1/2"</td><td>1</td><td>2351b656</td><td>&nbsp;</td><td>&nbsp;</td></tr>
<tr><td>Baked Clay</td><td>1/2"</td><td>1</td><td>2351m3399</td><td>&nbsp;</td><td>&nbsp;</td></tr>
<tr><td>Biface</td><td>1/2"</td><td>1</td><td>2351a3397</td><td>&nbsp;</td><td><a href="../dbs/page5.html" target="_top">yes</a></td></tr>
<tr><td>Bifaces</td><td>1/2"</td><td>2</td><td>2351a646</td><td>&nbsp;</td><td><a href="../dbs/page5.html" target="_top">yes</a></td></tr>
</table></body></html>
"""

info_fg1_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Animal Bone</td><td>1/4"</td><td>2</td><td>2351b668</td><td>&nbsp;</td><td>&nbsp;</td></tr>
<tr><td>Bottle Glass (Lip)</td><td>1/4"</td><td>1</td><td>2351a666</td><td>&nbsp;</td><td><a href="../dbs/page3.html" target="_top">yes</a></td></tr>
<tr><td>Daub</td><td>1/2"</td><td>3</td><td>2351m664</td><td>&nbsp;</td><td>&nbsp;</td></tr>
</table></body></html>
"""

info_fg2_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Brick Fragments</td><td>1/2"</td><td>3</td><td>2351m679</td><td>&nbsp;</td><td><a href="../dbs/page3.html" target="_top">yes</a></td></tr>
</table></body></html>
"""

info_fg3_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Potsherd</td><td>1/2"</td><td>1</td><td>2351p682</td><td>&nbsp;</td><td><a href="../dbs/page1.html" target="_top">yes</a></td></tr>
</table></body></html>
"""


# Test data from Feature 15 (/dig/html/artifacts/art_aj0.html)
# Parent page(s) for component frames
art_aj0_html_str = """
<html><head><title>Excavating Occaneechi Town - [Artifacts]</title></head>
<frameset rows="50%,50%" border=1>
<frame name="ctrl" src="ctrl_aj.html" marginwidth=1 marginheight=1>
<frame name="info" src="info_aj0.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

art_aj2_html_str = """
<html><head><title>Excavating Occaneechi Town - [Artifacts]</title></head>
<frameset rows="50%,50%" border=1>
<frame name="ctrl" src="ctrl_aj.html" marginwidth=1 marginheight=1>
<frame name="info" src="info_aj2.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# List of zones
ctrl_aj_html_str = """
<html><body><center><big><b>Feature 15</b></big><br>Artifact Inventory, Appendix A, Page 10<br></center>
<table align="right" border=2>
<tr><td align="center"><a href="../excavations/exc_aj.html" target="_top">Master</a></td></tr>
<tr><td align="center"><a href="../descriptions/tab0_18.html" target="_top">Description</a></td></tr>
<tr><td align="center"><a href="../maps/exc0.html" target="_top">Map</a></td></tr>
<tr><td align="center"><a href="../index.html" target="_top">Home</a></td></tr>
</table>
<a href="info_aj0.html" target="info">Troweling Top of Pit</a><br>
<a href="info_aj1.html" target="info">Posthole #2</a><br>
<a href="info_aj2.html" target="info">Zone 1</a><br>
<a href="info_aj3.html" target="info">Zone 1, 10-liter Flotation Sample</a><br>
<a href="info_aj4.html" target="info">Zone 2</a><br>
</body></html>
"""

# Artifacts per zone
info_aj0_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Flake</td><td></td><td>1</td><td>2351m6164</td><td>&nbsp;</td><td><a href="../dbs/page5.html" target="_top">yes</a></td></tr>
</table></body></html>
"""

info_aj1_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Potsherd</td><td></td><td>1</td><td>2351p6181</td><td>&nbsp;</td><td><a href="../dbs/page1.html" target="_top">yes</a></td></tr>
</table></body></html>
"""

info_aj2_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Charcoal</td><td>1/4"</td><td>4</td><td>2351eb6169</td><td>&nbsp;</td><td>&nbsp;</td></tr>
<tr><td>Chipped Stone Projectile Point</td><td>1/2"</td><td>1</td><td>2351a6165</td><td><a href="img_aj0.html" target="_top">photo</a></td><td><a href="../dbs/page5.html" target="_top">yes</a></td></tr>
<tr><td>Daub</td><td>1/4"</td><td>2</td><td>2351m6171</td><td>&nbsp;</td><td>&nbsp;</td></tr>
</table></body></html>
"""

info_aj3_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Heavy Fraction</td><td></td><td>1</td><td>2351w6175/1</td><td>&nbsp;</td><td>&nbsp;</td></tr>
</table></body></html>
"""

info_aj4_html_str = """
<html><body><table width="100%" border=0>
<tr><th align="left">Artifacts</th><th align="left">Size</th><th align="left">Count</th><th align="left">Cat. No.</th><th align="left">Photo</th><th align="left">More</th></tr>
<tr><td>Washings</td><td>1/16"</td><td>1</td><td>2351w6180</td><td>&nbsp;</td><td>&nbsp;</td></tr>
</table></body></html>
"""

# Related image
img_aj0_html_str = """
<html><head><title>Excavating Occaneechi Town - [Artifacts]</title></head>
<body><center><img src="../images/d16/d_3351.jpeg"><p>Figure 245. Chipped-stone projectile point from Feature 15 (RLA catalog no. 2351a6165).<p><hr><a href="art_aj2.html">Back</a></center></body></html>
"""

# Extra image for testing extract_all_artifacts_images
img_aa0_html_str = """
<html><head><title>Excavating Occaneechi Town - [Artifacts]</title></head>
<body><center><img src="../images/d16/d_3535.jpeg"><p>Figure 183. Plain and check-stamped potsherds from Burial 1 (RLA catalog no. 2351p255).<p><hr><a href="art_aa1.html">Back</a></center></body></html>
"""


# Appendix B samples
# Page 1, Beads
# Frame container
page0_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<frameset rows="28,*,28" border=1>
<frame scrolling="no" src="head0.html" marginwidth=1 marginheight=1>
<frame src="db0_0.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="foot0.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# Title
head0_html_str = "<html><body><center><i>Beads</i></center></body></html>"

# Footer/page number
foot0_html_str = "<html><body><center>Appendix B, Page 1</center></body></html>"

# Actual list of artifacts
db0_0_html_str = """
<html><body><table>
<tr><th nowrap align="left">Catalog No.</th><th nowrap align="left">Context</th></tr>
<tr><td nowrap>2351a1038/a</td><td nowrap>Sq. 260R80</td></tr>
<tr><td nowrap>2351a1076</td><td nowrap>Sq. 260R90</td></tr>
<tr><td nowrap>2351a1110</td><td nowrap>Sq. 270R60</td></tr>
<tr><td nowrap>2351a1110</td><td nowrap>Sq. 270R60</td></tr>
<tr><td nowrap>2351a425</td><td nowrap>Burial 2</td></tr>
<tr><td nowrap>2351a425</td><td nowrap>Burial 2</td></tr>
<tr><td nowrap>2351a425</td><td nowrap>Burial 2</td></tr>
<tr><td nowrap>2351a425</td><td nowrap>Burial 2</td></tr>
<tr><td nowrap>2351a425</td><td nowrap>Burial 2</td></tr>
</table></body><p><center><hr>Prev | <a href="db0_1.html">Next</a></center></body></html>
"""

db0_1_html_str = """
<html><body><table>
<tr><th nowrap align="left">Catalog No.</th><th nowrap align="left">Context</th></tr>
<tr><td nowrap>2351a425</td><td nowrap>Burial 2</td></tr>
<tr><td nowrap>2351a4282          Type IIa</td><td nowrap>Sq. 250R50</td></tr>
<tr><td nowrap>2351a4282          Type IVa</td><td nowrap>Sq. 250R50</td></tr>
<tr><td nowrap>2351a6824/1        Type IIa</td><td nowrap>Feature 28</td></tr>
<tr><td nowrap>2351a6824/1        Type IIa</td><td nowrap>Feature 28</td></tr>
</table></body><p><center><hr><a href="db0_0.html">Prev</a> | <a href="db0_2.html">Next</a></center></body></html>
"""

db0_2_html_str = """
<html><body><table>
<tr><th nowrap align="left">Catalog No.</th><th nowrap align="left">Context</th></tr>
<tr><td nowrap>2351a6824/1        Type IIa</td><td nowrap>Feature 28</td></tr>
<tr><td nowrap>2351a6824/1        Type IIa</td><td nowrap>Feature 28</td></tr>
<tr><td nowrap>2351a6824/1        Type IVa</td><td nowrap>Feature 28</td></tr>
</table></body><p><center><hr><a href="db0_1.html">Prev</a> | <a href="db0_3.html">Next</a></center></body></html>
"""

db0_3_html_str = """
<html><body><table>
<tr><th nowrap align="left">Catalog No.</th><th nowrap align="left">Context</th></tr>
<tr><td nowrap>2378w96            Type IIa</td><td nowrap>Feature 42</td></tr>
</table></body><p><center><hr><a href="db0_2.html">Prev</a> | Next</center></body></html>
"""

# Page 7, Pipes
# Frame container
page6_html_str = """
<html><head><title>Excavating Occaneechi Town - [Excavations]</title></head>
<frameset rows="28,*,28" border=1>
<frame scrolling="no" src="head6.html" marginwidth=1 marginheight=1>
<frame src="db6_0.html" marginwidth=1 marginheight=1>
<frame scrolling="no" src="foot6.html" marginwidth=1 marginheight=1>
</frameset><noframes>you need frames</noframes></html>
"""

# Title
head6_html_str = "<html><body><center><i>Pipes</i></center></body></html>"

# Footer/page number
foot6_html_str = "<html><body><center>Appendix B, Page 7</center></body></html>"

# Actual list of artifacts
db6_0_html_str = """
<html><body><table>
<tr><th nowrap align="left">Catalog No.</th><th nowrap align="left">Raw Material</th><th nowrap align="left">Morphology</th><th nowrap align="left">Portion</th><th nowrap align="left">Bowl Form</th><th nowrap align="left">Decoration</th><th nowrap align="left">Count</th><th nowrap align="left">Comment</th><th nowrap align="left">Context</th></tr>
<tr><td nowrap>2351a1008</td><td nowrap>Kaolin</td><td nowrap>European (Kaolin Form)</td><td nowrap>Bowl Frag.</td><td nowrap>N/A</td><td nowrap>&nbsp;</td><td nowrap>1</td><td nowrap>&nbsp;</td><td nowrap>S260R70</td></tr>
</table></body><p><center><hr>Prev | <a href="db6_1.html">Next</a></center></body></html>
"""

db6_1_html_str = """
<html><body><table>
<tr><th nowrap align="left">Catalog No.</th><th nowrap align="left">Raw Material</th><th nowrap align="left">Morphology</th><th nowrap align="left">Portion</th><th nowrap align="left">Bowl Form</th><th nowrap align="left">Decoration</th><th nowrap align="left">Count</th><th nowrap align="left">Comment</th><th nowrap align="left">Context</th></tr>
<tr><td nowrap>2378a1203</td><td nowrap>Kaolin</td><td nowrap>European (Kaolin Form)</td><td nowrap>Bowl Frag.</td><td nowrap>Indeterminate</td><td nowrap>&nbsp;</td><td nowrap>1</td><td nowrap>&nbsp;</td><td nowrap>S190R20</td></tr>
</table></body><p><center><hr><a href="db6_0.html">Prev</a> | Next</center></body></html>
"""


# Expected results of extraction
img_aa0_extracted = {
    "path": "/dig/html/images/d16/d_3535.jpeg",
    "figureNum": "183",
    "caption": "Plain and check-stamped potsherds from Burial 1 (RLA catalog no. 2351p255)."
}

img_aj0_extracted = {
    "path": "/dig/html/images/d16/d_3351.jpeg",
    "figureNum": "245",
    "caption": "Chipped-stone projectile point from Feature 15 (RLA catalog no. 2351a6165)."
}

ctrl_aj_extracted = {
    "excavationElement": "Feature 15",
    "parentExcPage": "/dig/html/excavations/exc_aj.html",
    "zones": [{
        "name": "Troweling Top of Pit",
        "pageName": "info_aj0.html"
    }, {
        "name": "Posthole #2",
        "pageName": "info_aj1.html"
    }, {
        "name": "Zone 1",
        "pageName": "info_aj2.html"
    }, {
        "name": "Zone 1, 10-liter Flotation Sample",
        "pageName": "info_aj3.html"
    }, {
        "name": "Zone 2",
        "pageName": "info_aj4.html"
    }]
}

ctrl_fg_extracted = {
    "excavationElement": "Sq. 240R60",
    "parentExcPage": "/dig/html/excavations/exc_fg.html",
    "zones": [{
        "name": "Plow Zone",
        "pageName": "info_fg0.html"
    }, {
        "name": "Plow Zone, 20-liter Waterscreen Sample",
        "pageName": "info_fg1.html"
    }, {
        "name": "Flatshoveling Top of Subsoil",
        "pageName": "info_fg2.html"
    }, {
        "name": "Troweling Top of Subsoil",
        "pageName": "info_fg3.html"
    }]
}

info_fg0_extracted = [{
    "Artifacts": "Animal Bone",
    "Size": '1/2"',
    "Count": "1",
    "Cat. No.": "2351b656",
    "Photo": None,
    "More": None
}, {
    "Artifacts": "Baked Clay",
    "Size": '1/2"',
    "Count": "1",
    "Cat. No.": "2351m3399",
    "Photo": None,
    "More": None
}, {
    "Artifacts": "Biface",
    "Size": '1/2"',
    "Count": "1",
    "Cat. No.": "2351a3397",
    "Photo": None,
    "More": "/dig/html/dbs/page5.html"
}, {
    "Artifacts": "Bifaces",
    "Size": '1/2"',
    "Count": "2",
    "Cat. No.": "2351a646",
    "Photo": None,
    "More": "/dig/html/dbs/page5.html"
}]

info_fg1_extracted = [{
    "Artifacts": "Animal Bone",
    "Size": '1/4"',
    "Count": "2",
    "Cat. No.": "2351b668",
    "Photo": None,
    "More": None
}, {
    "Artifacts": "Bottle Glass (Lip)",
    "Size": '1/4"',
    "Count": "1",
    "Cat. No.": "2351a666",
    "Photo": None,
    "More": "/dig/html/dbs/page3.html"
}, {
    "Artifacts": "Daub",
    "Size": '1/2"',
    "Count": "3",
    "Cat. No.": "2351m664",
    "Photo": None,
    "More": None
}]

info_fg2_extracted = [{
    "Artifacts": "Brick Fragments",
    "Size": '1/2"',
    "Count": "3",
    "Cat. No.": "2351m679",
    "Photo": None,
    "More": "/dig/html/dbs/page3.html"
}]

info_fg3_extracted = [{
    "Artifacts": "Potsherd",
    "Size": '1/2"',
    "Count": "1",
    "Cat. No.": "2351p682",
    "Photo": None,
    "More": "/dig/html/dbs/page1.html"
}]

info_aj0_extracted = [{
    "Artifacts": "Flake",
    "Size": None,
    "Count": "1",
    "Cat. No.": "2351m6164",
    "Photo": None,
    "More": "/dig/html/dbs/page5.html"
}]

info_aj1_extracted = [{
    "Artifacts": "Potsherd",
    "Size": None,
    "Count": "1",
    "Cat. No.": "2351p6181",
    "Photo": None,
    "More": "/dig/html/dbs/page1.html"
}]

info_aj2_extracted = [{
    "Artifacts": "Charcoal",
    "Size": '1/4"',
    "Count": "4",
    "Cat. No.": "2351eb6169",
    "Photo": None,
    "More": None
}, {
    "Artifacts": "Chipped Stone Projectile Point",
    "Size": '1/2"',
    "Count": "1",
    "Cat. No.": "2351a6165",
    "Photo": "/dig/html/artifacts/img_aj0.html",
    "More": "/dig/html/dbs/page5.html"
}, {
    "Artifacts": "Daub",
    "Size": '1/4"',
    "Count": "2",
    "Cat. No.": "2351m6171",
    "Photo": None,
    "More": None
}]

info_aj3_extracted = [{
    "Artifacts": "Heavy Fraction",
    "Size": None,
    "Count": "1",
    "Cat. No.": "2351w6175/1",
    "Photo": None,
    "More": None
}]

info_aj4_extracted = [{
    "Artifacts": "Washings",
    "Size": '1/16"',
    "Count": "1",
    "Cat. No.": "2351w6180",
    "Photo": None,
    "More": None
}]

art_aj0_or_feature_15_fully_extracted = {
    "excavationElement": "Feature 15",
    "parentExcPage": "/dig/html/excavations/exc_aj.html",
    "zones": [{
        "name": "Troweling Top of Pit",
        "pageName": "info_aj0.html",
        "artifacts": info_aj0_extracted
    }, {
        "name": "Posthole #2",
        "pageName": "info_aj1.html",
        "artifacts": info_aj1_extracted
    }, {
        "name": "Zone 1",
        "pageName": "info_aj2.html",
        "artifacts": info_aj2_extracted
    }, {
        "name": "Zone 1, 10-liter Flotation Sample",
        "pageName": "info_aj3.html",
        "artifacts": info_aj3_extracted
    }, {
        "name": "Zone 2",
        "pageName": "info_aj4.html",
        "artifacts": info_aj4_extracted
    }]
}

art_fg0_or_sq240r60_fully_extracted = {
    "excavationElement": "Sq. 240R60",
    "parentExcPage": "/dig/html/excavations/exc_fg.html",
    "zones": [{
        "name": "Plow Zone",
        "pageName": "info_fg0.html",
        "artifacts": info_fg0_extracted
    }, {
        "name": "Plow Zone, 20-liter Waterscreen Sample",
        "pageName": "info_fg1.html",
        "artifacts": info_fg1_extracted
    }, {
        "name": "Flatshoveling Top of Subsoil",
        "pageName": "info_fg2.html",
        "artifacts": info_fg2_extracted
    }, {
        "name": "Troweling Top of Subsoil",
        "pageName": "info_fg3.html",
        "artifacts": info_fg3_extracted
    }]
}

head0_extracted = "Beads"
head6_extracted = "Pipes"

db0_0_extracted = [{
    "Catalog No.": "2351a1038/a",
    "Context": "Sq. 260R80"
}, {
    "Catalog No.": "2351a1076",
    "Context": "Sq. 260R90"
}, {
    "Catalog No.": "2351a1110",
    "Context": "Sq. 270R60"
}, {
    "Catalog No.": "2351a1110",
    "Context": "Sq. 270R60"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}]

db0_1_extracted = [{
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a4282          Type IIa",
    "Context": "Sq. 250R50"
}, {
    "Catalog No.": "2351a4282          Type IVa",
    "Context": "Sq. 250R50"
}, {
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}]

db0_2_extracted = [{
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2351a6824/1        Type IVa",
    "Context": "Feature 28"
}]

db0_3_extracted = [{
    "Catalog No.": "2378w96            Type IIa",
    "Context": "Feature 42"
}]

db0_all_artifacts = [{
    "Catalog No.": "2351a1038/a",
    "Context": "Sq. 260R80"
}, {
    "Catalog No.": "2351a1076",
    "Context": "Sq. 260R90"
}, {
    "Catalog No.": "2351a1110",
    "Context": "Sq. 270R60"
}, {
    "Catalog No.": "2351a1110",
    "Context": "Sq. 270R60"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a425",
    "Context": "Burial 2"
}, {
    "Catalog No.": "2351a4282          Type IIa",
    "Context": "Sq. 250R50"
}, {
    "Catalog No.": "2351a4282          Type IVa",
    "Context": "Sq. 250R50"
}, {
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2351a6824/1        Type IIa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2351a6824/1        Type IVa",
    "Context": "Feature 28"
}, {
    "Catalog No.": "2378w96            Type IIa",
    "Context": "Feature 42"
}]

db6_0_extracted = [{
    "Catalog No.": "2351a1008",
    "Raw Material": "Kaolin",
    "Morphology": "European (Kaolin Form)",
    "Portion": "Bowl Frag.",
    "Bowl Form": "N/A",
    "Decoration": None,
    "Count": "1",
    "Comment": None,
    "Context": "S260R70"
}]

db6_1_extracted = [{
    "Catalog No.": "2378a1203",
    "Raw Material": "Kaolin",
    "Morphology": "European (Kaolin Form)",
    "Portion": "Bowl Frag.",
    "Bowl Form": "Indeterminate",
    "Decoration": None,
    "Count": "1",
    "Comment": None,
    "Context": "S190R20"
}]

db6_all_artifacts = [{
    "Catalog No.": "2351a1008",
    "Raw Material": "Kaolin",
    "Morphology": "European (Kaolin Form)",
    "Portion": "Bowl Frag.",
    "Bowl Form": "N/A",
    "Decoration": None,
    "Count": "1",
    "Comment": None,
    "Context": "S260R70"
}, {
    "Catalog No.": "2378a1203",
    "Raw Material": "Kaolin",
    "Morphology": "European (Kaolin Form)",
    "Portion": "Bowl Frag.",
    "Bowl Form": "Indeterminate",
    "Decoration": None,
    "Count": "1",
    "Comment": None,
    "Context": "S190R20"
}]


def mock_readfile(filename, parent_dir_path_obj):
    resolved_path_obj = pathlib.Path(os.path.normpath(parent_dir_path_obj / filename))
    filename = resolved_path_obj.name
    parent_dir_str = resolved_path_obj.parent.as_posix()
    if parent_dir_str == "C:/dig/html/artifacts":
        # Feature 15
        if filename == "ctrl_aj.html":
            return ctrl_aj_html_str
        elif filename == "art_aj0.html":
            return art_aj0_html_str
        elif filename == "art_aj2.html":
            return art_aj2_html_str
        elif filename == "info_aj0.html":
            return info_aj0_html_str
        elif filename == "info_aj1.html":
            return info_aj1_html_str
        elif filename == "info_aj2.html":
            return info_aj2_html_str
        elif filename == "info_aj3.html":
            return info_aj3_html_str
        elif filename == "info_aj4.html":
            return info_aj4_html_str
        elif filename == "img_aj0.html":
            return img_aj0_html_str
        # Sq. 240R60
        elif filename == "art_fg0.html":
            return art_fg0_html_str
        elif filename == "ctrl_fg.html":
            return ctrl_fg_html_str
        elif filename == "info_fg0.html":
            return info_fg0_html_str
        elif filename == "info_fg1.html":
            return info_fg1_html_str
        elif filename == "info_fg2.html":
            return info_fg2_html_str
        elif filename == "info_fg3.html":
            return info_fg3_html_str
        # Extra image
        elif filename == "img_aa0.html":
            return img_aa0_html_str
    elif parent_dir_str == "C:/dig/html/dbs":
        # Page 1, Beads
        if filename == "page0.html":
            return page0_html_str
        elif filename == "head0.html":
            return head0_html_str
        elif filename == "foot0.html":
            return foot0_html_str
        elif filename == "db0_0.html":
            return db0_0_html_str
        elif filename == "db0_1.html":
            return db0_1_html_str
        elif filename == "db0_2.html":
            return db0_2_html_str
        elif filename == "db0_3.html":
            return db0_3_html_str
        # Page 7, Pipes
        elif filename == "page6.html":
            return page6_html_str
        elif filename == "head6.html":
            return head6_html_str
        elif filename == "foot6.html":
            return foot6_html_str
        elif filename == "db6_0.html":
            return db6_0_html_str
        elif filename == "db6_1.html":
            return db6_1_html_str

    raise Exception("did not find file in mock_readfile")

@pytest.mark.parametrize("image_page_html_str,expected_result", [
    (img_aa0_html_str, img_aa0_extracted),
    (img_aj0_html_str, img_aj0_extracted)
])
def test_extract_artifacts_image(image_page_html_str, expected_result):
    assert artifacts.extract_artifacts_image(image_page_html_str) == expected_result

def test_extract_all_artifacts_images():
    with mock.patch.object(pathlib.Path, "iterdir") as mock_iterdir:
        iterdir_path_objs = [(pathlib.Path("C:/dig/html/artifacts") / filename)
                             for filename in ["img_aa0.html", "img_aj0.html"]]
        mock_iterdir.return_value = iterdir_path_objs
        assert artifacts.extract_all_artifacts_images("C:/", mock_readfile) == {
            "img_aa0.html": img_aa0_extracted,
            "img_aj0.html": img_aj0_extracted
        }

@pytest.mark.parametrize("ctrl_html_string,expected_result", [
    (ctrl_aj_html_str, ctrl_aj_extracted),
    (ctrl_fg_html_str, ctrl_fg_extracted)
])
def test_extract_excavation_zones(ctrl_html_string, expected_result):
    assert artifacts.extract_excavation_zones(ctrl_html_string, "C:/") == expected_result

@pytest.mark.parametrize("info_html_string,expected_result", [
    (info_aj0_html_str, info_aj0_extracted),
    (info_aj1_html_str, info_aj1_extracted),
    (info_aj2_html_str, info_aj2_extracted),
    (info_aj3_html_str, info_aj3_extracted),
    (info_aj4_html_str, info_aj4_extracted),
    (info_fg0_html_str, info_fg0_extracted),
    (info_fg1_html_str, info_fg1_extracted),
    (info_fg2_html_str, info_fg2_extracted),
    (info_fg3_html_str, info_fg3_extracted),
])
def test_extract_artifacts_list(info_html_string, expected_result):
    assert artifacts.extract_artifacts_list(info_html_string, "C:/") == expected_result

@pytest.mark.parametrize("art_html_string,expected_result", [
    (art_aj0_html_str, art_aj0_or_feature_15_fully_extracted),
    (art_aj2_html_str, art_aj0_or_feature_15_fully_extracted),
    (art_fg0_html_str, art_fg0_or_sq240r60_fully_extracted)
])
def test_extract_art_html_page(art_html_string, expected_result):
    assert artifacts.extract_art_html_page(
        art_html_string, "C:/", mock_readfile
    ) == expected_result

def test_extract_all_of_artifacts_dir():
    with mock.patch.object(pathlib.Path, "iterdir") as mock_iterdir:
        filenames_list = [
            "art_aj0.html", "art_aj2.html", "art_fg0.html",
            "ctrl_aj.html", "ctrl_fg.html",
            "info_aj0.html", "info_aj1.html", "info_aj2.html", "info_aj3.html", "info_aj4.html",
            "info_fg0.html", "info_fg1.html", "info_fg2.html", "info_fg3.html",
            "img_aa0.html", "img_aj0.html"
        ]
        iterdir_path_objs = [(pathlib.Path("C:/") / filename)
                             for filename in filenames_list]
        mock_iterdir.return_value = iterdir_path_objs
        assert artifacts.extract_all_of_artifacts_dir("C:/", mock_readfile) == {
            ctrl_aj_extracted["parentExcPage"]: art_aj0_or_feature_15_fully_extracted,
            ctrl_fg_extracted["parentExcPage"]: art_fg0_or_sq240r60_fully_extracted
        }

@pytest.mark.parametrize("db_html_str,expected_result", [
    (db0_0_html_str, db0_0_extracted),
    (db0_1_html_str, db0_1_extracted),
    (db0_2_html_str, db0_2_extracted),
    (db0_3_html_str, db0_3_extracted),
    (db6_0_html_str, db6_0_extracted),
    (db6_1_html_str, db6_1_extracted)
])
def test_extract_db_frame(db_html_str, expected_result):
    assert artifacts.extract_db_frame(db_html_str) == expected_result

@pytest.mark.parametrize("page_num,expected_result", [
    (0, {
        "name": head0_extracted,
        "pageNum": 0,
        "artifacts": db0_all_artifacts
    }),
    (6, {
        "name": head6_extracted,
        "pageNum": 6,
        "artifacts": db6_all_artifacts
    })
])
def test_extract_appendix_b_page(page_num, expected_result):
    with mock.patch.object(pathlib.Path, "iterdir") as mock_iterdir:
        filenames_list = [
            "db0_0.html", "db0_1.html", "db0_2.html", "db0_3.html",
            "db6_0.html", "db6_1.html",
            "foot0.html", "foot6.html",
            "head0.html", "head6.html",
            "page0.html", "page6.html"
        ]
        iterdir_path_objs = [(pathlib.Path("C:/dig/html/dbs") / filename)
                             for filename in filenames_list]
        mock_iterdir.return_value = iterdir_path_objs

        assert artifacts.extract_appendix_b_page(page_num, "C:/", mock_readfile) == expected_result

# TODO
# def test_extract_appendix_b():
#     assert artifacts.extract_appendix_b

def test_generate_cat_num_to_artifacts_dict():
    exc_page_name = art_fg0_or_sq240r60_fully_extracted["parentExcPage"]
    fg_artifacts_in_summary_dict = {
        exc_page_name: art_fg0_or_sq240r60_fully_extracted
    }
    db0_artifacts_in_details_dict = {
        head0_extracted: {
            "name": head0_extracted,
            "pageNum": 0,
            "artifacts": db0_all_artifacts
        }
    }
    assert artifacts.generate_cat_num_to_artifacts_dict(
        fg_artifacts_in_summary_dict, db0_artifacts_in_details_dict, True
    ) == {
        "2351b656": {
            "appendixBPageNum": None,
            "zoneNum": 0,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Animal Bone",
                "Size": '1/2"',
                "Count": "1",
                "Cat. No.": "2351b656",
                "Photo": None,
                "More": None
            }
        },
        "2351m3399": {
            "appendixBPageNum": None,
            "zoneNum": 0,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Baked Clay",
                "Size": '1/2"',
                "Count": "1",
                "Cat. No.": "2351m3399",
                "Photo": None,
                "More": None
            }
        },
        "2351a3397": {
            "appendixBPageNum": 5,
            "zoneNum": 0,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Biface",
                "Size": '1/2"',
                "Count": "1",
                "Cat. No.": "2351a3397",
                "Photo": None,
                "More": "/dig/html/dbs/page5.html"
            }
        },
        "2351a646": {
            "appendixBPageNum": 5,
            "zoneNum": 0,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Bifaces",
                "Size": '1/2"',
                "Count": "2",
                "Cat. No.": "2351a646",
                "Photo": None,
                "More": "/dig/html/dbs/page5.html"
            }
        },
        "2351b668": {
            "appendixBPageNum": None,
            "zoneNum": 1,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Animal Bone",
                "Size": '1/4"',
                "Count": "2",
                "Cat. No.": "2351b668",
                "Photo": None,
                "More": None
            }
        },
        "2351a666": {
            "appendixBPageNum": 3,
            "zoneNum": 1,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Bottle Glass (Lip)",
                "Size": '1/4"',
                "Count": "1",
                "Cat. No.": "2351a666",
                "Photo": None,
                "More": "/dig/html/dbs/page3.html"
            }
        },
        "2351m664": {
            "appendixBPageNum": None,
            "zoneNum": 1,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Daub",
                "Size": '1/2"',
                "Count": "3",
                "Cat. No.": "2351m664",
                "Photo": None,
                "More": None
            }
        },
        "2351m679": {
            "appendixBPageNum": 3,
            "zoneNum": 2,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Brick Fragments",
                "Size": '1/2"',
                "Count": "3",
                "Cat. No.": "2351m679",
                "Photo": None,
                "More": "/dig/html/dbs/page3.html"
            }
        },
        "2351p682": {
            "appendixBPageNum": 1,
            "zoneNum": 3,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Potsherd",
                "Size": '1/2"',
                "Count": "1",
                "Cat. No.": "2351p682",
                "Photo": None,
                "More": "/dig/html/dbs/page1.html"
            }
        },
        "2351a1038/a": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a1038/a",
                "Context": "Sq. 260R80"
            }],
            "summary": None
        },
        "2351a1076": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a1076",
                "Context": "Sq. 260R90"
            }],
            "summary": None
        },
        "2351a1110": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a1110",
                "Context": "Sq. 270R60"
            }, {
                "Catalog No.": "2351a1110",
                "Context": "Sq. 270R60"
            }],
            "summary": None
        },
        "2351a425": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a425",
                "Context": "Burial 2"
            }, {
                "Catalog No.": "2351a425",
                "Context": "Burial 2"
            }, {
                "Catalog No.": "2351a425",
                "Context": "Burial 2"
            }, {
                "Catalog No.": "2351a425",
                "Context": "Burial 2"
            }, {
                "Catalog No.": "2351a425",
                "Context": "Burial 2"
            }, {
                "Catalog No.": "2351a425",
                "Context": "Burial 2"
            }],
            "summary": None
        },
        "2351a4282          Type IIa": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a4282          Type IIa",
                "Context": "Sq. 250R50"
            }],
            "summary": None
        },
        "2351a4282          Type IVa": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a4282          Type IVa",
                "Context": "Sq. 250R50"
            }],
            "summary": None
        },
        "2351a6824/1        Type IIa": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a6824/1        Type IIa",
                "Context": "Feature 28"
            }, {
                "Catalog No.": "2351a6824/1        Type IIa",
                "Context": "Feature 28"
            }, {
                "Catalog No.": "2351a6824/1        Type IIa",
                "Context": "Feature 28"
            }, {
                "Catalog No.": "2351a6824/1        Type IIa",
                "Context": "Feature 28"
            }],
            "summary": None
        },
        "2351a6824/1        Type IVa": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2351a6824/1        Type IVa",
                "Context": "Feature 28"
            }],
            "summary": None
        },
        "2378w96            Type IIa": {
            "appendixBPageNum": 0,
            "zoneNum": None,
            "parentExcPage": None,
            "details": [{
                "Catalog No.": "2378w96            Type IIa",
                "Context": "Feature 42"
            }],
            "summary": None
        }
    }

def test_insert_details_into_summary_dict():
    # From info_fg1.html
    exc_page_name = art_fg0_or_sq240r60_fully_extracted["parentExcPage"]
    summary_dict = {
        "/dig/html/excavations/exc_fg.html": {
            "excavationElement": "Sq. 240R60",
            "parentExcPage": "/dig/html/excavations/exc_fg.html",
            "zones": [{
                "name": "Plow Zone",
                "pageName": "info_fg0.html",
                "artifacts": [{
                    "Artifacts": "Animal Bone",
                    "Size": '1/2"',
                    "Count": "1",
                    "Cat. No.": "2351b656",
                    "Photo": None,
                    "More": None
                }]
            }, {
                "name": "Plow Zone, 20-liter Waterscreen Sample",
                "pageName": "info_fg1.html",
                "artifacts": [{
                    "Artifacts": "Animal Bone",
                    "Size": '1/4"',
                    "Count": "2",
                    "Cat. No.": "2351b668",
                    "Photo": None,
                    "More": None
                }, {
                    "Artifacts": "Bottle Glass (Lip)",
                    "Size": '1/4"',
                    "Count": "1",
                    "Cat. No.": "2351a666",
                    "Photo": None,
                    "More": "/dig/html/dbs/page3.html"
                }, {
                    "Artifacts": "Daub",
                    "Size": '1/2"',
                    "Count": "3",
                    "Cat. No.": "2351m664",
                    "Photo": None,
                    "More": None
                }]
            }]
        }
    }
    artifacts_by_cat_no_dict = {
        "2351b656": {
            "appendixBPageNum": None,
            "zoneNum": 0,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Animal Bone",
                "Size": '1/2"',
                "Count": "1",
                "Cat. No.": "2351b656",
                "Photo": None,
                "More": None
            }
        },
        "2351b668": {
            "appendixBPageNum": None,
            "zoneNum": 1,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Animal Bone",
                "Size": '1/4"',
                "Count": "2",
                "Cat. No.": "2351b668",
                "Photo": None,
                "More": None
            }
        },
        "2351a666": {
            "appendixBPageNum": 3,
            "zoneNum": 1,
            "parentExcPage": exc_page_name,
            "details": [{
                "Catalog No.": "2351a666",
                "Context": "S240R60"
            }],
            "summary": {
                "Artifacts": "Bottle Glass (Lip)",
                "Size": '1/4"',
                "Count": "1",
                "Cat. No.": "2351a666",
                "Photo": None,
                "More": "/dig/html/dbs/page3.html"
            }
        },
        "2351m664": {
            "appendixBPageNum": None,
            "zoneNum": 0,
            "parentExcPage": exc_page_name,
            "details": None,
            "summary": {
                "Artifacts": "Daub",
                "Size": '1/2"',
                "Count": "3",
                "Cat. No.": "2351m664",
                "Photo": None,
                "More": None
            }
        },
    }
    assert artifacts.insert_details_into_summary_dict(summary_dict, artifacts_by_cat_no_dict) == {
        "/dig/html/excavations/exc_fg.html": {
            "excavationElement": "Sq. 240R60",
            "parentExcPage": "/dig/html/excavations/exc_fg.html",
            "zones": [{
                "name": "Plow Zone",
                "pageName": "info_fg0.html",
                "artifacts": [{
                    "Artifacts": "Animal Bone",
                    "Size": '1/2"',
                    "Count": "1",
                    "Cat. No.": "2351b656",
                    "Photo": None,
                    "More": None,
                    "details": None
                }]
            }, {
                "name": "Plow Zone, 20-liter Waterscreen Sample",
                "pageName": "info_fg1.html",
                "artifacts": [{
                    "Artifacts": "Animal Bone",
                    "Size": '1/4"',
                    "Count": "2",
                    "Cat. No.": "2351b668",
                    "Photo": None,
                    "More": None,
                    "details": None
                }, {
                    "Artifacts": "Bottle Glass (Lip)",
                    "Size": '1/4"',
                    "Count": "1",
                    "Cat. No.": "2351a666",
                    "Photo": None,
                    "More": "/dig/html/dbs/page3.html",
                    "details": [{
                        "Catalog No.": "2351a666",
                        "Context": "S240R60"
                    }]
                }, {
                    "Artifacts": "Daub",
                    "Size": '1/2"',
                    "Count": "3",
                    "Cat. No.": "2351m664",
                    "Photo": None,
                    "More": None,
                    "details": None
                }]
            }]
        }
    }
