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
        return ('My Info section.capitalone360.comInteractive' in text or
               'capitalone.com  1-888-464-0727  P.O. Box 60, St. Cloud, MN 56302' in text)

    def extract(self, text):

        start_date = None
        end_date = None

        start = 0
        while True:
            start = text.find(self.__class__.SEARCH_TEXT, start + 1)

            self.__handle_search_failure__(start < 0)

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
