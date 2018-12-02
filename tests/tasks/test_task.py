import mock
import argparse
import unittest
from statement_renamer.tasks.action import Action, ActionType
from statement_renamer.tasks.task import Task

def empty_function():
    pass

class TestTask(unittest.TestCase):

    FILEPATH_A = '/mypath/filename_a'
    HASH_A = '0123456789ABCDEF'
    def md5parser_parse_single_file(filepath):
        return {FILEPATH_A: HASH_A}[filepath]
    # def md5parser_parse_duplicate_file(filepath):
    #     return {FILEPATH_A: HASH_A, FILEPATH_B: HASH_B, FILEPATH_C: HASH_C}[filepath]

    # @mock.patch('statement_renamer.readers.md5_reader.Md5Reader')
    # @mock.patch('argparse.ArgumentParser')
    # def test_determine_action_for_file_when_file_already_named_properly(self, mock_parser, mock_md5reader):
    #     """ Tests one files which has already been named
    #         Expectation: The file is to be ignored.
    #     """

    #     mock_parser.parse_args = empty_function
    #     task = Task(mock_parser, logger=None)

    #     # self.args = parser.parse_args()
    #     # # TODO: inject these
    #     # self.reader = PdfReader()
    #     # self.date_formatter = DateFormatter()
    #     # self.logger = logger
    #     # self.actions = []
    #     # self.hashes = []
    #     # self.action_totals = {}

    #     mock_md5reader.parse = TestTask.md5parser_parse_single_file
    #     actual = task.determine_action_for_file(TestTask.FILEPATH_A)

    #     assert actual.action_type == ActionType.ignore
    #     assert actual.reason == 'Already named correctly'
    #     assert actual.filepath == FILEPATH_A
    #     assert actual.source == '???'
    #     assert actual.target == '???'



    def test_determine_action_for_file_when_other_file_already_named_properly(self):
        """ Tests two files with identical hashes, one having already been named
            Expectation: The already-named file is to be ignored. The other deleted.
        """

    def test_determine_action_for_file_when_neither_already_named_properly(self):
        """ Tests two files with identical hashes, neither having been renamed
            Expectation: One of the files is renamed, the other to be deleted.
        """





    def test_act_on_file_when_ignore(self):
        pass
    def test_act_on_file_when_renane(self):
        pass
    def test_act_on_file_when_renane_and_simulation_mode(self):
        pass


    @mock.patch('argparse.ArgumentParser.parse_args',
        return_Value=argparse.Namespace(kwarg1='E'))
    # @mock.patch('Task.os.path')
    @mock.patch('statement_renamer.tasks.task.Task')
    def test_act_on_file_when_delete(self, mock_task, mock_parser):
        # mock_os, mock_path
        # mock_parser.parse_args = empty_function
        task = Task(mock_parser, logger=None)
        task.config.simulate = False

        print(task.action_totals)
        assert(task.action_totals[ActionType.ignore] == 1, 'task.action_totals: {0}'.format(task.action_totals))
        assert(task.action_totals[ActionType.delete] == 0, 'task.action_totals: {0}'.format(task.action_totals))
        assert(task.action_totals[ActionType.rename] == 0, 'task.action_totals: {0}'.format(task.action_totals))
     


    def test_act_on_file_when_delete_and_simulation_mode(self):
        pass

def act_on_file(self, action):

    # Increment action total
    self.action_totals[action.action_type.name] += 1

    if self.args.simulate:
        if not self.args.quiet:
            print('SIMULATION ' + str(action))
        return

    if action.action_type is ActionType.rename:
        self._perform_rename_(action)

    elif action.action_type is ActionType.delete:
        os.remove(action.source)