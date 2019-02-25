import os

from ..extractors.extractor import ExtractorException
from ..extractors.factory import ExtractorFactory
from ..formatters.date_formatter import DateFormatter
from ..readers.md5_reader import Md5Reader
from ..readers.pdf_reader import PdfReader
from ..readers.reader_exception import ReaderException
from ..tasks.action import ActionType, Action
# from ..tasks.deduplicator import Deduplicator
from tqdm import tqdm


def walkdir(folder):
    """Walk through each files in a directory"""
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            yield os.path.abspath(os.path.join(dirpath, filename))


class Task(object):

    class Config(object):

        @staticmethod
        def __get_val_or__(obj, field, default):
            if obj:
                return obj.get(field)
            return default

        @staticmethod
        def from_parser(parser):
            args = parser.parse_args()
            return Task.Config(
                location=args.location, quiet=args.quiet, verbose=args.verbose,
                simulate=args.simulate, hash_only=args.hash_only,
                extract_only=args.extract_only)

        def __init__(self, location,
                     quiet=False, verbose=False, simulate=False,
                     hash_only=False, extract_only=False):
            self.location = location
            self.quiet = quiet
            self.verbose = verbose
            self.simulate = simulate
            self.hash_only = hash_only
            self.extract_only = extract_only

    def __init__(self, parser, logger=None):
        self.config = Task.Config.from_parser(parser)
        # TODO: inject these
        self.reader = PdfReader()
        self.date_formatter = DateFormatter()
        self.logger = logger

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

    # def __deduplicate_actions__(self):
    #     deduper = Deduplicator(self.actions)
    #     new_actions = deduper.deduplicate_actions()

    def execute(self):
        self.__reset_action_totals__()

        if os.path.isfile(self.config.location):
            self.determine_action_for_file(self.config.location)

        elif os.path.isdir(self.config.location):

            dir_name = self.config.location
            for curr_file in tqdm(walkdir(self.config.location),
                                  disable=self.config.quiet or self.config.verbose,
                                  desc='Processing Files', unit=' files'):
                dir_name = os.path.dirname(curr_file)
                curr_path = curr_file  # (dir_name + '/' + curr_file).replace('//', '/')
                self.logger.info('Processing: {}'.format(curr_path))
                if self.config.verbose:
                    print('Processing: {}'.format(curr_path))

                try:
                    self.determine_action_for_file(curr_path)
                except ReaderException as e:
                    # print('Failed to read {} : {}'.format(
                    #     curr_path, str(e)))
                    self.actions.append(Action.create_ignore_action(
                        curr_path, reason='Failed to read file {}'.format(curr_path)))
                    self.logger.exception(e)
                    continue
                except ExtractorException as e:
                    # print('Failed to extract {} : {}'.format(
                    #     curr_path, str(e)))
                    self.actions.append(Action.create_ignore_action(
                        curr_path, reason=str(e)))  # 'Failed to extract text from PDF'
                    self.logger.exception(e)
                    continue
        else:
            print("Error: file or folder not found: {}".format(self.config.location))

        print('Done processing files')

        # self.__deduplicate_actions__()
        self.__perform_actions__()

        summary = 'Summary: ' + ', '.join(
            ['{}: {}'.format(key.capitalize(), self.action_totals[key])
             for key in self.action_totals.keys()])
        self.logger.debug(summary)
        if not self.config.quiet:
            if self.config.simulate:
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
        if self.config.hash_only:
            print('{} - {}'.format(hash, filepath))
            return

        # if hash in self.hashes:
        #     self.actions.append(Action.create_delete_action(
        #         filepath, reason='Duplicate hash: {}'.format(hash)))
        #     return

            # TODO: can PdfReader accept/process the same streamed data as Md5Reader?
        contents = self.reader.parse(filepath)

        if self.config.extract_only:
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

            # OPTIMIZE: likely possible here:
            #       Let there be 25 copies of a file in a folder.
            #       Hypothesis: the contents will be hashed 50 times, when we could
            #       suffice with 25 hashes.
            existing_hash = Md5Reader().parse(new_path)
            if existing_hash == data.get_hash():
                reason = ('Found duplicate hash ({}) shared by [{}].'.
                          format(existing_hash, new_path, data.get_source()))
                action = Action.create_delete_action(data.get_source(), reason=reason)

            else:
                action = Action.create_dedup_action(
                    filepath,
                    reason=(
                        'Target File [{}] already exists. Ignoring to avoid an overwrite.'
                        .format(new_name)))
        else:
            action = Action.create_rename_action(filepath, new_path)

        self.actions.append(action)

        if self.config.verbose:
            print('Adding action: {}'.format(action))

    def _perform_rename_(self, action):
        """ Perform the rename operation in the provided Action """
        if os.path.isfile(action.target):
            error_text = (
                'Aborting action {} to avoid overwrite of target'.format(action))
            if not self.config.quiet:
                print(error_text)
            self.logger.error(error_text)
            return
        os.rename(action.source, action.target)

    def act_on_file(self, action):

        # Increment action total
        self.action_totals[action.action_type.name] += 1

        if self.config.simulate:
            if not self.config.quiet:
                print('SIMULATION ' + str(action))
            return

        if action.action_type is ActionType.rename:
            self._perform_rename_(action)

        elif action.action_type is ActionType.delete:
            os.remove(action.source)
