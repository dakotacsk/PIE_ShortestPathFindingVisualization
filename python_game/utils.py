import os
import sys

def resource_path(relative_path):
    """
    Get absolute path to resource, compatible with PyInstaller
    """
    try:
        # PyInstaller extracts to _MEIPASS in a temp directory
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
