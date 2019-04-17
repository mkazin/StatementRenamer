from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException
from ..utils.dateutil import DateUtil


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

        if start < 0:
            raise self.__class__.EXCEPTION(
                type(self).__name__ + ': Expected text not found')

        start_date = datetime.strptime(extracted, '%m/%d/%Y')
        end_date = DateUtil.last_day_of_month(start_date)
        return ExtractedData(start_date, end_date)

    def rename(self, extracted_data):
        return self.__class__.FILE_FORMAT.format(
            extracted_data.get_end_date().year,
            extracted_data.get_end_date().month)