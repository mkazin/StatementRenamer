""" Defines actions which can be taken on an input file
"""
import enum

import os


@enum.unique
class ActionType(enum.Enum):
    """ Enum definition of action types with assigned identifiers """
    delete = 3
    ignore = 2
    rename = 1


class Action():
    """ Defines the action which should be taken on a file """

    def __init__(self, action_type, source, target=None, reason=None):
        """ Do not use. Call a create_XYZ_action() builder instead.
        """
        self.action_type = action_type
        self.source = source
        self.target = target
        self.reason = reason

    def __repr__(self):
        response = '{} {}'.format(
            self.action_type.name.capitalize(),
            os.path.basename(self.source))
        if self.action_type == ActionType.rename:
            response += ' to {}'.format(
                os.path.basename(self.target))
        if self.reason:
            response += ' ({})'.format(self.reason)
        return response

    @staticmethod
    def create_delete_action(filepath, reason=None):
        """ Creates an Action for deleting a file """
        return Action(ActionType.delete, filepath, reason=reason)

    @staticmethod
    def create_rename_action(source_filepath, target_filepath):
        """ Creates an Action for renaming a file """
        return Action(ActionType.rename, source_filepath, target_filepath)

    @staticmethod
    def create_ignore_action(filepath, reason):
        """ Creates an Action for ignoring a file """
        return Action(ActionType.ignore, filepath, target=None, reason=reason)
