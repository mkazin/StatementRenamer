""" Provides file-handling operations for files located on an attached drive """
import os
from pathlib import Path
# from .task import Task
# from .action import ActionType
from .file_handler import FileHandler

class DiskFileHandler(FileHandler):
    """ Main class """

    # TODO: decouple Task

    def walkdir(self, folder):
        """Walk through each files in a directory"""
        for dirpath, _, files in os.walk(folder):
            for filename in files:
                yield os.path.abspath(os.path.join(dirpath, filename))

    def is_file(self, location):
        return os.path.isfile(location)

    def is_folder(self, location):
        return os.path.isdir(location)

    def file_exists(self, location):
        return os.path.isfile(location)

    def basename(self, location):
        return os.path.basename(location)

    def pathname(self, location):
        return Path(location).parent if self.is_file(location) else location

    def build_path(self, path, filename):
        return Path(path) / filename

    def __init__(self, config, logger):
        super().__init__(config, logger)

        self.config = config
        self.logger = logger

    def _rename_handler_(self, task, action):
        """ Handles the Rename operation for the provided Action """
        if os.path.isfile(action.target):
            error_text = (
                'Aborting action {} to avoid overwrite of target'.format(action))
            if not task.config.quiet:
                print(error_text)
            task.logger.error(error_text)
            return
        os.rename(action.source, action.target)

    def _delete_handler_(self, task, action):
        os.remove(action.source)

    def _ignore_handler_(self, task, action):
        pass
