# DVK Archive (Python)

Utility for loading and handling media files in the DVK file format.

- [Installation](#installation)
- [Scripts](#scripts)
- [DVK File Format](#dvk-file-format)

# Installation

DVK Archive can be installed from its [PyPI package](https://pypi.org/project/dvk-archive/) using pip:

    pip install dvk-archive

If you are installing from source, the following python packages are required:
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
* [lxml](https://pypi.org/project/lxml/)
* [requests](https://pypi.org/project/requests/)
* [selenium](https://pypi.org/project/selenium/)
* [tqdm](https://pypi.org/project/tqdm/)

# Scripts

All scripts contain a [directory] field, which tells the script which directory to search.
If left empty, [directory] defaults to the current working directoy.
Scripts search both [directory] and its subdirectories.

- [dvk-same-ids](#dvk-same-ids)
- [dvk-unlinked](#dvk-unlinked)
- [dvk-missing-media](#dvk-missing-media)
- [dvk-rename](#dvk-rename)

## Finding Errors

Scripts for finding errors in DVK files and their referenced media.

### dvk-same-ids

    dvk-same-ids [directory]

Checks for DVK files in [directory] that share the same ID.
Prints file paths if any are found.

### dvk-unlinked

    dvk-unlinked [directory]

Checks for any files in [directory] that are not linked to a DVK file.
Ignores folders that contain no DVKs.
Prints file paths if any are found.

### dvk-missing-media

    dvk-missing-media [directory]

Checks for any DVK files in [directory] which reference media files or secondary media files that do not exist.
Prints file paths if any are found.

## Reformatting

Scripts for editing DVK files and their referenced media.

### dvk-rename

    dvk_rename [directory]

Renames all DVKs and their referenced media in [directory] to fit the standard naming convention: TITLE_ID

# DVK File Format

DVK files are simply repackaged JSON files that contain useful metadata fields for media files downloaded from the internet.
DVK files contain only metadata, and point to separate media files (images, video, audio, etc.).

Below are the standard DVK metadata fields, shown with their corresponding JSON keys.

### id

(str)
A unique ID for other DVK files to reference.

### title

(String)
The title for the referenced media.

### artists

(list[str])
A list of artists/authors who created the referenced media.

### time

(str)
A string showing the time and date in which the referenced media was published/uploaded.

Formatted YYYY/MM/DD|hh:mm

Example: 6 October, 2017 @ 5:00PM -> 2017/10/06|17:00

### web_tags

(list[str])
A list of tags gathered from the referenced media's original web source.

### description

(str)
A media description gathered from the referenced media's original web source.

### page_url

(str)
The URL of the web page from which the referenced media was sourced.

### direct_url

(str)
The direct media URL from which the referenced media was downloaded.
Not to be confused with the page_url, which is the URL for the page containing both the referenced media and accessory info.

### secondary_url

(str)
The direct media URL from which the secondary media file was downloaded.
This field is only used if the DVK references a secondary media file. (See [secondary file](#secondary_file))

### media_file

(str)
File path of the referenced media file.
Path is relative to the directory of the DVK file.

### secondary_file

(str)
File path of a secondary media file that supplements the main media file.
For example, a DVK that references a text file might have a secondary file for the cover illustration.
Path is relative to the directory of the DVK file.
Not used if there is no secondary media file.

### favorites

(list[str])
A list of artists who favorited the media on the site it originated from.
Used to indicate that the media was downloaded from a favorites gallery and not from the artist themselves.

### is_single
(bool)
Whether the file was downloaded on its own rather than as part of a larger gallery.
