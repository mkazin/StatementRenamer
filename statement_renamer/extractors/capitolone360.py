from datetime import datetime
from .exceptions import ExtractorException


class CapitolOne360ExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class CapitolOne360DateExtractor(object):  # DateExtractor

    DATE_FORMAT = '%m/%d/%Y'
    SEARCH_TEXT = "Opening Balance"
    END_TEXT = 'Closing Balance'

    def match(self, text):
        return 'My Info section.capitalone360.comInteractive' in text

    def extract(self, text):

        data = {}
        data['start_date'] = None
        data['end_date'] = None

        start = 0
        while True:
            start = text.find(self.__class__.SEARCH_TEXT, start + 1)

            if start < 0:
                raise CapitolOne360ExtractorException(
                    type(self).__name__ + ': Expected text not found')

            try:
                start += len(self.__class__.SEARCH_TEXT)
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
            # except NumberError:
            #     print("ValueError at index: {}".format(start))
            except ValueError:
                print("ValueError at index: {} - [{}]".format(start, text[start:]))
                pass

        return data
