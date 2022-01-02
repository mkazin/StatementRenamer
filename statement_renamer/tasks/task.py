""" Primary functionality and configuration of StatementRenamer """
import logging
from tqdm import tqdm
from statement_renamer.extractors.extractor import ExtractorException, NoMatchingExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from statement_renamer.formatters.date_formatter import DateFormatter
from statement_renamer.readers.hash_reader import HashReader
from statement_renamer.readers.pdf_reader import PdfReader
from statement_renamer.readers.reader_exception import ReaderException
from statement_renamer import config
from .action import ActionType, Action


class Task(object):
    """ Central task of StatementRenamer. Uses Config to define parameters of execution """

    def __init__(self, file_handler_class):
        self.reader = PdfReader()
        self.date_formatter = DateFormatter()
        self.logger = logging.getLogger('StatementRenamer')
        self.file_handler = file_handler_class()

        self.actions = []
        self.hashes = []
        self.action_totals = {}

        self.hash_reader = HashReader()


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

        if self.file_handler.is_file(config.LOCATION):
            self.logger.debug(f'Handling single file at {config.LOCATION}')
            self.determine_action_for_file(config.LOCATION)

        elif self.file_handler.is_folder(config.LOCATION):
            self.handle_folder()

        else:
            self.logger.error("Error: file or folder not found: %s", config.LOCATION)

        self.logger.debug('Done processing files')

        self.__perform_actions__()

        summary = 'Summary: ' + ', '.join(
            ['{}: {}'.format(key.capitalize(), self.action_totals[key])
             for key in self.action_totals.keys()])
        self.logger.debug(summary)
        if not config.QUIET:
            if config.SIMULATE:
                summary = 'SIMULATED ' + summary
            print(summary)

    def handle_folder(self):
        """ Iterates over the files in the configured folder """
        for curr_file in tqdm(self.file_handler.walkdir(config.LOCATION),
                              disable=config.QUIET or config.VERBOSE,
                              desc='Processing Files', unit=' files'):
            # dir_name = os.path.dirname(curr_file)
            curr_path = curr_file  # (dir_name + '/' + curr_file).replace('//', '/')
            self.logger.info('Processing: {%s}', curr_path)
            if config.VERBOSE:
                print('Processing: {}'.format(curr_path))

            try:
                self.determine_action_for_file(curr_path)
            except ReaderException as ex:
                self.actions.append(Action.create_ignore_action(
                    curr_path, reason='Failed to read file {}'.format(curr_path)))
                self.logger.exception(ex)
                continue
            except NoMatchingExtractor as ex:
                self.actions.append(Action.create_ignore_action(
                    curr_path, reason=str(ex)))  # 'Failed to extract text from PDF'
                self.logger.debug('No matching extractor for file {%s}', curr_path)
            except ExtractorException as ex:
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
        file_hash = self.hash_reader.parse(filepath)
        if config.HASH_ONLY:
            print('{} - {}'.format(file_hash, filepath))
            return

        if file_hash in self.hashes:
            self.actions.append(Action.create_delete_action(
                filepath, reason='Duplicate hash: {}'.format(file_hash)))
            return

            # TODO: can PdfReader accept/process the same streamed data as Md5Reader?
        contents = self.reader.parse(filepath)

        if config.EXTRACT_ONLY:
            print(contents)
            return

        extractor = ExtractorFactory.get_matching_extractor(contents)

        data = extractor.extract(contents)

        data.set_source(filepath)
        data.set_hash(file_hash)

        new_name = extractor.rename(data)
        old_name = self.file_handler.basename(filepath)

        target_path = config.DESTINATION if config.DESTINATION else filepath
        new_path = self.file_handler.build_path(self.file_handler.pathname(target_path), new_name)

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

        if config.VERBOSE:
            print('Adding action: {}'.format(action))

    def act_on_file(self, action):
        """ Breakout function to each type for a single Action. Respects simulation config. """

        # Increment counter for this action's type
        self.action_totals[action.action_type.name] += 1

        if config.SIMULATE:
            if not config.QUIET:
                print('SIMULATION ' + str(action))
            return

        self.file_handler.handle(action)
