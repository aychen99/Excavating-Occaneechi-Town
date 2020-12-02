from src.generate_new_site.utilities import process_content
from src.generate_new_site.site_data_structs.site import Index
from src.generate_new_site.site_data_structs.references import References
from src.generate_new_site.site_data_structs.tables import Tables
from src.generate_new_site.utilities.tables import PathTable
from src.generate_new_site.site_data_structs.figure import Figure, Figures
from bs4 import BeautifulSoup
from unittest import mock
import pytest
import pathlib

# Example data
raw_paragraph_with_slid_link = (
    'This paragraph has a link to an image: <a href="/html/excavations/slid_abc.html">Image</a>'
)

raw_paragraph_with_ref_link = (
    'This paragraph has a reference: <a href="/html/part6/ref_ab.html">Reference</a>'
)

raw_paragraph_with_table_link = (
    'We have a table here: <a href="/html/tables/table0.html">Table</a>'
)

raw_paragraph_with_table_with_images_link = (
    'We have a table here: <a href="/html/tables/table2.html">Table</a>'
)

raw_paragraph_with_part_links = (
    'We have links to many parts here: <a href="../part2/body0.html">Part 2</a>\n'
    '<a href="/html/part3/body0.html">Part 3</a>\n'
    '<a href="/html/part4/body0.html">Part 4</a>\n'
    '<a href="/html/part5/body0.html">Part 5</a>\n'
    '<a href="/html/part5/body0_2.html">A Section in Part 5</a>\n'
    '<a href="/html/body0.html">The Current Part, Part 0</a>\n'
)

raw_paragraph_with_excavations_link = (
    'We have an excavation element that is not just an image: '
    '<a href="/html/excavations/exc_az.html">Excavation</a>'
)



index = Index(pathlib.Path("testdir"))
# Add figuretable, datatables, references, pathtable
references = References(index)
references.references = {
    "Alvord, Clarence W., and Lee Bidgood (editors)": [
        "1912  <i>The First Explorations of the Trans-Allegheny Region by the Virginians, 1650</i>-<i>1674</i>.  Arthur H. Clark Co., Cleveland."
    ]
}
references.old_reference_letters = {
    "ab": {
        "author": "Alvord, Clarence W., and Lee Bidgood (editors)",
        "refNum": 0
    }
}
index.add_references(references)

figures = Figures(index)
figure_abc = Figure(
    "773", "Sq. 210R100, top of subsoil (view to north).", pathlib.Path("/html/images/2/210r100.gif"),
    "/html/excavations/slid_abc.html", pathlib.Path("/figures/figure_0773.html"), figures,
    390, 390
)
figure_auh = Figure(
    "156", "Vessel 1, a Uwharrie Net Impressed jar from Feature 8 (RLA catalog no. 2351p2711).", pathlib.Path("/html/images/d16/d_3553.jpeg"),
    "/html/excavations/slid_auh.html", pathlib.Path("/figures/figure_0156.html"), figures,
    390, 364
)
figure_auk = Figure(
    "134", "Vessel 2, a Fredricks Check Stamped jar from Burial 1 (RLA catalog no. 2351p255/1).", pathlib.Path("/html/images/d16/d_3556.jpeg"),
    "/html/excavations/slid_auk.html", pathlib.Path("/figures/figure_0134.html"), figures,
    317, 352
)
figures.register(figure_abc)
figures.register(figure_auh)
figures.register(figure_auk)
index.add_figures(figures)

datatables = Tables(index)
datatables.register_table("0", {
    "tableNum": "1",
    "caption": "Summary of pottery recovered from the Fredricks site.",
    "table": ("==========================================================\n"
              " Excavation  Features/                          Total  \n "
              "Season      Burials  Structures  Plowzone    n        %\n"
              "==========================================================\n"
              " 1983          725         0      2,059    2,784     4.43\n"
              " 1984        1,077        28      7,345    8,450    13.47\n"
              " 1985        2,620        62     20,926   23,608    37.62\n"
              " 1986        3,365         0     24,545   27,910    44.48\n\n"
              " Total       7,787        90     54,875   62,752   100.00\n"
              "==========================================================")
})
datatables.register_table("2", {
    "tableNum": "3",
    "caption": "Formal attributes for whole vessels and reconstructed vessel sections from the Fredricks site.",
    "table": ("=======================================================================================\n"
              " Vessel No. (click to view pot)\n"
              " |               Exterior     Interior Decoration/    Vessel  Rim     Lip     Base\n"
              " | Temper Type   Surface      Surface  Modification    Type  Profile  Form    Form\n"
              "=======================================================================================\n"
              " <a href=\"tab2_0.html\">1</a> Fine Quartz  Net Impressed  Scraped Incising (Neck) Jar  Everted  Rounded    -\n"
              " <a href=\"tab2_1.html\">2</a> Fine Sand    Check Stamped  Plain   None            Jar  Everted  Flat       -\n"
              "=====================================================================================")
})
datatables.register_path("/html/tables/table0.html", "0")
datatables.register_path("/html/tables/table2.html", "2")
datatables.register_image_paths({
    "tab2_0.html": "156",
    "tab2_1.html": "134"
})
index.add_tables(datatables)

pathtable = index.pathtable

# Updated Paragraphs
updated_paragraph_with_slid_link = (
    '<html><head></head><body>This paragraph has a link to an image: <a class="a-img" data-src="../../imgs/2/210r100.gif" '
    'data-sub-html="&lt;b&gt;Figure 773&lt;/b&gt;. Sq. 210R100, top of subsoil (view to north)." '
    'href="../../imgs/2/210r100.gif">Image</a></body></html>'
)

updated_paragraph_with_ref_link = (
    'This paragraph has a reference: <a href="#genModal" data-toggle="modal"'
    'data-target="#genModal" class="a-ref" data-author="Alvord, Clarence W., and Lee Bidgood (editors)"'
    'data-ref-text="1912  <i>The First Explorations of the Trans-Allegheny Region by the Virginians, 1650</i>-<i>1674</i>.  Arthur H. Clark Co., Cleveland.">'
    'Reference</a>'
)

updated_paragraph_with_table_link = (
    'We have a table here: <a href="#genModal" data-toggle="modal" data-target="#genModal"'
    'class="a-table" data-table-header="<b>Table 1</b>. Summary of pottery recovered from the Fredricks site."'
    'data-table-string="'
    '==========================================================\n'
    ' Excavation  Features/                          Total  \n '
    'Season      Burials  Structures  Plowzone    n        %\n'
    '==========================================================\n'
    ' 1983          725         0      2,059    2,784     4.43\n'
    ' 1984        1,077        28      7,345    8,450    13.47\n'
    ' 1985        2,620        62     20,926   23,608    37.62\n'
    ' 1986        3,365         0     24,545   27,910    44.48\n\n'
    ' Total       7,787        90     54,875   62,752   100.00\n'
    '=========================================================='
    '">Table</a>'
)

updated_paragraph_with_table_with_images_link = (
    'We have a table here: <a href="#genModal" data-toggle="modal" data-target="#genModal"'
    'class="a-table" data-table-header="<b>Table 3</b>. Formal attributes for whole vessels and reconstructed vessel sections from the Fredricks site."'
    'data-table-string="">Table</a>'
)

soup = BeautifulSoup(updated_paragraph_with_table_with_images_link, 'html5lib').body
table_soup = BeautifulSoup((
        "=======================================================================================\n"
        " Vessel No. (click to view pot)\n"
        " |               Exterior     Interior Decoration/    Vessel  Rim     Lip     Base\n"
        " | Temper Type   Surface      Surface  Modification    Type  Profile  Form    Form\n"
        "=======================================================================================\n"
        " <a href=\"tab2_0.html\">1</a> Fine Quartz  Net Impressed  Scraped Incising (Neck) Jar  Everted  Rounded    -\n"
        " <a href=\"tab2_1.html\">2</a> Fine Sand    Check Stamped  Plain   None            Jar  Everted  Flat       -\n"
        "====================================================================================="
    ), 'html5lib').body
first_img_a = table_soup.find_all('a')[0]
second_img_a = table_soup.find_all('a')[1]
first_img_a['href'] = '#tableImgModal'
first_img_a['data-toggle'] = 'modal'
first_img_a['data-target'] = '#tableImgModal'
first_img_a['data-figure-caption'] = '<b>Figure 156</b>. Vessel 1, a Uwharrie Net Impressed jar from Feature 8 (RLA catalog no. 2351p2711).'
first_img_a['data-figure-path'] = '../../imgs/d16/d_3553.jpeg'
second_img_a['href'] = '#tableImgModal'
second_img_a['data-toggle'] = 'modal'
second_img_a['data-target'] = '#tableImgModal'
second_img_a['data-figure-caption'] = '<b>Figure 134</b>. Vessel 2, a Fredricks Check Stamped jar from Burial 1 (RLA catalog no. 2351p255/1).'
second_img_a['data-figure-path'] = '../../imgs/d16/d_3556.jpeg'
soup.a['data-table-string'] = str(table_soup).replace('<body>', '').replace('</body>', '')
updated_paragraph_with_table_with_images_link = str(soup).replace('<body>', '').replace('</body>', '')

@pytest.mark.parametrize("paragraph_string,path,expected_result", [
    (raw_paragraph_with_ref_link, pathlib.Path("/"), updated_paragraph_with_ref_link),
    (raw_paragraph_with_slid_link, pathlib.Path("/"), updated_paragraph_with_slid_link),
    (raw_paragraph_with_table_link, pathlib.Path("/"), updated_paragraph_with_table_link),
    (raw_paragraph_with_table_with_images_link, pathlib.Path("/"), updated_paragraph_with_table_with_images_link)
])
def test_update_text_paragraph(paragraph_string, path, expected_result):
    assert BeautifulSoup(
        process_content.update_text_paragraph(paragraph_string, index, path), 'html5lib'
    ) == BeautifulSoup(expected_result, 'html5lib')
