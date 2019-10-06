from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException
from .utils.dateutil import DateUtil


class ETradeExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class ETradeDateExtractor(DateExtractor):

    EXCEPTION = ETradeExtractorException
    MATCH_TEXT = 'visitwww.etrade.com,orcallusat1-800-387-2331'
    PRE_DATE_TEXT = 'Statement Period :  '  # February 1, 2019 - March 31, 2019'
    POST_DATE_TEXT = 'Account Type'
    FILE_FORMAT = '{}-{:02} E-Trade Statement.pdf'

    @staticmethod
    def match(text):
        return (__class__.MATCH_TEXT in text)

    def extract(self, text):
        start = text.find(self.__class__.PRE_DATE_TEXT) + \
            len(self.__class__.PRE_DATE_TEXT)
        end = text.find(self.__class__.POST_DATE_TEXT)

        # Re-generated statements will mention the statement has been "corrected":
        extracted = text[start:end].split(' - ')

        self.__handle_search_failure__(len(extracted) < 2)

        start_date = datetime.strptime(extracted[0], '%B %d, %Y')
        end_date = datetime.strptime(extracted[1], '%B %d, %Y')
        # end_date = DateUtil.last_day_of_month(start_date)
        return ExtractedData(start_date, end_date)
