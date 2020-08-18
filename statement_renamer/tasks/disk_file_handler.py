""" Provides file-handling operations for files located on an attached drive """
import os
# from .task import Task
# from .action import ActionType
from .file_handler import FileHandler

class DiskFileHandler(FileHandler):
    """ Main class """

    # # Map of handlers for each of the ActionTypes.
    # HANDLERS = {
    #     ActionType.ignore.name: DiskFileHandler._ignore_handler_,
    #     ActionType.rename.name: DiskFileHandler._rename_handler_,
    #     ActionType.delete.name: DiskFileHandler._delete_handler_
    # }

    # # TODO: decouple Task
    # def handle(self, task, action):
    #     DiskFileHandler.HANDLERS[action.action_type.name](task, action)

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

    def __init__(self, config, logger):
        super().__init__(config, logger)

        self.config = config
        self.logger = logger

    @staticmethod
    def _rename_handler_(task, action):
        """ Handles the Rename operation for the provided Action """
        if os.path.isfile(action.target):
            error_text = (
                'Aborting action {} to avoid overwrite of target'.format(action))
            if not task.config.quiet:
                print(error_text)
            task.logger.error(error_text)
            return
        os.rename(action.source, action.target)

    @staticmethod
    def _delete_handler_(task, action):
        os.remove(action.source)

    @staticmethod
    def _ignore_handler_(task, action):
        pass
