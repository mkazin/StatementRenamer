from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException
from .utils.dateutil import DateUtil


class RobinhoodExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class RobinhoodDateExtractor(DateExtractor):

    EXCEPTION = RobinhoodExtractorException
    MATCH_TEXT = 'Robinhood85 Willow Rd, Menlo Park, CA 94025support@robinhood.com'
    PRE_DATE_TEXT = 'support@robinhood.com'
    POST_DATE_TEXT = ' to '
    FILE_FORMAT = '{}-{:02} Robinhood Statement.pdf'

    @staticmethod
    def match(text):
        return (__class__.MATCH_TEXT in text)

    def extract(self, text):
        start = text.find(self.__class__.PRE_DATE_TEXT) + \
            len(self.__class__.PRE_DATE_TEXT)
        end = text.find(self.__class__.POST_DATE_TEXT)

        # Re-generated statements will mention the statement has been "corrected":
        extracted = text[start:end].replace('CORRECTED STATEMENT', '')

        self.__handle_search_failure__(start < 0)

        start_date = datetime.strptime(extracted, '%m/%d/%Y')
        end_date = DateUtil.last_day_of_month(start_date)
        return ExtractedData(start_date, end_date)
