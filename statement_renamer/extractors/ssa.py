from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException


class SocialSecurityExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class SocialSecurityDateExtractor(DateExtractor):

    EXCEPTION = SocialSecurityExtractorException
    SEARCH_TEXT = 'Your estimated taxable earnings per year after '
    FILE_FORMAT = '{} Yearly Statement.pdf'

    @staticmethod
    def match(text):
        return (__class__.SEARCH_TEXT in text)

    def extract(self, text):

        start = 0
        while True:
            start = text.find(self.__class__.SEARCH_TEXT, start + 1)
            extracted = text[start:start + len(self.__class__.SEARCH_TEXT) + 4]

            self.__handle_search_failure__(start < 0)

            try:
                parts = extracted.split(' ')

                start += len(self.__class__.SEARCH_TEXT)

                start_date = datetime(int(parts[-1]), 1, 1)
                end_date = datetime(int(parts[-1]), 12, 31)
                return ExtractedData(start_date, end_date)

            except ValueError:
                print("ValueError at index: {} - [{}]".format(start, extracted))
                pass

    def rename(self, extracted_data):
        return self.__class__.FILE_FORMAT.format(
            extracted_data.get_end_date().year)
