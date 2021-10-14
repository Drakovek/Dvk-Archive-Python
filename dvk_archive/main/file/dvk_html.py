#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.color_print import color_print
from dvk_archive.main.processing.html_processing import add_escapes
from dvk_archive.main.processing.html_processing import create_html_tag
from dvk_archive.main.processing.string_processing import get_extension
from dvk_archive.main.processing.string_processing import pad_num
from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.list_processing import list_to_string
from os import mkdir
from os.path import abspath, exists, join
from shutil import rmtree
from tempfile import gettempdir
from typing import List
from webbrowser import open as web_open

def get_temp_directory() -> str:
    """
    Returns a temporary directory for holding HTML files.
    Deletes previous temp directory when called, if applicable.

    :return: Path of the temporary directory
    :rtype: str
    """
    temp_dir = abspath(join(abspath(gettempdir()), "dvk_html"))
    if(exists(temp_dir)):
        rmtree(temp_dir)
    mkdir(temp_dir)
    return temp_dir

def list_to_lines(lst:List[str]=None) -> str:
    """
    Converts a list of strings into a single string with items on separate lines.

    :param lst: List of strings, defaults to None
    :type lst: list[str], optional
    :return: Single string with items on separate lines
    :rtype: str
    """
    # Return empty string if list is None
    if lst is None:
        return ""
    # Convert list to single string
    lines = ""
    for i in range(0, len(lst)):
        # Add new line character if necessary
        if i > 0:
            lines = lines + "\n"
        # Add item to the string
        lines = lines + lst[i]
    return lines

def get_time_string(dvk:Dvk=None, twelve_hour:bool=True) -> str:
    """
    Returns a HTML string showing a Dvk's time published in a readable format.

    :param dvk: Dvk to get time info from, defaults to None
    :type dvk: Dvk, optional
    :param twelve_hour: Whether to use a 12-hour instead of a 24-hour clock, defaults to True
    :type twelve_hour: bool, optional
    :return: HTML string showing the time published
    :rtype: str
    """
    # Check if the time published is invalid
    if dvk is None or dvk.get_time() == "0000/00/00|00:00":
        return "Unknown Publication Date"
    # Get the year
    time = dvk.get_time()
    year = time[0:4]
    # Get the month
    month_int = int(time[5:7])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = months[month_int-1]
    # Get the day
    day = time[8:10]
    # Get the hour
    hour_int = int(time[11:13])
    # Get the minute
    minute = time[14:16]
    # Get the clock string
    clock_string = ":" + minute
    if twelve_hour:
        # Convert 24-hour time to 12-hour clock
        if hour_int < 12:
            clock_string = clock_string + " AM"
            if hour_int == 0:
                hour_int = 12
        else:
            clock_string = clock_string + " PM"
            if not hour_int == 12:
                hour_int -= 12
    clock_string = pad_num(str(hour_int), 2) + clock_string
    # Combine to form full time string
    time_string = "Posted <b>" + day + " " + month + " " + year\
                + " - " + clock_string + "</b>"
    # Return the time string
    return time_string

def is_image_extension(extension:str=None) -> bool:
    """
    Returns whether a given file extension is for an image file.

    :param extension: Given file extension, defaults to None
    :type extension: str, optional
    :return: Whether file extension is for an image file.
    :rtype: bool
    """
    if (extension == ".jpg"
            or extension == ".jpeg"
            or extension == ".png"
            or extension == ".gif"
            or extension == ".svg"
            or extension == ".webp"
            or extension == ".apng"
            or extension == ".avif"
            or extension == ".jfif"
            or extension == ".pjpeg"
            or extension == ".pjp"):
        return True
    return False

def get_media_html(dvk:Dvk=None) -> str:
    """
    Returns an HTML tag that contains the media file(s) for a given Dvk.

    :param dvk: Dvk to get media file(s) from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML tag that displays the media file for a given Dvk
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if dvk is None or dvk.get_title() is None or dvk.get_media_file() is None:
        return ""
    media_tag = ""
    media_file = "file://" + str(dvk.get_media_file())
    extension = get_extension(media_file)
    # Check if media file is an image
    if is_image_extension(extension):
        # Create HTML img tag
        attr = [["id", "dvk_image"],
                    ["src", media_file],
                    ["alt", add_escapes(dvk.get_title())]]
        media_tag = create_html_tag("img", attr)
    # Returns the media tag
    return media_tag

def get_dvk_header_html(dvk:Dvk=None) -> str:
    """
    Returns dvk_header HTML tag for a given Dvk.
    Contains Dvk's title, artist(s), and publication time.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :return: Header tag for the given Dvk
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if dvk is None or dvk.get_title() is None or dvk.get_artists() == []:
        return ""
    # Create title tag
    title_tag = "<b>" + add_escapes(dvk.get_title()) + "</b>"
    title_tag = create_html_tag("div", [["id","dvk_title"]], title_tag, False)
    # Create published tag
    pub_tag = "By <b>" + list_to_string(dvk.get_artists(), True, 1)\
                + "</b>, " + get_time_string(dvk)
    pub_tag = create_html_tag("div", [["id", "dvk_pub"]], pub_tag, False)
    # Combine into header tag
    attr = [["id", "dvk_header"], ["class", "dvk_padded"]]
    header = create_html_tag("div", attr, title_tag + "\n" + pub_tag)
    # Return dvk_header tag
    return header

def get_dvk_info_html(dvk:Dvk=None) -> str:
    """
    Returns HTML containing the main Dvk info.
    Includes the title, artist(s), time published, and description.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML containing main Dvk info.
    :rtype: str
    """
    # Create the dvk_header tag
    header_tag = get_dvk_header_html(dvk)
    # Return empty string if header is empty
    if header_tag == "":
        return ""
    # Create div to hold the description
    desc_tag = ""
    attr = [["id", "dvk_description"], ["class", "dvk_padded"]]
    description = dvk.get_description()
    if description is None:
        desc_tag = create_html_tag("div", attr, "<i>No Description</i>")
    else:
        desc_tag = create_html_tag("div", attr, description)
    # Combine into larger dvk_info_base tag
    attr = [["id", "dvk_info_base"], ["class", "dvk_info"]]
    info = create_html_tag("div", attr, header_tag + "\n" + desc_tag)
    # Return the dvk_info_base tag
    return info

def get_tag_info_html(dvk:Dvk=None) -> str:
    """
    Returns an HTML block containing the web_tags for a given Dvk.

    :param dvk: Dvk to get web_tags from.
    :type dvk: Dvk, optional
    :return: HTML block containing web_tags
    :rtype: str
    """
    # Return empty string if there are no tags
    if dvk is None or dvk.get_web_tags() == []:
        return ""
    # Create web_tag_header
    attr = [["id", "dvk_web_tag_header"], ["class", "dvk_padded"]]
    wt_header = create_html_tag("b", None, "Web Tags", False)
    wt_header = create_html_tag("div", attr, wt_header, False)
    # Create web_tag_elements
    wt_elements = []
    attr = [["class", "dvk_tag"]]
    web_tags = dvk.get_web_tags()
    for tag in web_tags:
        element = create_html_tag("span", attr, add_escapes(tag), False)
        wt_elements.append(element)
    # Create web_tag_container
    attr = [["id", "dvk_tags"], ["class", "dvk_padded"]]
    wt_container = create_html_tag("div", attr, list_to_lines(wt_elements))
    # Create tag info container
    attr = [["id", "dvk_tag_info"], ["class", "dvk_info"]]
    ti = create_html_tag("div", attr, wt_header + "\n" + wt_container)
    return ti

def get_page_link_html(dvk:Dvk=None) -> str:
    """
    Returns an HTML tag including links to all the URLs contained in the Dvk.
    Contains the Page URL as well as direct media and and secondary media URLs.

    :param dvk: Dvk to get URLs from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML tag containing links to the Dvk's media
    :rtype: str
    """
    links = []
    cls = ["class", "dvk_link"]
    # Return empty string if Dvk is invalid
    if dvk is None:
        return ""
    # Get page URL link
    page = dvk.get_page_url()
    if page is not None:
        link = create_html_tag("a", [cls, ["href", page]], "Page URL", False)
        links.append(link)
    # Get direct URL link
    direct = dvk.get_direct_url()
    if direct is not None:
        link = create_html_tag("a", [cls, ["href", direct]], "Direct URL", False)
        links.append(link)
    # Get secondary URL link
    secondary = dvk.get_secondary_url()
    if secondary is not None:
        link = create_html_tag("a", [cls, ["href", secondary]], "Secondary URL", False)
        links.append(link)
    # Set the appropriate attributes for the number of links used
    if len(links) == 3:
        attr = [["id", "dvk_page_links"], ["class", "dvk_three_grid"]]
    elif len(links) == 2:
        attr = [["id", "dvk_page_links"], ["class", "dvk_two_grid"]]
    elif len(links) == 1:
        attr = [["id", "dvk_page_links"], ["class", "dvk_one_grid"]]
    else:
        # Return empty string if no links are present
        return ""
    # Combine links into an HTML tag
    return create_html_tag("div", attr, list_to_lines(links))

def get_dvk_html(dvk:Dvk=None) -> str:
    """
    Returns HTML page with all the info for a given Dvk file.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML containing Dvk info
    :rtype: str
    """
    # Return empty string if dvk is invalid
    if dvk is None or dvk.get_title() is None:
        return ""
    # Create HTML head
    title = create_html_tag("title", None, add_escapes(dvk.get_title()), False)
    charset = create_html_tag("meta", [["charset", "UTF-8"]])
    head = create_html_tag("head", None, list_to_lines([title, charset]))
    # Create HTML media tag
    media = get_media_html(dvk)
    # Create dvk_info_tag
    dvk_info = get_dvk_info_html(dvk)
    # Create tag info HTML tag
    tag_info = get_tag_info_html(dvk)
    # Create page link tag
    page_links = get_page_link_html(dvk)
    # Combine into dvk_content tag
    content = list_to_lines(clean_list([media, dvk_info, tag_info, page_links]))
    dvk_content = create_html_tag("div", [["id", "dvk_content"]], content)
    # Combine into final HTML
    html = head + "\n" + create_html_tag("body", None, dvk_content)
    html = "<!DOCTYPE html>\n" + create_html_tag("html", None, html)
    # Return HTML
    return html

def write_dvk_html(dvk:Dvk=None) -> str:
    """
    Creates an HTML file from Dvk info.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :return: Path of the written HTML file
    :rtype: str
    """
    # Get the filename for the dvk
    temp_dir = get_temp_directory()
    html_file = abspath(join(temp_dir, "dvk.html"))
    # Get HTML for the given Dvk
    html = get_dvk_html(dvk)
    if html == "":
        return ""
    # Write html to disk
    with open(html_file, "w") as out_file:
        out_file.write(html)
    if not exists(html_file):
        return ""
    # Return the path to the html file
    return html_file

def main():
    """
    Sets up parser for creating and opening HTML files from DVK.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "dvk",
        help="DVK file to open as an HTML file.",
        type=str)
    args = parser.parse_args()
    dvk = Dvk(abspath(args.dvk))
    if dvk is not None:
        html = write_dvk_html(dvk)
        if not html == "":
            print(html)
            web_open("file://" + abspath(html))
        else:
            color_print("Failed writing HTML", "r")
    else:
        color_print("Invalid Dvk", "r")

if __name__ == "__main__":
    main()