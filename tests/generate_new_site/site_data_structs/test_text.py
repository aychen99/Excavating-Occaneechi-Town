from pytest import mark
from unittest import mock
from unittest.mock import patch
from src.generate_new_site.site_data_structs import text
from pathlib import Path


###################################
# Test add_child() and set_path() #
###################################

# @parametrize("test_json_data,test_name,test_dir,expected_chapter_attrs",
#              (
#                 None,
#                 "Test1",
#                 Path("test"),
#                 None
#              ))
# def test_text_chapter_from_json(test_json_data, test_name, test_dir, expected_chapter_attrs):
#     index = mock.Mock()
#     test_json_path = mock.Mock()
#     test_json_path.open = mock.mock_open(read_data=test_json_data)
#     chapter = text.TextChapter.from_json(
#         json_path=test_json_path,
#         name=test_name,
#         dir=test_dir,
#         index=index
#     )
#     pass


###################################
# Test add_child() and set_path() #
###################################

@patch('src.generate_new_site.site_data_structs.text.TextChapter.set_path')
def test_text_chapter_add_child(mock_set_path):
    chapter = text.TextChapter(name="Test Chapter", parent=None, path=None)

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


@patch('src.generate_new_site.site_data_structs.text.TextModule.set_path')
def test_text_module_add_child(mock_set_path):
    module = text.TextModule(
        short_name="Test Module 1",
        long_name="Test Module 1",
        parent=None,
        path=None
    )
    # Mock pages
    page_1 = mock.Mock()
    page_2 = mock.Mock()

    # Assert call to set_path, module having no path
    module.add_child(page_1)
    mock_set_path.assert_called_once()
    mock_set_path.reset_mock()

    # Assert no call to set_path if module.path is not None
    module.path = "arbitrary value"
    module.add_child(page_2)
    mock_set_path.assert_not_called()


def test_text_chapter_set_path():
    chapter = text.TextChapter(name="Test Chapter", parent=None, path=None)

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


def test_text_module_set_path():
    module = text.TextModule(
        short_name="Test Module 1",
        long_name="Test Module 1",
        parent=None,
        path=None
    )

    child1 = mock.Mock(path=Path("path1"))
    child2 = mock.Mock(path=Path("path2"))

    assert(module.path is None)

    # Ensure path is set if path is none when child is added
    module.add_child(child1)
    assert(module.path == child1.path)

    module.add_child(child2)
    assert(module.path == child1.path)

    module.path = None
    module.set_path()

    assert(module.path == child1.path)




################
# Test write() #
################

@patch('src.generate_new_site.site_data_structs.text.rel_path', return_value=Path("relpath"))
@patch('jinja2.Template.render')
@patch('src.generate_new_site.site_data_structs.text.update_text_paragraph', return_value="touched")
@patch('src.generate_new_site.site_data_structs.site.SitePage.write')
def test_text_page_write(mock_super_write, mock_update_content, mock_render, mock_rel_path):
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
        {'content': "content 1"},
        {'content': "content 2"}
    ]
    other_info = "hocuspocus"
    path = Path("page.html")
    page = text.TextPage(
        name="page",
        path=path,
        content=content,
        parent=module,
        other_info=other_info,
        page_num="5"
    )

    with patch('src.generate_new_site.site_data_structs.text.Path.open', mock.mock_open()):
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
            other_info=other_info,
            pagination={
                'prev_page_href': Path("relpath").as_posix(),
                'this_page_num': page.page_num,
                'next_page_href': Path("relpath").as_posix()
            }
        )
        # Assert that we call super().write()
        mock_super_write.assert_called()
