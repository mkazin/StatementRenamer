from datetime import datetime
from .extractor import DateExtractor, ExtractorException


class CapitolOne360ExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class CapitolOne360DateExtractor(DateExtractor):

    EXCEPTION = CapitolOne360ExtractorException
    DATE_FORMAT = '%m/%d/%Y'
    SEARCH_TEXT = "Opening Balance"
    END_TEXT = 'Closing Balance'

    @staticmethod
    def match(text):
        return 'My Info section.capitalone360.comInteractive' in text

    def extract(self, text):

        data = {}
        data['start_date'] = None
        data['end_date'] = None

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

                data['start_date'] = datetime.strptime(
                    parts[0], self.__class__.DATE_FORMAT)

                end = text.find(self.__class__.END_TEXT)
                end_text = text[end + len(self.__class__.END_TEXT):]
                int(end_text[0])
                parts = end_text.replace(' ', '').split('$')
                data['end_date'] = datetime.strptime(
                    parts[0], self.__class__.DATE_FORMAT)
                break

            except ValueError:
                print("ValueError at index: {} - [{}]".format(start, text[start:]))
                pass

        return data
