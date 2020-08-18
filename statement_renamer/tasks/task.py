""" Primary functionality and configuration of StatementRenamer """
import os
from tqdm import tqdm
from statement_renamer.extractors.extractor import ExtractorException
from statement_renamer.extractors.factory import ExtractorFactory
from statement_renamer.formatters.date_formatter import DateFormatter
from statement_renamer.readers.md5_reader import Md5Reader
from statement_renamer.readers.pdf_reader import PdfReader
from statement_renamer.readers.reader_exception import ReaderException
from .action import ActionType, Action


class Task():
    """ Central task of StatementRenamer. Uses Config to define parameters of execution """

    class Config():
        """ Data object holding the parameters of the task to execute """
        @staticmethod
        def __get_val_or__(obj, field, default):
            if obj:
                return obj.get(field)
            return default

        @staticmethod
        def from_parser(parser):
            """ Instantiates a Config object based on values in ArgumentParser """
            args = parser.parse_args()
            return Task.Config(
                location=args.location, quiet=args.quiet, verbose=args.verbose,
                simulate=args.simulate, hash_only=args.hash_only, extract_only=args.extract_only)

        def __init__(self, location,
                     quiet=False, verbose=False, simulate=False,
                     hash_only=False, extract_only=False):
            self.location = location
            self.quiet = quiet
            self.verbose = verbose
            self.simulate = simulate
            self.hash_only = hash_only
            self.extract_only = extract_only



    def __init__(self, parser, file_handler_class, logger=None):
        self.config = Task.Config.from_parser(parser)
        # TODO: inject these
        self.reader = PdfReader()
        self.date_formatter = DateFormatter()
        self.logger = logger
        self.file_handler = file_handler_class(self.config, self.logger)

        self.actions = []
        self.hashes = []
        self.action_totals = {}


    def __reset_action_totals__(self):
        """ Sets up a map to track number of actions performed per action type """
        for action_type in ActionType:
            self.action_totals[action_type.name] = 0

    def __perform_actions__(self):
        for action in self.actions:
            self.logger.debug(action)
            self.act_on_file(action)

    def execute(self):
        self.__reset_action_totals__()

        if self.file_handler.is_file(self.config.location):
            self.determine_action_for_file(self.config.location)

        elif self.file_handler.is_folder(self.config.location):
            self.handle_folder()

        else:
            print("Error: file or folder not found: {}".format(self.config.location))

        print('Done processing files')

        self.__perform_actions__()

        summary = 'Summary: ' + ', '.join(
            ['{}: {}'.format(key.capitalize(), self.action_totals[key])
             for key in self.action_totals.keys()])
        self.logger.debug(summary)
        if not self.config.quiet:
            if self.config.simulate:
                summary = 'SIMULATED ' + summary
            print(summary)

    def handle_folder(self):
        """ Iterates over the files in the configured folder """
        for curr_file in tqdm(self.file_handler.walkdir(self.config.location),
                              disable=self.config.quiet or self.config.verbose,
                              desc='Processing Files', unit=' files'):
            # dir_name = os.path.dirname(curr_file)
            curr_path = curr_file  # (dir_name + '/' + curr_file).replace('//', '/')
            self.logger.info('Processing: {}'.format(curr_path))
            if self.config.verbose:
                print('Processing: {}'.format(curr_path))

            try:
                self.determine_action_for_file(curr_path)
            except ReaderException as ex:
                # print('Failed to read {} : {}'.format(
                #     curr_path, str(ex)))
                self.actions.append(Action.create_ignore_action(
                    curr_path, reason='Failed to read file {}'.format(curr_path)))
                self.logger.exception(ex)
                continue
            except ExtractorException as ex:
                # print('Failed to extract {} : {}'.format(
                #     curr_path, str(ex)))
                self.actions.append(Action.create_ignore_action(
                    curr_path, reason=str(ex)))  # 'Failed to extract text from PDF'
                self.logger.exception(ex)
                continue

    def determine_action_for_file(self, filepath):
        """ Determine the action required on the specified file:
            - Checks for a duplicate using MD5 hash
            - Extracts text from the document
            - Extracts meaningful data from the document
            - Constructs the necessary Action to take on the file and appends
              it to the actions list
        """

        # TODO: perform this every time? Or only when we find a duplicate target filename?
        file_hash = Md5Reader().parse(filepath)
        if self.config.hash_only:
            print('{} - {}'.format(file_hash, filepath))
            return

        if file_hash in self.hashes:
            self.actions.append(Action.create_delete_action(
                filepath, reason='Duplicate hash: {}'.format(file_hash)))
            return

            # TODO: can PdfReader accept/process the same streamed data as Md5Reader?
        contents = self.reader.parse(filepath)

        if self.config.extract_only:
            print(contents)
            return

        extractor = ExtractorFactory.get_matching_extractor(contents)

        data = extractor.extract(contents)

        data.set_source(filepath)
        data.set_hash(file_hash)

        # TODO: don't automatically reuse the input location, allow for a specified target location
        new_name = extractor.rename(data)
        old_name = self.file_handler.basename(filepath)
        new_path = self.file_handler.build_path(self.file_handler.pathname(filepath), new_name)

        self.hashes.append(file_hash)

        if old_name == new_name:
            action = Action.create_ignore_action(
                filepath, reason='Already named correctly')
        elif self.file_handler.file_exists(new_path):

            # TODO: this isn't good enough to avoid an overwrite, as there is no
            #       coordination between files.
            #       How about storing the data objects in a hash of target paths?
            #       Or, key's c

            existing_hash = Md5Reader().parse(new_path)
            if existing_hash == data.get_hash():
                reason = ('{} matches existing hash ({}) - shared by [{}].'.
                          format(data.get_source(), existing_hash, new_path))
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

        if self.config.verbose:
            print('Adding action: {}'.format(action))

    def act_on_file(self, action):
        """ Breakout function to each type for a single Action. Respects simulation config. """

        # Increment counter for this action's type
        self.action_totals[action.action_type.name] += 1

        if self.config.simulate:
            if not self.config.quiet:
                print('SIMULATION ' + str(action))
            return

        self.file_handler.handle(self, action)
