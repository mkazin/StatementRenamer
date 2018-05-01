from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException


class CapitalOne360ExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class CapitalOne360DateExtractor(DateExtractor):

    EXCEPTION = CapitalOne360ExtractorException
    DATE_FORMAT = '%m/%d/%Y'
    SEARCH_TEXT = "Opening Balance"
    END_TEXT = 'Closing Balance'
    FILE_FORMAT = '{:02}-{:02}-CapitalOne360.pdf'

    @staticmethod
    def match(text):
        return 'My Info section.capitalone360.comInteractive' in text

    def extract(self, text):

        start_date = None
        end_date = None

        start = 0
        while True:
            start = text.find(self.__class__.SEARCH_TEXT, start + 1)

            if start < 0:
                raise self.__class__.EXCEPTION(
                    type(self).__name__ + ': Expected text not found')

            start += len(self.__class__.SEARCH_TEXT)

            try:
                int(text[start])
                parts = text[start:].strip().split('$')

                start_date = datetime.strptime(
                    parts[0], self.__class__.DATE_FORMAT)

                end = text.find(self.__class__.END_TEXT)
                end_text = text[end + len(self.__class__.END_TEXT):]
                int(end_text[0])
                parts = end_text.replace(' ', '').split('$')
                end_date = datetime.strptime(
                    parts[0], self.__class__.DATE_FORMAT)
                break

            except ValueError:
                print("ValueError at index: {} - [{}]".format(start, text[start:]))
                pass

        return ExtractedData(start_date, end_date)

    def rename(self, extracted_data):
        return self.__class__.FILE_FORMAT.format(
            extracted_data.get_end_date().year,
            extracted_data.get_end_date().month)