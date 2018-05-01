import argparse
import enum
import logging
import os
import sys
from tqdm import tqdm
from readers.md5_reader import Md5Reader
from readers.pdf_reader import PdfReader
import extractors
from extractors.extractor import ExtractorException
from extractors.factory import ExtractorFactory
from readers.reader_exception import ReaderException
from formatters.date_formatter import DateFormatter


@enum.unique
class ActionType(enum.Enum):
    delete = 3
    ignore = 2
    rename = 1


class Action(object):

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
        return Action(ActionType.delete, filepath, reason=reason)

    @staticmethod
    def create_rename_action(source_filepath, target_filepath):
        return Action(ActionType.rename, source_filepath, target_filepath)

    @staticmethod
    def create_ignore_action(filepath, reason):
        return Action(ActionType.ignore, filepath, target=None, reason=reason)


class Task(object):

    def __init__(self, parser, logger=None):
        self.args = parser.parse_args()
        # TODO: inject these
        self.reader = PdfReader()
        self.date_formatter = DateFormatter()
        self.logger = logger

        self.actions = []
        self.hashes = []
        self.action_totals = {}

    def execute(self):
        # Map to track number of actions performed per action type
        for action_type in ActionType:
            self.action_totals[action_type.name] = 0

        if os.path.isfile(self.args.positional):
            self.determine_action_for_file(self.args.positional)

        elif os.path.isdir(self.args.positional):

            dir_name = self.args.positional
            for curr_file in tqdm(walkdir(self.args.positional),
                                  disable=self.args.quiet or self.args.verbose,
                                  desc='Processing Files', unit=' files'):
                dir_name = os.path.dirname(curr_file)
                curr_path = curr_file  # (dir_name + '/' + curr_file).replace('//', '/')
                self.logger.info('Processing: {}'.format(curr_path))
                if self.args.verbose:
                    print('Processing: {}'.format(curr_path))

                try:
                    self.determine_action_for_file(curr_path)
                except ReaderException as e:
                    # print('Failed to read {} : {}'.format(
                    #     curr_path, str(e)))
                    self.actions.append(Action.create_ignore_action(
                        curr_path, reason='Failed to read file {}'.format(curr_path)))
                    self.logger.exception(e)
                    self.action_totals[ActionType.ignore.name] += 1
                    continue
                except ExtractorException as e:
                    # print('Failed to extract {} : {}'.format(
                    #     curr_path, str(e)))
                    self.actions.append(Action.create_ignore_action(
                        curr_path, reason=str(e)))  # 'Failed to extract text from PDF'
                    self.logger.exception(e)
                    self.action_totals[ActionType.ignore.name] += 1
                    continue
        else:
            print("Error: file or folder not found: {}".format(self.args.positional))

        print('Done processing files')
        for action in self.actions:
            self.logger.debug(action)
            self.act_on_file(action)

        summary = 'Summary: ' + ', '.join(
            ['{}: {}'.format(key.capitalize(), self.action_totals[key])
             for key in self.action_totals.keys()])
        self.logger.debug(summary)
        if not self.args.quiet:
            if self.args.simulate:
                summary = 'SIMULATED ' + summary
            print(summary)

    def determine_action_for_file(self, filepath):
        """ Determine the action required on the specified file:
            - Checks for a duplicate using MD5 hash
            - Extracts text from the document
            - Extracts meaningful data from the document
            - Constructs the necessary Action to take on the file and appends
              it to the actions list
        """

        # TODO: perform this every time? Or only when we find a duplicate target filename?
        hash = Md5Reader().parse(filepath)
        if self.args.hash_only:
            print('{} - {}'.format(hash, filepath))
            return

        if hash in self.hashes:
            self.actions.append(Action.create_delete_action(
                filepath, reason='Duplicate hash: {}'.format(hash)))
            return

            # TODO: can PdfReader accept/process the same streamed data as Md5Reader?
        contents = self.reader.parse(filepath)

        if self.args.extract_only:
            print(contents)
            return

        extractor = ExtractorFactory.get_matching_extractor(contents)

        data = extractor.extract(contents)

        data.set_source(filepath)
        data.set_hash(hash)

        new_name = extractor.rename(data)
        old_name = filepath.split('/')[-1]
        new_path = filepath[0:filepath.rfind('/') + 1] + new_name

        self.hashes.append(hash)

        if old_name == new_name:
            action = Action.create_ignore_action(
                filepath, reason='Already named correctly')
        elif os.path.isfile(new_path):

            # TODO: this isn't good enough to avoid an overwrite, as there is no
            #       coordination between files.
            #       How about storing the data objects in a hash of target paths?
            #       Or, key's c

            existing_hash = Md5Reader().parse(new_path)
            if existing_hash == data.get_hash():
                reason = ('Found duplicate hash ({}) shared by [{}] and [{}].'.
                          format(existing_hash, new_path, data.get_source()))
                action = Action.create_delete_action(data.get_source(), reason=reason)

            else:
                action = Action.create_ignore_action(
                    filepath,
                    reason=(
                        'Target File [{}] already exists. Ignoring to avoid an overwrite.'
                        .format(new_name)))
        else:
            action = Action.create_rename_action(filepath, new_path)

        self.actions.append(action)

        if self.args.verbose:
            print('Adding action: {}'.format(action))

    def act_on_file(self, action):
        self.action_totals[action.action_type.name] += 1

        if self.args.simulate:
            if not self.args.quiet:
                print('SIMULATION ' + str(action))
            return
        # print(action)

        if action.action_type is ActionType.rename:
            if os.path.isfile(action.target):
                error_text = (
                    'Aborting action {} to avoid overwrite of target'.format(action))
                if not self.args.quiet:
                    print(error_text)
                self.logger.error(error_text)
                return
            os.rename(action.source, action.target)
        elif action.action_type is ActionType.delete:
            os.remove(action.source)


LOG_FILE_NAME = 'Logs/output.log'
logger = logging.getLogger('StatementRenamer')


def main():

    handler = logging.FileHandler(LOG_FILE_NAME)
    logger.addHandler(handler)
    logger.setLevel("DEBUG")  # WARNING")
    logger.warning('Starting rename with params: [{}]'.format(' '.join(sys.argv[1:])))

    parser = argparse.ArgumentParser()

    parser.add_argument('-E', '--extract-only',
                        dest='extract_only',
                        action='store_true',
                        help=('Extract-only mode. Returns content of PDF'),
                        required=False)
    parser.add_argument('-H', '--hash-only',
                        dest='hash_only',
                        action='store_true',
                        help=('Hash-only mode. Returns MD5 hash of input files'),
                        required=False)
    parser.add_argument('-S', '--simulate',
                        dest='simulate',
                        action='store_true',
                        help=('Simulation mode. Outputs actions that would be taken'),
                        required=False)
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help=('Verbose mode. Outputs detailed information'),
                        required=False)
    parser.add_argument('-q', '--quiet',
                        dest='quiet',
                        action='store_true',
                        help=('Quiet mode. Produces no console output'),
                        required=False)

    parser.add_argument('positional',
                        # dest='target',
                        action='store',
                        help='File or folder to process',
                        # required=True,
                        type=str)

    try:
        task = Task(parser, logger)
        task.execute()
    except Exception as e:
        logger.exception(e)
        raise e


def walkdir(folder):
    """Walk through each files in a directory"""
    results = []
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            # yield os.path.abspath(os.path.join(dirpath, filename))
            results.append(os.path.abspath(os.path.join(dirpath, filename)))
    return results
