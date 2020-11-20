from pytest import mark
from unittest import mock
from unittest.mock import patch
from src.generate_new_site.site_data_structs import archaeology_primer as ap
from pathlib import Path


###################################
# Test add_child() and set_path() #
###################################

@patch('src.generate_new_site.site_data_structs.archaeology_primer.PrimerChapter.set_path')
def test_primer_chapter_add_child(mock_set_path):
    chapter = ap.PrimerChapter(name="Test Chapter", parent=None, path=None)

    # Mock modules
    module_1 = mock.Mock()
    module_2 = mock.Mock()

    # Assert call to set_path
    chapter.add_child(module_1)
    mock_set_path.assert_called_once()
    mock_set_path.reset_mock()

    # Assert no call to set_path if chapter.path is not None
    chapter.path = "arbitrary value"
    chapter.add_child(module_2)
    mock_set_path.assert_not_called()


def test_primer_chapter_set_path():
    chapter = ap.PrimerChapter(name="Test Chapter", parent=None, path=None)

    testpath = Path("manually_set")

    child1 = mock.Mock(path=Path("path1"))
    child2 = mock.Mock(path=Path("path2"))

    assert(chapter.path is None)

    # Ensure path is set if path is none when child is added
    chapter.add_child(child1)
    assert(chapter.path == child1.path)

    chapter.add_child(child2)
    assert(chapter.path == child1.path)

    chapter.path = None
    chapter.set_path()

    assert(chapter.path == child1.path)

    chapter.set_path(testpath)
    assert(chapter.path == testpath)


################
# Test write() #
################

@patch('src.generate_new_site.site_data_structs.archaeology_primer.rel_path', return_value=Path("relpath"))
@patch('jinja2.Template.render')
@patch('src.generate_new_site.site_data_structs.archaeology_primer.update_text_paragraph', return_value="touched")
@patch('src.generate_new_site.site_data_structs.site.SitePage.write')
def test_primer_page_write(mock_super_write, mock_update_content, mock_render, mock_rel_path):
    # Set up mock objects
    next = Path("next")
    prev = Path("prev")

    children = "arbitary"
    ch_name = "chapter"
    mo_long_name = "module"

    module = mock.Mock(long_name=mo_long_name)
    module.parent = mock.Mock()
    module.parent.name = ch_name
    module.parent.parent = mock.Mock(children=children)
    module.parent.parent.pagetable.get_next_page_path = mock.Mock(return_value=next)
    module.parent.parent.pagetable.get_prev_page_path = mock.Mock(return_value=prev)

    # Instantiate page
    content = [
        {'type': None, 'content': "content 1"},
        {'type': None, 'content': "content 2"}
    ]
    path = Path("page.html")
    page = ap.PrimerPage(
        name="page",
        path=path,
        content=content,
        parent=module,
        image=None,
        page_num="5"
    )

    with patch('src.generate_new_site.site_data_structs.archaeology_primer.Path.open', mock.mock_open()):
        page.write()

        # Assert next and prev paths are made relative
        mock_rel_path.assert_any_call(next, path)
        mock_rel_path.assert_any_call(prev, path)

        # Assert that content is updated
        for content_obj in content:
            assert content_obj['content'] == "touched"

        # Assert that we call render with all of the args the template expects
        mock_render.assert_called_once_with(
            chapters=children,
            this_chapter_name=ch_name,
            this_module_name=mo_long_name,
            this_section_name=page.name,
            this_section=page,
            pagination={
                'prev_page_href': Path("relpath").as_posix(),
                'this_page_num': page.page_num,
                'next_page_href': Path("relpath").as_posix()
            }
        )
        # Assert that we call super().write()
        mock_super_write.assert_called()
