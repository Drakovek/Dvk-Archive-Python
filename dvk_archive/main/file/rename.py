#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.color_print import color_print
from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from os import getcwd, pardir
from os.path import abspath, exists, isdir, join
from tqdm import tqdm

def rename_files(dvk_handler:DvkHandler=None):
    """
    Renames DVKs and associated media to their default names.

    :param dvk_handler: Contains DVKs to be renamed, defaults to None
    :type dvk_handler: DvkHandler, optional
    """
    # TEST IF DVK HANDLER IS VALID
    if dvk_handler is not None:
        print("Renaming files:")
        size = dvk_handler.get_size()
        for dvk_num in tqdm(range(0, size)):
            dvk = dvk_handler.get_dvk(dvk_num)
            # Get parent directory
            parent = abspath(join(abspath(dvk.get_dvk_file()), pardir))
            # RENAME DVK FILE AND ASSOCIATED MEDIA
            dvk.rename_files(dvk.get_filename(parent, False), dvk.get_filename(parent, True))
            # UPDATE EXTENSIONS
            dvk.update_extensions()

def rename_directory(directory:str=None):
    """
    Reformats files in a given directory.

    :param directory: Directory in which to rename files, defaults to None
    :type directory: str, optional
    """
    # CHECK IF DIRECTORY EXISTS
    if directory is not None and exists(directory) and isdir(directory):
        # READ DVKS IN THE GIVEN DIRECTORY
        dvk_handler = DvkHandler()
        dvk_handler.read_dvks(directory)
        # REFORMAT DVKS
        rename_files(dvk_handler)
    else:
        color_print("Invalid directory", "r")

def main():
    """
    Sets up renaming DVK and media files.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "directory",
        help="Directory in which to rename files.",
        nargs="?",
        type=str,
        default=str(getcwd()))
    args = parser.parse_args()
    rename_directory(abspath(args.directory))

if __name__ == "__main__":
    main()
