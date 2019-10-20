from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException


class VanguardExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class VanguardDateExtractor(DateExtractor):

    EXCEPTION = VanguardExtractorException
    DATE_FORMAT = '%m/%d/%Y'
    SEARCH_TEXT = 'Beginning balance on '
    END_TEXT = 'Ending balance on '
    FILE_FORMAT = '{:2}-Q{} Quarterly Statement.pdf'

    @staticmethod
    def match(text):
        return ('Client Services: 800-662-2739' in text and
                ('year-to-date statement' in text or
                 'quarter-to-date statement' in text))

    def extract(self, text):

        return ExtractedData(
            self.__get_date_following__(
                text, self.__class__.SEARCH_TEXT),
            self.__get_date_following__(
                text, self.__class__.END_TEXT))

    def __get_date_following__(self, text, clause):

        start = 0
        while True:
            start = text.find(clause, start + 1)

            self.__handle_search_failure__(start < 0)

            try:
                start += len(clause)
                parts = text[start:].strip().split('$')

                return datetime.strptime(parts[0], self.__class__.DATE_FORMAT)

            except ValueError:
                print("ValueError at index: {} - [{}]".format(start, text[start:]))
                pass

    def rename(self, extracted_data):
        return self.__class__.FILE_FORMAT.format(
            extracted_data.get_end_date().year,
            extracted_data.get_end_date().month // 3)
