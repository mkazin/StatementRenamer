import os

from extractors.extractor import ExtractorException
from extractors.factory import ExtractorFactory
from formatters.date_formatter import DateFormatter
from main import walkdir
from readers.md5_reader import Md5Reader
from readers.pdf_reader import PdfReader
from readers.reader_exception import ReaderException
from tasks.action import ActionType, Action


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

        if os.path.isfile(self.args.location):
            self.determine_action_for_file(self.args.location)

        elif os.path.isdir(self.args.location):

            dir_name = self.args.location
            for curr_file in tqdm(walkdir(self.args.location),
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
            print("Error: file or folder not found: {}".format(self.args.location))

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

        if self.args.simulate:
            if not self.args.quiet:
                print('SIMULATION ' + str(action))
            return

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