from os import walk
from _functools import cmp_to_key
from os import listdir
from pathlib import Path
from tqdm import tqdm
from drak_archive.file.dvk import Dvk
from drak_archive.file.dvk_directory import DvkDirectory
from drak_archive.processing.list_processing import clean_list
from drak_archive.processing.list_processing import list_to_string
from drak_archive.processing.string_compare import compare_strings
from drak_archive.processing.string_compare import compare_alphanum


class DvkHandler:
    """
    Handles Dvk objects for given directories and their sub-directories.

    Attributes:
        dvk_directories (list): Loaded Dvk objects
        sorted (list): List of direct indexes to Dvks in a sorted order
    """

    def __init__(self):
        """
        Initializes DvkHandler attributes.
        """
        self.dvks = []
        self.sorted = []
        self.paths = []

    def load_dvks(self, directory_strs: list = None):
        """
        Loads DVK files from a given directory and sub-directories.

        Parameters:
            directory_strs (list): Directories from which to load DVK files
        """
        self.dvks = []
        self.paths = self.get_directories(directory_strs)
        print("Loading DVK Files:")
        for path in tqdm(self.paths):
            dvk_directory = DvkDirectory()
            dvk_directory.read_dvks(path.absolute())
            self.dvks.extend(dvk_directory.dvks)
        self.reset_sorted()

    def reset_sorted(self):
        """
        Resets the sorted list to the default order.
        """
        self.sorted = []
        size = len(self.dvks)
        for i in range(0, size):
            self.sorted.append(i)

    def get_size(self) -> int:
        """
        Returns the number of DVK files loaded / size of sorted list.

        Returns:
            int: Number of DVK files loaded
        """
        return len(self.sorted)

    def get_dvk_sorted(self, index_int: int = -1) -> Dvk:
        """
        Returns the Dvk object for a given index in the sorted index list.

        Parameters:
            index_int (int): Sorted index

        Returns:
            Dvk: Dvk object for the given index
        """
        if index_int > -1 and index_int < self.get_size():
            return self.get_dvk_direct(self.sorted[index_int])
        return Dvk()

    def get_dvk_direct(self, index_int: int = -1) -> Dvk:
        """
        Returns the Dvk object for a given direct index.

        Parameters:
            index_int (int): Direct index

        Returns:
            Dvk: Dvk object for the given index
        """
        if index_int > -1 and index_int < self.get_size():
            return self.dvks[index_int]
        return Dvk()

    def get_directories(self, directory_strs: list = None) -> list:
        """
        Returns a list of directories and sub-directories in a given file path.

        Parameters:
            directory_strs (list): Directories to search within

        Returns:
            list: Internal directories in the form of pathlib Path objects
        """
        if directory_strs is None:
            return []
        paths = []
        for d in directory_strs:
            if d is not None and not d == "":
                directory_path = Path(d)
                for p in walk(directory_path.absolute()):
                    dir = Path(p[0])
                    add = False
                    for file in listdir(dir.absolute()):
                        if str(file).endswith(".dvk"):
                            add = True
                            break
                    if add:
                        paths.append(Path(p[0]))
        return sorted(clean_list(paths))

    def sort_dvks(
            self,
            sort_type: str = None,
            group_artists_bool: bool = False):
        """
        Sorts all currently loaded DVK objects in dvks list.

        Parameters:
            sort_type (str): Sort type
                ("t": Time, "r": Ratings, "v": Views, "a": Alpha-numeric)
            group_artists_bool (bool): Whether to group DVKs of the same artist
        """
        self.group_artists = group_artists_bool
        if sort_type is not None and self.get_size() > 0:
            if sort_type == "t":
                comparator = cmp_to_key(self.compare_time)
            elif sort_type == "r":
                comparator = cmp_to_key(self.compare_ratings)
            elif sort_type == "v":
                comparator = cmp_to_key(self.compare_views)
            else:
                comparator = cmp_to_key(self.compare_alpha)
            self.dvks = sorted(self.dvks, key=comparator)

    def compare_alpha(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects alpha-numerically by their titles.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            result = compare_alphanum(x.get_title(), y.get_title())
        if result == 0:
            return compare_strings(x.get_time(), y.get_time())
        return result

    def compare_time(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects by their publication time.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            result = compare_strings(x.get_time(), y.get_time())
        if result == 0:
            return compare_alphanum(x.get_title(), y.get_title())
        return result

    def compare_ratings(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects by their ratings.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            if x.get_rating() < y.get_rating():
                return -1
            elif x.get_rating() > y.get_rating():
                return 1
            return self.compare_alpha(x, y)
        return result

    def compare_views(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects by their view counts.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            if x.get_views() < y.get_views():
                return -1
            if x.get_views() > y.get_views():
                return 1
            return self.compare_alpha(x, y)
        return result

    def compare_artists(self, x: Dvk = None, y: Dvk = None) -> int:
        x_artists = list_to_string(x.get_artists())
        y_artists = list_to_string(y.get_artists())
        return compare_alphanum(x_artists, y_artists)