import os
import sys
from readers.pdf_reader import PdfReader
from extractors.ascensus import AscensusDateExtractor
from extractors.exceptions import ExtractorException
from readers.reader_exception import ReaderException
from formatters.date_formatter import DateFormatter


def main():

    # TODO: inject these
    reader = PdfReader()
    extractor = AscensusDateExtractor()
    date_formatter = DateFormatter()

    folder = sys.argv[1]
    for dir_name, subdir_list, file_list in os.walk(folder):

        for curr_file in file_list:

            curr_path = (dir_name + '/' + curr_file).replace('//', '/')

            try:
                contents = reader.parse(curr_path)
                data = extractor.extract(contents)
            except ReaderException as e:
                print('Failed to read {} : {}'.format(
                    curr_path, str(e)))
                continue
            except ExtractorException as e:
                print('Failed to extract {} : {}'.format(
                    curr_path, str(e)))
                continue

            print('{} : {}'.format(
                date_formatter.format(data['start_date']),
                curr_path))
