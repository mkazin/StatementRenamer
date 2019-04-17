from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException


class AWSExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class AWSDateExtractor(DateExtractor):

    EXCEPTION = AWSExtractorException
    MATCH_TEXT = 'All AWS Services are sold by Amazon Web Services, Inc.'
    PRE_DATE_TEXT = 'This invoice is for the billing period '
    POST_DATE_TEXT = 'Greetings from Amazon Web Services'
    FILE_FORMAT = '{}-{:02} AWS Invoice.pdf'

    @staticmethod
    def match(text):
        return (__class__.MATCH_TEXT in text)

    def extract(self, text):
        start = text.find(self.__class__.PRE_DATE_TEXT) + \
            len(self.__class__.PRE_DATE_TEXT)
        end = text.find(self.__class__.POST_DATE_TEXT)
        extracted = text[start:end]

        self.__handle_search_failure__(start < 0)

        parts = extracted.split(' ')
        start_day = int(parts[1])
        end_day = int(parts[4])
        month = datetime.strptime(parts[0], '%B').month
        year = int(parts[6])

        start_date = datetime(year, month, start_day)
        end_date = datetime(year, month, end_day)
        return ExtractedData(start_date, end_date)
