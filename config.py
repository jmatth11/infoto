import json
from os import path

class Handler:
    """
    Provides a convenient way to access the different top level config data
    """
    def __init__(self, data):
        """
        Initialize with the config data

        Args:
            data: Config data
        """
        self.__data = data

    def get_metadata(self):
        """
        Get the metadata data from our config

        Returns:
            Dictionary object
        """
        return self.__data["metadata"]
    def get_font(self):
        """
        Get the font data from our config

        Returns:
            Dictionary object
        """
        return self.__data["font"]
    def get_background(self):
        """
        Get the background data from our config

        Returns:
            Dictionary object
        """
        return self.__data["background"]

def create_handler(filename):
    """
    Generates a config.Handler object for the given JSON file.

    Args:
        filename: The file to parse the config data out of
    
    Returns:
        A config.Handler object
    """
    # TODO maybe change to raise an exception instead of exiting program
    if not (path.exists(filename) and path.isfile(filename)):
        print("could not find the given info file")
        exit()
    with open(filename) as f:
        data = json.load(f)
    return Handler(data)