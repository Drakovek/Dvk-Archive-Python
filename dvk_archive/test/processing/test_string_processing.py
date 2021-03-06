#!/usr/bin/env/ python3

from dvk_archive.main.processing.string_processing import pad_num
from dvk_archive.main.processing.string_processing import remove_whitespace
from dvk_archive.main.processing.string_processing import get_filename
from dvk_archive.main.processing.string_processing import truncate_string
from dvk_archive.main.processing.string_processing import get_extension
from dvk_archive.main.processing.string_processing import get_url_directory

def test_pad_num():
    """
    Tests the pad_num function.
    """
    ## TEST PADDING OUT NUMBER STRINGS WITH ZEROS
    assert pad_num("2F", 2) == "2F"
    assert pad_num("2E", 5) == "0002E"
    ## TEST USING INVALID VALUES
    assert pad_num("10F", 2) == "00"
    assert pad_num("A3", 0) == ""
    assert pad_num("F3", -1) == ""
    assert pad_num(None, 2) == ""

def test_remove_whitespace():
    """
    Tests the remove_whitespace function.
    """
    ## TEST REMOVING WHITESPACE FROM THE BEGINNING AND END OF STRINGS
    assert remove_whitespace("") == ""
    assert remove_whitespace(" ") == ""
    assert remove_whitespace(" \t  ") == ""
    assert remove_whitespace("  blah") == "blah"
    assert remove_whitespace("blah   ") == "blah"
    assert remove_whitespace(" \t blah  \t") == "blah"
    assert remove_whitespace("blah") == "blah"
    ## TEST USING INVALID STRING
    assert remove_whitespace(None) == ""

def test_get_filename():
    """
    Tests the get_filename function
    """
    ## TEST GETTING FILE FRIENDLY NAMES
    assert get_filename("This & That 2") == "This - That 2"
    assert get_filename("! !end filler!??  ") == "end filler"
    assert get_filename("thing--stuff  @*-   bleh") == "thing-stuff - bleh"
    assert get_filename("a% - !b @  ??c") == "a - b - c"
    assert get_filename("Test String", 5) == "Test"
    assert get_filename("Test String", -1) == "Test String"
    ## TEST GETTING FILENAMES WITH NO LENGTH
    assert get_filename("") == "0"
    assert get_filename("$") == "0"
    ## TEST GETTING FILENAME WHEN GIVEN STRING IS INVALID
    assert get_filename(None) == "0"

def test_truncate_string():
    """
    Tests the truncate_string function.
    """
    ## TEST TRUNCATING STRINGS
    assert truncate_string("blah", 0) == ""
    assert truncate_string("bleh", -1) == ""
    assert truncate_string("bleh", 4) == "bleh"
    assert truncate_string("words", 3) == "wor"
    assert truncate_string("word-stuff", 5) == "word"
    assert truncate_string("words n stuff", 4) == "stu"
    assert truncate_string("word stuff", 5) == "word"
    assert truncate_string("words-n-stuff", 4) == "stu"
    in_str = "This string is way too long to work as a title p25"
    out_str = "This string is way too long to work p25";
    assert truncate_string(in_str, 40) == out_str
    in_str = "HereIsA LongThingWithoutManySpacesWhichCanBeShort"
    out_str = "HereIsA WithoutManySpacesWhichCanBeShort"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisMessageIsAbsolutelyWayToLongToWorkFor-"
    in_str = in_str + "AnyThingAtAllSoLetsSeeHowThisWillFareISuppose"
    out_str = "ThisMessageIsAbsolutelyWayToLongToWorkFo"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisMessageIsAbsolutelyWayToLongToWorkForAnyThing-"
    in_str = in_str + "AtAllSoLetsSeeHowThisWillFareISuppose"
    out_str = "Th-AtAllSoLetsSeeHowThisWillFareISuppose"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisLongTitleHasNoSpacesAtAllSoItHasAMiddleBreak"
    out_str = "ThisLongTitleHasAtAllSoItHasAMiddleBreak"
    assert truncate_string(in_str, 40) == out_str
    ## TEST WHEN GIVEN STRING IS INVALID
    assert truncate_string(None, 2) == ""

def test_get_extension():
    """
    Tests the get_extension function.
    """
    ## TEST GETTING EXTENSIONS FROM FILENAMES
    assert get_extension("test.png") == ".png"
    assert get_extension(".long") == ".long"
    assert get_extension("test.thing") == ".thing"
    assert get_extension("blah.test.png") == ".png"
    ## TEST GETTING EXTENTIONS FROM URLS WITH TOKENS
    assert get_extension("test.png?extra.thing") == ".png"
    assert get_extension("thing.test.thing?") == ".thing"
    ## TEST GETTING INVALID EXTENSIONS
    assert get_extension("test.tolong") == ""
    assert get_extension("test.notextension") == ""
    assert get_extension("asdfasdfasdfasdf") == ""
    assert get_extension("test.tolong?extra") == ""
    ## TEST GETTING EXTENSION IF GIVEN STRING IS NULL
    assert get_extension(None) == ""

def test_get_url_directory():
    """
    Tests the get_url_directory function.
    """
    # TEST GETTING LAST DIRECTORY
    assert get_url_directory("a/b/c/url.txt") == "url.txt"
    assert get_url_directory("/url//test") == "test"
    # TEST GETTING DIRECTORY WITH ENDING SLASH
    assert get_url_directory("test/") == "test"
    assert get_url_directory("/other/thing//") == "thing"
    assert get_url_directory("///") == ""
    # TEST GETTING DIRECTORY FROM INVALID URL
    assert get_url_directory("") == ""
    assert get_url_directory(None) == ""

def all_tests():
    """
    Runs all test for the string_processing module.
    """
    test_pad_num()
    test_remove_whitespace()
    test_get_filename()
    test_truncate_string()
    test_get_extension()
    test_get_url_directory()
