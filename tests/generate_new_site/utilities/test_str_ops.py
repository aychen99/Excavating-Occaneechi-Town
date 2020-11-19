from src.generate_new_site.utilities import str_ops
import pytest

################################
# page_num_to_arabic unit test #
################################


@pytest.mark.parametrize("roman,arabic", [
    ("i", "1"),
    ("iii", "3"),
    ("iv", "4"),
    ("v", "5"),
    ("vi", "6"),
    ("ix", "9"),
    ("x", "10"),
    ("xii", "12"),
    ("xiv", "14"),
    ("xix", "19"),
    ("xxv", "25"),
    ("xxvii", "27")
])
def test_page_num_to_arabic(roman, arabic):
    assert str_ops.page_num_to_arabic(roman) == arabic


####################################
# make_str_filename_safe unit test #
####################################


@pytest.mark.parametrize("str_in,str_out", [
    ("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz"),
    ("abc\\bcd", "abcbcd"),
    ("test test", "test_test"),
    ("test      test", "test______test"),
    ("test(test)test", "testtesttest"),
    ("test (test) test", "test_test_test"),
    ("bad/file/name", "badfilename"),
    ("test.test", "testtest"),
    ("test.()../\\.\\/()test", "testtest")
])
def test_make_str_filename_safe(str_in, str_out):
    assert str_ops.make_str_filename_safe(str_in) == str_out
