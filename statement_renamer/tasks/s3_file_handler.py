""" Provides file-handling operations for files located in S3 """
from .file_handler import FileHandler

class S3FileHandler(FileHandler):
    """ Main class """


""" Provides file-handling operations for files located on an attached drive """
import os
from pathlib import Path
# from .action import ActionType
from .file_handler import FileHandler

class DiskFileHandler(FileHandler):
    """ Main class """

    def walkdir(self, folder):
        NotImplementedError

    def is_file(self, location):
        NotImplementedError

    def is_folder(self, location):
        NotImplementedError

    def file_exists(self, location):
        NotImplementedError

    def basename(self, location):
        NotImplementedError

    def pathname(self, location):
        NotImplementedError

    def build_path(self, path, filename):
        NotImplementedError


    def __init__(self):
        super().__init__()

    def _rename_handler_(self, action):
        """ Handles the Rename operation for the provided Action """
        NotImplementedError

    def _delete_handler_(self, action):
        NotImplementedError

    def _ignore_handler_(self, action):
        pass
