from unittest import mock
from unittest.mock import patch
from src.generate_new_site.site_data_structs import site
from pathlib import Path


################
# Test write() #
################


@patch('jinja2.Template.render')
@patch('src.generate_new_site.site_data_structs.site.Index.update_href')
def test_index_write(mock_index_href, mock_render):
    index = site.Index(Path("index.html"))
    for i in range(4):
        index.children.append(mock.Mock())

    with patch("pathlib.Path.open", mock.mock_open()):
        index.write()

    # Ensure call to self.update_href
    mock_index_href.assert_called_with(index.path)

    # Ensure correct args passed to template.render
    mock_render.assert_called_with(children=index.children)

    # Ensure calls to child.write() for child in self.children
    for mock_module in index.children:
        mock_module.write.assert_called_once()


def test_chapter_write():
    index = mock.Mock()
    chapter = site.SiteChapter(name="chapter", parent=index)

    # Mock modules
    for i in range(4):
        chapter.children.append(mock.Mock())

    chapter.write()

    # Ensure call to self.parent.update_href
    assert index.update_href.call_count == len(chapter.children)

    for mocked_module in chapter.children:
        # Ensure calls to child.write() for child in self.children
        mocked_module.write.assert_called_once()
        mocked_module.path.parent.mkdir.assert_called_once()


@patch('src.generate_new_site.site_data_structs.site.SitePage.write')
def test_module_write(mock_child_write):
    index = mock.Mock()
    chapter = mock.Mock(parent=index)

    module = site.SiteModule(
        short_name="mod",
        long_name="module",
        parent=chapter,
        author=None,
        path=Path("module.html")
    )
    for i in range(4):
        module.children.append(mock.Mock())

    module.write()
    # Ensure calls to child.write() for child in self.children
    for mocked_page in module.children:
        mocked_page.write.assert_called_once()


# Mock it with itself just so we can get a count
def test_page_write():
    page = site.SitePage(name="page", path=Path("page.html"), content=None, parent=None, page_num=None)
    for i in range(4):
        page.add_child(mock.Mock())
    page.write()
    # Ensure calls to child.write() for child in self.children
    for mocked_child in page.children:
        mocked_child.write.assert_called_once()


######################
# Test update_href() #
######################

# Integration test for all update_href methods in site.py
@patch('src.generate_new_site.site_data_structs.site.rel_path', return_value=Path("updated"))
def test_update_href(mock_rel_path):
    index = site.Index(Path("index.html"))
    chapters = [
        site.SiteChapter(
            name="c{}".format(i),
            parent=index,
            path=Path("c{}.html".format(i))
        ) for i in range(2)]
    for chapter in chapters:
        # Don't rely on add_child
        index.children.append(chapter)
        modules = [
            site.SiteModule(
                short_name="{}m{}".format(chapter.name, i),
                parent=chapter,
                long_name=None,
                author=None,
                path=Path("{}m{}.html".format(chapter.name, i))
            ) for i in range(2)]
        for module in modules:
            chapter.children.append(module)
            pages = [
                site.SitePage(
                    name="{}p{}".format(module.short_name, i),
                    path=Path("{}p{}.html".format(module.short_name, i)),
                    content=None,
                    parent=module,
                    page_num=None
                ) for i in range(2)]
            for page in pages:
                module.children.append(page)
                sub_pages = [
                    site.SitePage(
                        name="{}p{}".format(page.name, i),
                        path=Path("{}p{}.html".format(page.name, i)),
                        content=None,
                        parent=module,
                        page_num=None
                    ) for i in range(2)]
                for sub_page in sub_pages:
                    page.children.append(sub_page)

    index.update_href(Path("test"))

    # Ensure that all hrefs in the tree are updated
    assert index.href == Path("updated").as_posix()
    for chapter in index.children:
        assert chapter.href == Path("updated").as_posix()
        for module in chapter.children:
            assert module.href == Path("updated").as_posix()
            for page in module.children:
                assert page.href == Path("updated").as_posix()
                for sub_page in page.children:
                    assert sub_page.href == Path("updated").as_posix()
