from datetime import datetime
from .extractor import DateExtractor, ExtractorException


class VanguardExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class VanguardDateExtractor(DateExtractor):

    EXCEPTION = VanguardExtractorException
    DATE_FORMAT = '%m/%d/%Y'
    SEARCH_TEXT = 'Beginning balance on '
    END_TEXT = 'Ending balance on '

    @staticmethod
    def match(text):
        return 'Vanguard, P.O. Box 2600Valley Forge, PA 19482-2600' in text

    def extract(self, text):

        data = {}
        data['start_date'] = None
        data['end_date'] = None

        data['start_date'] = self.__get_date_following__(
            text, self.__class__.SEARCH_TEXT)
        data['end_date'] = self.__get_date_following__(
            text, self.__class__.END_TEXT)

        return data

    def __get_date_following__(self, text, clause):

        start = 0
        while True:
            start = text.find(clause, start + 1)

            if start < 0:
                raise self.__class__.EXCEPTION(
                    type(self).__name__ + ': Expected text not found')

            try:
                start += len(clause)
                parts = text[start:].strip().split('$')

                return datetime.strptime(parts[0], self.__class__.DATE_FORMAT)

            except ValueError:
                print("ValueError at index: {} - [{}]".format(start, text[start:]))
                pass
