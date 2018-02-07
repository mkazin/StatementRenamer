import os
import sys
import argparse
from readers.pdf_reader import PdfReader
from extractors.exceptions import ExtractorException
from extractors.factory import ExtractorFactory
from readers.reader_exception import ReaderException
from formatters.date_formatter import DateFormatter


class Task(object):

    def __init__(self, parser):
        self.args = parser.parse_args()
        # TODO: inject these
        self.reader = PdfReader()
        self.date_formatter = DateFormatter()

    def execute(self):
        if os.path.isfile(self.args.positional):
            self.process_file(self.args.positional)

        elif os.path.isdir(self.args.positional):
            for dir_name, subdir_list, file_list in os.walk(self.args.positional):

                for curr_file in file_list:

                    curr_path = (dir_name + '/' + curr_file).replace('//', '/')

                    try:
                        self.process_file(curr_path)
                    except ReaderException as e:
                        print('Failed to read {} : {}'.format(
                            curr_path, str(e)))
                        continue
                    except ExtractorException as e:
                        print('Failed to extract {} : {}'.format(
                            curr_path, str(e)))
                        continue
        else:
            print("Error: file or folder not found: {}".format(self.args.positional))

    def process_file(self, filepath):
        contents = self.reader.parse(filepath)

        if self.args.extract_only:
            print(contents)
            return

        extractor = ExtractorFactory.get_matching_extractor(contents)

        data = extractor.extract(contents)

        sim_text = 'SIMULATION ' if self.args.simulate else ''
        print('{}{} : {}'.format(
            sim_text,
            self.date_formatter.format(data['start_date']),
            filepath))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-E', '--extract-only',
                        dest='extract_only',
                        action='store_true',
                        help=('Extract-only mode. Returns content of PDF).'),
                        required=False)
    parser.add_argument('-S', '--simulate',
                        dest='simulate',
                        action='store_true',
                        help=('Simulation mode. Outputs actions that would be taken).'),
                        required=False)

    parser.add_argument('positional',
                        # dest='target',
                        action='store',
                        help='File or folder to process',
                        # required=True,
                        type=str)

    task = Task(parser)
    task.execute()
