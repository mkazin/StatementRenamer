""" Provides mock file-handling operations for unit tests """
import os
from pathlib import Path

import static as static

import statement_renamer.config
# from .task import Task
# from .action import ActionType
from statement_renamer.tasks.file_handler import FileHandler
import logging


class MockFileHandler(FileHandler):
    """ Main class """
    def __init__(self):
        super().__init__()
        self.existing_files = []

    def set_existing_files(self, existing_files):
        self.existing_files = existing_files

    def walkdir(self, folder):
        """Walking is not mocked"""
        raise NotImplemented

    def is_file(self, location):
        return True

    def is_folder(self, location):
        return False

    # You'll want to override the behavior of this one for delete/rename
    def file_exists(self, location):
        return location in self.existing_files

    def basename(self, location):
        return os.path.basename(location)

    def pathname(self, location):
        return Path(location).parent if self.is_file(location) else location

    def build_path(self, path, filename):
        return Path(path) / filename

    def _rename_handler_(self, action):
        self.before_name = action.source
        self.target_name = action.target
        self.file_exists = __file_not_found__

    def _delete_handler_(self, action):
        os.remove(action.source)
        self.file_exists = __file_not_found__

    def _ignore_handler_(self, action):
        pass

    def __file_not_found__(self, location):
        return False

    def __file_found__(self, location):
        return True


