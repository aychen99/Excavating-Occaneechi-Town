from src.extract_old_site.modules import standard_text_chapter

def test_extract_page_title():
    test_data = "<html><body><center><i>Historical Background</i></center></body></html>"
    assert standard_text_chapter.extract_page_title(test_data) == "Historical Background"

def test_extract_page_number():
    test_data1 = "<html><body><center>Page i</center></body></html>"
    test_data2 = "<html><body><center>Page 51</center></body></html>"
    assert standard_text_chapter.extract_page_number(test_data1) == "i"
    assert standard_text_chapter.extract_page_number(test_data2) == "51"

def test_extract_sidebar():
    test_data1 = """<html><body><p>
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
    extracted = standard_text_chapter.extract_sidebar(test_data1, '/dig/html/part2', 'body0_2.html')
    assert extracted['currentModuleFullName'] == 'Archaeological Background'
    assert extracted['moduleAuthor'] == 'by Dickens, Roy S., Jr., H. Trawick Ward, and R. P. Stephen Davis, Jr.'
    assert extracted['sections'] == test1_sections

    test_data2 = """<html><body><p>
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
    extracted = standard_text_chapter.extract_sidebar(test_data2, '/dig/html/part4', 'body0_05.html')
    assert extracted['currentModuleFullName'] == 'Animal Remains: 1983-1984 Excavations'
    assert extracted['moduleAuthor'] == 'by Mary Ann Holm'
    assert extracted['sections'] == test2_sections

def test_extract_topbar():
    test_data = """<html><body><b>
                   Archaeology |
                   <a target="_parent" href="tab1.html">History (1525-1725)</a> |
                   <a target="_parent" href="tab2.html">History (1725-present)</a> |
                   <a target="_parent" href="../index.html">Home</a> |
                   <a target="_parent" href="../copyright.html">Copyright</a>
                   </b></body></html>"""
    assert standard_text_chapter.extract_topbar(test_data, '/dig/html/part2', 'tab0.html') == [{
        "moduleShortName": "Archaeology",
        "path": "/dig/html/part2/tab0.html"
    }, {
        "moduleShortName": "History (1525-1725)",
        "path": "/dig/html/part2/tab1.html"
    }, {
        "moduleShortName": "History (1725-present)",
        "path": "/dig/html/part2/tab2.html"
    }]

def test_extract_frames():
    def readfile(filename):
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
    assert standard_text_chapter.extract_frames(test_data, readfile) == ["a", "b", "c"]