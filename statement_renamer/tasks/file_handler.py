""" Base class for file operations """
from abc import ABC, abstractmethod
from .action import ActionType

class FileHandler(ABC):
    """ Main class """

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    # TODO: decouple Task
    def handle(self, task, action):
        """ Handles the specified Action according to action type """
        if action.action_type == ActionType.ignore:
            self._ignore_handler_(task, action)
        elif action.action_type == ActionType.rename:
            self._rename_handler_(task, action)
        elif action.action_type == ActionType.delete:
            self._delete_handler_(task, action)

    @abstractmethod
    def walkdir(self, folder):
        """ Walk through files in the specified container """

    @abstractmethod
    def is_file(self, location):
        """ Return true if location is a single file """

    @abstractmethod
    def is_folder(self, location):
        """ Return true if location holds files """

    @abstractmethod
    def file_exists(self, location):
        """ Return true if a file exists at location """

    @staticmethod
    @abstractmethod
    def _rename_handler_(task, action):
        """ Handles the Rename operation for the provided Action """

    @staticmethod
    @abstractmethod
    def _delete_handler_(task, action):
        """ Handles the Delete operation for the provided Action """

    @staticmethod
    @abstractmethod
    def _ignore_handler_(task, action):
        """ Handles the Ignore operation for the provided Action """
