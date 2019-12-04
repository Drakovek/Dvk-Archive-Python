from os import getcwd
from tqdm import tqdm
from pathlib import Path
from argparse import ArgumentParser
from dvk_archive.file.dvk_handler import DvkHandler
from dvk_archive.processing.printing import print_paths


def same_ids(
        dvk_directories: list = None,
        dvk_handler: DvkHandler = None) -> list:
    """
    Checks for Dvk objects with identical IDs.
    Parameters:
        dvk_directory (str): Directory from which to search for DVK files.
            Used if dvk_handler is None
        dvk_handler (list): DvkHandler with loaded DVK files.
    Returns:
        list: List of Paths for DVK files with identical IDs
    """
    if dvk_handler is not None:
        handler = dvk_handler
    else:
        handler = DvkHandler()
        handler.load_dvks(dvk_directories)
    handler.sort_dvks("a", True)
    # CREATE LIST OF IDS
    print("Searching for DVK files with identical IDs:")
    ids = []
    size = handler.get_size()
    for i in range(0, size):
        ids.append(handler.get_dvk_sorted(i).get_id())
    # FIND IDENTICAL IDS
    s_ids = []
    for i in tqdm(range(0, size)):
        if i not in s_ids:
            for k in range(i + 1, size):
                if ids[i] == ids[k]:
                    if i not in s_ids:
                        s_ids.append(i)
                    s_ids.append(k)
    # CREATE PATH LIST
    identicals = []
    for id in s_ids:
        identicals.append(handler.get_dvk_sorted(int(id)).get_file())
    return identicals


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "directory",
        help="Directory in which to preform operations.",
        nargs="?",
        type=str,
        default=str(getcwd()))
    args = parser.parse_args()
    dir = Path(args.directory)
    print_paths(same_ids([dir.absolute()]), dir)


if __name__ == "__main__":
    main()
