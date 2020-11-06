from unittest import mock
from unittest.mock import patch
from src.generate_new_site.utilities import tables
from pathlib import Path


###############################
# PathTable integration tests #
###############################

def test_pathtable_register_and_gets():
    pathtable = tables.PathTable()
    test_objs = [{
        'entity': "{}".format(i) if i < 5 else None,
        'old_path': Path("{}old".format(i)),
        'new_path': Path("{}old".format(i))
        } for i in range(10)]
    for test_obj in test_objs:
        pathtable.register(
            old_path=test_obj['old_path'],
            new_path=test_obj['new_path'],
            entity=test_obj['entity']
        )
    for test_obj in test_objs:
        assert pathtable.get_entity(test_obj['old_path']) == test_obj['entity']
        assert pathtable.get_path(test_obj['old_path']) == test_obj['new_path']


###############################
# PageTable integration tests #
###############################

def test_pagetable_register_and_gets():
    def mock_page_num_to_arabic(page_num):
        if page_num.isdigit():
            return page_num
        elif page_num == "i":
            return "1"
        elif page_num == "ii":
            return "2"
        elif page_num == "iii":
            return "3"
        elif page_num == "vi":
            return "6"

        return page_num

    pagetable = tables.PageTable()
    page_nums = ["1", "2", "3", "6", "i", "ii", "iii", "vi"]
    test_pages = {num: Path("page{}".format(num)) for num in page_nums}

    with patch('src.generate_new_site.utilities.tables.page_num_to_arabic', mock_page_num_to_arabic):
        for num, path in test_pages.items():
            pagetable.register(
                page_num=num,
                path=path
            )

    # Test get_path_path
    for num, path in test_pages.items():
        assert pagetable.get_page_path(num) == path

    # Test get_prev/next_page_path
    # 1
    assert pagetable.get_prev_page_path("1") is None
    assert pagetable.get_next_page_path("1") == test_pages["2"]
    # 2
    assert pagetable.get_prev_page_path("2") == test_pages["1"]
    assert pagetable.get_next_page_path("2") == test_pages["3"]
    # 3
    assert pagetable.get_prev_page_path("3") == test_pages["2"]
    assert pagetable.get_next_page_path("3") is None
    # 6
    assert pagetable.get_prev_page_path("6") is None
    assert pagetable.get_next_page_path("6") is None
    # i
    assert pagetable.get_prev_page_path("i") is None
    assert pagetable.get_next_page_path("i") == test_pages["ii"]
    # ii
    assert pagetable.get_prev_page_path("ii") == test_pages["i"]
    assert pagetable.get_next_page_path("ii") == test_pages["iii"]
    # iii
    assert pagetable.get_prev_page_path("iii") == test_pages["ii"]
    assert pagetable.get_next_page_path("iii") is None
    # vi
    assert pagetable.get_prev_page_path("vi") is None
    assert pagetable.get_next_page_path("vi") is None
