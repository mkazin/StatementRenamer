""" Provides file-handling operations for files located on an attached drive """
import os
from pathlib import Path
import statement_renamer.config
# from .task import Task
# from .action import ActionType
from .file_handler import FileHandler
import logging

class DiskFileHandler(FileHandler):
    """ Main class """

    def walkdir(self, folder):
        """Walk through each files in a directory"""
        for dirpath, _, files in os.walk(folder):
            for filename in files:
                yield os.path.abspath(os.path.join(dirpath, filename))

    def is_file(self, location):
        log = logging.getLogger('StatementRenamer')
        # log = logging.getLogger(__name__)
        log.debug('abspath: {%s}', os.path.abspath(location))
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

    def _rename_handler_(self, action):
        """ Handles the Rename operation for the provided Action """
        if os.path.isfile(action.target):
            error_text = (
                'Aborting action {} to avoid overwrite of target'.format(action))
            if not statement_renamer.config.QUIET:
                print(error_text)
            self.logger.error(error_text)
            return
        os.rename(action.source, action.target)

    def _delete_handler_(self, action):
        os.remove(action.source)

    def _ignore_handler_(self, action):
        pass
