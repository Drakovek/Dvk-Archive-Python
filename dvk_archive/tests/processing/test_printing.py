from os.path import abspath, expanduser, join
from dvk_archive.processing.printing import truncate_path


def test_truncate_path():
    """
    Tests the truncate_path function
    """
    assert truncate_path() == ""
    base_path = abspath(join(expanduser("~"), "printingTest"))
    sub = join(base_path, "sub")
    other = join(base_path, "kjskjld")
    assert truncate_path(sub) == str(sub)
    assert truncate_path(sub, other) == str(sub)
    assert truncate_path(sub, base_path) == ".../sub"


def run_all():
    """
    Tests all functions of the printing.py module
    """
    test_truncate_path()
