from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException
from .utils.dateutil import DateUtil


class AmazonPrimeExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class AmazonPrimeDateExtractor(DateExtractor):

    EXCEPTION = AmazonPrimeExtractorException
    MATCH_TEXT = 'www.chase.com/amazon'
    PRE_DATE_TEXT = 'Opening/Closing Date'
    POST_DATE_TEXT = 'Credit Access Line'
    FILE_FORMAT = '{}-{:02} AmazonPrime Statement.pdf'

    @staticmethod
    def match(text):
        return (__class__.MATCH_TEXT in text)

    def extract(self, text):
        start = text.find(self.__class__.PRE_DATE_TEXT) + \
            len(self.__class__.PRE_DATE_TEXT)
        end = text.find(self.__class__.POST_DATE_TEXT)

        extracted = text[start:end].split(' - ')

        self.__handle_search_failure__(len(extracted) < 2)

        start_date = datetime.strptime(extracted[0], '%m/%d/%y')
        end_date = datetime.strptime(extracted[1], '%m/%d/%y')
        return ExtractedData(start_date, end_date)