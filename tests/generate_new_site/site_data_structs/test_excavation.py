from unittest import mock
from unittest.mock import patch
from src.generate_new_site.site_data_structs import excavation
from pathlib import Path


###################################
# Test add_child() and set_path() #
###################################

@patch('src.generate_new_site.site_data_structs.excavation.ExcavationChapter.set_path')
def test_excavation_chapter_add_child(mock_set_path):
    chapter = excavation.ExcavationChapter(name="Test Chapter", parent=None, path=None)

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


@patch('src.generate_new_site.site_data_structs.excavation.ExcavationModule.set_path')
def test_excavation_module_add_child(mock_set_path):
    module = excavation.ExcavationModule(
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


@patch('src.generate_new_site.site_data_structs.excavation.rel_path', return_value=Path("relpath"))
@patch('jinja2.Template.render')
@patch('src.generate_new_site.site_data_structs.excavation.update_text_paragraph', return_value="touched")
@patch('src.generate_new_site.site_data_structs.site.SitePage.write')
def test_excavation_page_write(mock_super_write, mock_update_content, mock_render, mock_rel_path):
    # Set up mock objects
    next = Path("next")
    prev = Path("prev")

    children = "arbitary"
    ch_name = "Excavations"
    mo_long_name = "module"

    module = mock.Mock(long_name=mo_long_name)
    module.parent = mock.Mock()
    module.parent.name = ch_name
    module.parent.parent = mock.Mock(children=children)
    module.parent.parent.pagetable.get_next_page_path = mock.Mock(return_value=next)
    module.parent.parent.pagetable.get_prev_page_path = mock.Mock(return_value=prev)

    # Instantiate page
    content = {
        'content': {
            'content':[
                {'content': "content 1"},
                {'content': "content 2"}
            ]
        }
    }
    path = Path("page.html")
    page = excavation.ExcavationPage(
        name="page",
        path=path,
        content=content,
        parent=module,
        mini_map_orig_path=Path('origpath'),
        info=None,
        page_num="5"
    )


    with patch('src.generate_new_site.site_data_structs.excavation.Path.open', mock.mock_open()):
        page.write()

    # Assert that content is updated
    for content_obj in content['content']['content']:
        assert content_obj['content'] == "touched"

    # Assert next and prev paths are made relative
    mock_rel_path.assert_any_call(next, path)
    mock_rel_path.assert_any_call(prev, path)

    # Assert that correct kwargs are passed to render
    mock_render.assert_called_once_with(
        excavation_element=page,
        chapters=children,
        this_chapter_name=ch_name,
        this_module_name=mo_long_name,
        this_section_name=page.name,
        pagination={
            'prev_page_href': Path("relpath"),  # TODO as_posix()?
            'this_page_num': page.page_num,
            'next_page_href': Path("relpath")  # TODO as_posix()?
        }
    )

    # Assert that we call super().write()
    mock_super_write.assert_called()


######################
# Test update_href() #
######################

@patch('src.generate_new_site.site_data_structs.excavation.rel_path', return_value=Path("updated"))
def test_excavation_page_update_href(mock_rel_path):
    # Mock parent
    module = mock.Mock()
    module.parent.parent.pathtable.get_path = mock.Mock(return_value=Path('tablepath'))

    # Instantiate page
    content = {
        'content': {
            'content':[
                {'content': "content 1"},
                {'content': "content 2"}
            ]
        }
    }
    path = Path("page.html")
    page = excavation.ExcavationPage(
        name="page",
        path=path,
        content=content,
        parent=module,
        mini_map_orig_path=Path('origpath'),
        info=None,
        page_num="5"
    )
    # Don't use add_figure or add_related_element
    figures = [mock.Mock() for i in range(4)]
    page.figures = figures
    related_elements = [excavation.RelatedElement(str(i), Path("re{}".format(i)), page) for i in range(4)]
    page.related_elements = related_elements

    page.update_href(Path("test"))

    assert page.href == Path("updated").as_posix()
    for figure in figures:
        figure.update_href.assert_called_once_with(Path("test"))
    for re in related_elements:
        assert re.href == Path("updated").as_posix()
