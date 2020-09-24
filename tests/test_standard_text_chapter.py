from src.extract_old_site.modules import standard_text_chapter

def test_extract_page_title():
    assert standard_text_chapter.extract_page_title("<html><body><center><i>Historical Background</i></center></body></html>") == "Historical Background"

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