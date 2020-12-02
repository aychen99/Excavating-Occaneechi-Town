from src.extract_old_site.modules import references as refs
import pytest
from pathlib import Path

# Portions of /dig/html/split/report282b.html, references pg. 1.
report_282b_sample_html_str = """
<html><body bgcolor=white>
<a name="ku">Abler, T. S., and Elisabeth Tooker</a><blockquote>
   1978  Seneca.  In <i>Handbook of North American Indians</i>, vol. 15, edited
by Bruce G. Trigger.  Smithsonian Institution, Washington, D.C.<p>
</blockquote><a name="go">Gwynn, John V.</a><blockquote>
   1964  <i>Virginia Upland Game Investigations: Restoration of the Wild
Turkey</i>.  Annual Report, Virginia Pittman-Robertson Project.<p>
</blockquote></body></html>
"""

# Portions of /dig/html/split/report283b.html, references pg. 2.
# Chosen to contain examples of references where the author has no letters
# but one of the references does,
# where an author has multiple references with letters,
# where an author has multiple references without letters,
# where an author has a single reference with letters,
# and where an author has a single reference without letters.
report_283b_sample_html_str = """
<html><body bgcolor=white>
<a name="bs">Hale, Horatio</a><blockquote>
   1883  The Tutelo Tribe and Language.  <i>Proceedings of the American
Philosophical Society</i> 21:114:1-47.<p>
</blockquote>Hammett, Julia E.<blockquote>
   1983  Preliminary Classification of North Carolina Shell Bead Artifacts:
Some Indications and Implications.  Ms. on file, Research Laboratories of
Anthropology, University of North Carolina, Chapel Hill.<p>
   1987  Shell Artifacts from the Carolina Piedmont.  In <i>The Siouan Project:
Seasons I and II</i>, edited by Roy S. Dickens Jr., H. Trawick Ward, and R. P.
Stephen Davis, Jr., pp. 167-183.  Monograph Series No. 1.  Research
Laboratories of Anthropology, University of North Carolina, Chapel Hill.<p>
</blockquote><a name="iu">Horn, Henry S.</a><blockquote>
   1974  The Ecology of Secondary Succession.  <i>Annual Review of Ecology and
Systematics</i> 5:25-37.<p>
   1978  Optimal Tactics of Reproduction and Life-History.  In <i>Behavioral
Ecology: An Evolutionary Approach</i>, edited by J. R. Krebs and N. B. Davies,
pp 411-429.  Blackwell Scientific Publications, Oxford.<p>
</blockquote><a name="cx">Hudson, Charles M.</a><blockquote>
   1970  <i>The Catawba Nation</i>.  University of Georgia Press, Athens.<p>
   <a name="bu">1976</a>  <i>The Southeastern Indians</i>.  The University of Tennessee Press,
Knoxville.<p>
</blockquote>Morris, Percy C.<blockquote>
   1975  <i>A Field Guide to Shells of the Atlantic and Gulf Coasts and the
West Indies</i>.  Houghton Mifflin Co., Boston.<p>
</blockquote><a name="ax">Morrison, A. J.</a><blockquote>
   1921  The Virginia Indian Trade to 1673.  <i>William and Mary Quarterly</i>
(2nd ser.) 1:217-236.<p>
</blockquote>Myers, Albert Cook (editor)<blockquote>
   1970  <i>William Penn's Own Account of the Lenni Lenape or Delaware
Indians</i>.  The Middle Atlantic Press, Somerset.<p>
</blockquote>Petherick, Gary L.<blockquote>
   1985  Architecture and Features at the Fredricks, Wall, and Mitchum Sites.
In <i>The Historic Occaneechi: An Archaeological Investigation of Culture
Change.  Final Report of 1984 Investigations</i>, edited by Roy S. Dickens,
Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr., pp. 53-178.  Research
Laboratories of Anthropology, University of North Carolina, Chapel Hill.<p>
   <a name="lk">1987</a>  Architecture and Features at the Fredricks, Wall, and Mitchum Sites.
In <i>The Siouan Project: Seasons I and II</i>, edited by Roy S. Dickens, Jr.,
H. Trawick Ward and R. P. Stephen Davis, Jr., pp. 29-80.  Monograph Series No.
1, Research Laboratories of Anthropology, University of North Carolina, Chapel
Hill.<p>
</blockquote><a name="dy">Rush County Clerk of Courts</a><blockquote>
   1869  Court Papers: Jefries vs. O'Brien case of 1869.  Rushville, Indiana.<p>
</blockquote></body></html>
"""

# Portions of /dig/html/split/report284b.html, references pg. 3
report_284b_sample_html_str = """
<html><body bgcolor=white>
<a name="ky">Sahlins, Marshall D.</a><blockquote>
   1968  <i>Tribesmen</i>.  Prentice-Hall, Inc., Englewood Cliffs, New
Jersey.<p>
</blockquote>Sainesbury, W. N. (editor)<blockquote>
   1893  Calendar of State Papers, Colonial Series, America and the West
Indies, 1669-1674.  Printed for Her Majesty's Stationery Office by Eyre and
Spottiswoods, London.<p>
</blockquote><a name="hn">Yarnell, Richard A., and M. Jean Black</a><blockquote>
   1983  Temporal Trends Indicated by a Survey of Prehistoric Plant Food
Remains from Southeastern North America.  Revised version of a paper presented
at the 40th Annual Meeting of the Southeastern Archaeological Conference,
Columbia, South Carolina.<p>
   <a name="iz">1985</a>  Temporal Trends Indicated by a Survey of Archaic and Woodland Plant
Food Remains from Southeastern North America. <i>Southeastern Archaeology</i>
4:93-106.<p>
</blockquote></body></html>
"""


report_282b_extracted = {
    "refs": {
        "Abler, T. S., and Elisabeth Tooker": [
            ("1978  Seneca.  In <i>Handbook of North American Indians</i>, vol. 15, edited "
             "by Bruce G. Trigger.  Smithsonian Institution, Washington, D.C.")
        ],
        "Gwynn, John V.": [
            ("1964  <i>Virginia Upland Game Investigations: Restoration of the Wild "
             "Turkey</i>.  Annual Report, Virginia Pittman-Robertson Project.")
        ]
    },
    "hrefsToRefs": {
        "ku": {
            "author": "Abler, T. S., and Elisabeth Tooker",
            "refNum": 0
        },
        "go": {
            "author": "Gwynn, John V.",
            "refNum": 0
        }
    }
}

report_283b_extracted = {
    "refs": {
        "Hale, Horatio": [
            ("1883  The Tutelo Tribe and Language.  "
             "<i>Proceedings of the American Philosophical Society</i> 21:114:1-47.")
        ],
        "Hammett, Julia E.": [
            ("1983  Preliminary Classification of North Carolina Shell Bead Artifacts: "
             "Some Indications and Implications.  Ms. on file, Research Laboratories "
             "of Anthropology, University of North Carolina, Chapel Hill."),
            ("1987  Shell Artifacts from the Carolina Piedmont.  In <i>The Siouan Project: "
             "Seasons I and II</i>, edited by Roy S. Dickens Jr., H. Trawick Ward, and R. P. "
             "Stephen Davis, Jr., pp. 167-183.  Monograph Series No. 1.  Research "
             "Laboratories of Anthropology, University of North Carolina, Chapel Hill.")
        ],
        "Horn, Henry S.": [
            ("1974  The Ecology of Secondary Succession.  <i>Annual Review of Ecology and "
             "Systematics</i> 5:25-37."),
            ("1978  Optimal Tactics of Reproduction and Life-History.  In <i>Behavioral "
             "Ecology: An Evolutionary Approach</i>, edited by J. R. Krebs and N. B. Davies, "
             "pp 411-429.  Blackwell Scientific Publications, Oxford.")
        ],
        "Hudson, Charles M.": [
            ("1970  <i>The Catawba Nation</i>.  University of Georgia Press, Athens."),
            ("1976  <i>The Southeastern Indians</i>.  The University of Tennessee Press, "
             "Knoxville.")
        ],
        "Morris, Percy C.": [
            ("1975  <i>A Field Guide to Shells of the Atlantic and Gulf Coasts and the "
             "West Indies</i>.  Houghton Mifflin Co., Boston.")
        ],
        "Morrison, A. J.": [
            ("1921  The Virginia Indian Trade to 1673.  <i>William and Mary Quarterly</i> "
             "(2nd ser.) 1:217-236.")
        ],
        "Myers, Albert Cook (editor)": [
            ("1970  <i>William Penn's Own Account of the Lenni Lenape or Delaware "
             "Indians</i>.  The Middle Atlantic Press, Somerset.")
        ],
        "Petherick, Gary L.": [
            ("1985  Architecture and Features at the Fredricks, Wall, and Mitchum Sites. "
             "In <i>The Historic Occaneechi: An Archaeological Investigation of Culture "
             "Change.  Final Report of 1984 Investigations</i>, edited by Roy S. Dickens, "
             "Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr., pp. 53-178.  Research "
             "Laboratories of Anthropology, University of North Carolina, Chapel Hill."),
            ("1987  Architecture and Features at the Fredricks, Wall, and Mitchum Sites. "
             "In <i>The Siouan Project: Seasons I and II</i>, edited by Roy S. Dickens, Jr., "
             "H. Trawick Ward and R. P. Stephen Davis, Jr., pp. 29-80.  Monograph Series No. "
             "1, Research Laboratories of Anthropology, University of North Carolina, Chapel "
             "Hill.")
        ],
        "Rush County Clerk of Courts": [
            ("1869  Court Papers: Jefries vs. O'Brien case of 1869.  Rushville, Indiana.")
        ]
    },
    "hrefsToRefs": {
        "bs": {
            "author": "Hale, Horatio",
            "refNum": 0
        },
        "iu": {
            "author": "Horn, Henry S.",
            "refNum": 0
        },
        "cx": {
            "author": "Hudson, Charles M.",
            "refNum": 0
        },
        "bu": {
            "author": "Hudson, Charles M.",
            "refNum": 1
        },
        "ax": {
            "author": "Morrison, A. J.",
            "refNum": 0
        },
        "lk": {
            "author": "Petherick, Gary L.",
            "refNum": 1
        },
        "dy": {
            "author": "Rush County Clerk of Courts",
            "refNum": 0
        }
    }
}

report_284b_extracted = {
    "refs": {
        "Sahlins, Marshall D.": [
            ("1968  <i>Tribesmen</i>.  Prentice-Hall, Inc., Englewood Cliffs, New "
             "Jersey.")
        ],
        "Sainesbury, W. N. (editor)": [
            ("1893  Calendar of State Papers, Colonial Series, America and the West "
             "Indies, 1669-1674.  Printed for Her Majesty's Stationery Office by Eyre and "
             "Spottiswoods, London.")
        ],
        "Yarnell, Richard A., and M. Jean Black": [
            ("1983  Temporal Trends Indicated by a Survey of Prehistoric Plant Food "
             "Remains from Southeastern North America.  Revised version of a paper presented "
             "at the 40th Annual Meeting of the Southeastern Archaeological Conference, "
             "Columbia, South Carolina."),
            ("1985  Temporal Trends Indicated by a Survey of Archaic and Woodland Plant "
             "Food Remains from Southeastern North America. <i>Southeastern Archaeology</i> "
             "4:93-106.")
        ]
    },
    "hrefsToRefs": {
        "ky": {
            "author": "Sahlins, Marshall D.",
            "refNum": 0
        },
        "hn": {
            "author": "Yarnell, Richard A., and M. Jean Black",
            "refNum": 0
        },
        "iz": {
            "author": "Yarnell, Richard A., and M. Jean Black",
            "refNum": 1
        }
    }
}

all_sample_refs_extracted = {
    "refs": {
        "Abler, T. S., and Elisabeth Tooker": [
            ("1978  Seneca.  In <i>Handbook of North American Indians</i>, vol. 15, edited "
             "by Bruce G. Trigger.  Smithsonian Institution, Washington, D.C.")
        ],
        "Gwynn, John V.": [
            ("1964  <i>Virginia Upland Game Investigations: Restoration of the Wild "
             "Turkey</i>.  Annual Report, Virginia Pittman-Robertson Project.")
        ],
        "Hale, Horatio": [
            ("1883  The Tutelo Tribe and Language.  "
             "<i>Proceedings of the American Philosophical Society</i> 21:114:1-47.")
        ],
        "Hammett, Julia E.": [
            ("1983  Preliminary Classification of North Carolina Shell Bead Artifacts: "
             "Some Indications and Implications.  Ms. on file, Research Laboratories "
             "of Anthropology, University of North Carolina, Chapel Hill."),
            ("1987  Shell Artifacts from the Carolina Piedmont.  In <i>The Siouan Project: "
             "Seasons I and II</i>, edited by Roy S. Dickens Jr., H. Trawick Ward, and R. P. "
             "Stephen Davis, Jr., pp. 167-183.  Monograph Series No. 1.  Research "
             "Laboratories of Anthropology, University of North Carolina, Chapel Hill.")
        ],
        "Horn, Henry S.": [
            ("1974  The Ecology of Secondary Succession.  <i>Annual Review of Ecology and "
             "Systematics</i> 5:25-37."),
            ("1978  Optimal Tactics of Reproduction and Life-History.  In <i>Behavioral "
             "Ecology: An Evolutionary Approach</i>, edited by J. R. Krebs and N. B. Davies, "
             "pp 411-429.  Blackwell Scientific Publications, Oxford.")
        ],
        "Hudson, Charles M.": [
            ("1970  <i>The Catawba Nation</i>.  University of Georgia Press, Athens."),
            ("1976  <i>The Southeastern Indians</i>.  The University of Tennessee Press, "
             "Knoxville.")
        ],
        "Morris, Percy C.": [
            ("1975  <i>A Field Guide to Shells of the Atlantic and Gulf Coasts and the "
             "West Indies</i>.  Houghton Mifflin Co., Boston.")
        ],
        "Morrison, A. J.": [
            ("1921  The Virginia Indian Trade to 1673.  <i>William and Mary Quarterly</i> "
             "(2nd ser.) 1:217-236.")
        ],
        "Myers, Albert Cook (editor)": [
            ("1970  <i>William Penn's Own Account of the Lenni Lenape or Delaware "
             "Indians</i>.  The Middle Atlantic Press, Somerset.")
        ],
        "Petherick, Gary L.": [
            ("1985  Architecture and Features at the Fredricks, Wall, and Mitchum Sites. "
             "In <i>The Historic Occaneechi: An Archaeological Investigation of Culture "
             "Change.  Final Report of 1984 Investigations</i>, edited by Roy S. Dickens, "
             "Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr., pp. 53-178.  Research "
             "Laboratories of Anthropology, University of North Carolina, Chapel Hill."),
            ("1987  Architecture and Features at the Fredricks, Wall, and Mitchum Sites. "
             "In <i>The Siouan Project: Seasons I and II</i>, edited by Roy S. Dickens, Jr., "
             "H. Trawick Ward and R. P. Stephen Davis, Jr., pp. 29-80.  Monograph Series No. "
             "1, Research Laboratories of Anthropology, University of North Carolina, Chapel "
             "Hill.")
        ],
        "Rush County Clerk of Courts": [
            ("1869  Court Papers: Jefries vs. O'Brien case of 1869.  Rushville, Indiana.")
        ],
        "Sahlins, Marshall D.": [
            ("1968  <i>Tribesmen</i>.  Prentice-Hall, Inc., Englewood Cliffs, New "
             "Jersey.")
        ],
        "Sainesbury, W. N. (editor)": [
            ("1893  Calendar of State Papers, Colonial Series, America and the West "
             "Indies, 1669-1674.  Printed for Her Majesty's Stationery Office by Eyre and "
             "Spottiswoods, London.")
        ],
        "Yarnell, Richard A., and M. Jean Black": [
            ("1983  Temporal Trends Indicated by a Survey of Prehistoric Plant Food "
             "Remains from Southeastern North America.  Revised version of a paper presented "
             "at the 40th Annual Meeting of the Southeastern Archaeological Conference, "
             "Columbia, South Carolina."),
            ("1985  Temporal Trends Indicated by a Survey of Archaic and Woodland Plant "
             "Food Remains from Southeastern North America. <i>Southeastern Archaeology</i> "
             "4:93-106.")
        ]
    },
    "hrefsToRefs": {
        "ku": {
            "author": "Abler, T. S., and Elisabeth Tooker",
            "refNum": 0
        },
        "go": {
            "author": "Gwynn, John V.",
            "refNum": 0
        },
        "bs": {
            "author": "Hale, Horatio",
            "refNum": 0
        },
        "iu": {
            "author": "Horn, Henry S.",
            "refNum": 0
        },
        "cx": {
            "author": "Hudson, Charles M.",
            "refNum": 0
        },
        "bu": {
            "author": "Hudson, Charles M.",
            "refNum": 1
        },
        "ax": {
            "author": "Morrison, A. J.",
            "refNum": 0
        },
        "lk": {
            "author": "Petherick, Gary L.",
            "refNum": 1
        },
        "dy": {
            "author": "Rush County Clerk of Courts",
            "refNum": 0
        },
        "ky": {
            "author": "Sahlins, Marshall D.",
            "refNum": 0
        },
        "hn": {
            "author": "Yarnell, Richard A., and M. Jean Black",
            "refNum": 0
        },
        "iz": {
            "author": "Yarnell, Richard A., and M. Jean Black",
            "refNum": 1
        }
    }
}

def mock_readfile(filename, parent_dir_path_obj):
    if parent_dir_path_obj.as_posix() == "C:/dig/html/part6":
        pass
    if parent_dir_path_obj.as_posix() == "C:/dig/html/split":
        if filename == "report282b.html":
            return report_282b_sample_html_str
        elif filename == "report283b.html":
            return report_283b_sample_html_str
        elif filename == "report284b.html":
            return report_284b_sample_html_str

    raise Exception("failed to find file path in mock_readfile")

@pytest.mark.parametrize("ref_reportb_html_str,expected_results", [
    (report_282b_sample_html_str, report_282b_extracted),
    (report_283b_sample_html_str, report_283b_extracted),
    (report_284b_sample_html_str, report_284b_extracted)
])
def test_extract_references_page(ref_reportb_html_str, expected_results):
    assert refs.extract_references_page(ref_reportb_html_str) == expected_results

def test_extract_all_references():
    assert refs.extract_all_references("C:/dig", mock_readfile) == all_sample_refs_extracted

# TODO
# def test_validate_ref_page():
#     pass

# def test_validate_all_ref_pages():
#     pass
