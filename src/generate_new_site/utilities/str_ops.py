def make_str_filename_safe(s):
    translation_table = {
        ord(' '): ord('_'),
        ord('('): None,
        ord(')'): None,
        ord('/'): None,
        ord('\\'): None,
        ord('.'): None
    }

    return s.lower().translate(translation_table)


def normalize_file_page_num(page_num):
    """
    Correctly formats page numbers for file names.
    Format is 'XXX' for body matter and 'prelimsXX' for front matter.
    """

    if page_num.isdigit():  # Not roman numerals, so in main section
        return '{:0>3}'.format(page_num)  # We want 3 digits with leading 0s
    else:  # Dealing with preliminaries, different formatting required
        page_num = page_num_to_arabic(page_num)
        return '{}_{:0>2}'.format("prelims", page_num)


def page_num_to_arabic(page_num):
    """
    Ensures that a page number is in arabic.
    Front matter pagination goes up to 'xxxiii', so don't worry about handling
    'L' and up.
    Parameters
    ----------
    page_num : str
        Page number
    Returns
    -------
    num_arabic :str
        Page number in arabic
    """

    if page_num.isdigit():  # Don't do anything if number is already arabic
        return page_num

    rn = {'i': 1, 'v': 5, 'x': 10}
    num_arabic = 0
    count = 0
    while count < len(page_num):
        if count + 1 == len(page_num):  # Last char in StopIteration
            num_arabic += rn[page_num[count]]
            count += 1
        elif rn[page_num[count]] < rn[page_num[count+1]]:  # Subtract (iv, ix)
            num_arabic += rn[page_num[count+1]] - rn[page_num[count]]
            count += 2
        else:
            num_arabic += rn[page_num[count]]
            count += 1
    return str(num_arabic)
