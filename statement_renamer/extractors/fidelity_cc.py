""" Extractor for Fidelity Credit Card Statements. Does not include employer-sponsored retirement accounts. """
from .extractor import DateExtractor, ExtractorException


class FidelityCreditCardExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class FidelityCreditCardDateExtractor(DateExtractor):
    """ Extractor implementation """
    EXCEPTION = FidelityCreditCardExtractorException
    MATCH_TEXT = 'fidelityrewards.com/login'
    PRE_DATE_TEXT = 'Open Date:'
    POST_DATE_TEXT = 'Account:'
    FILE_FORMAT = '{}-{:02} - Fidelity CC Statement.pdf'
    # MULTI_MONTH_FILE_FORMAT = '{}-{:02}-{:02} - Fidelity CC Statement.pdf'
    # QUARTERLY_FILE_FORMAT = '{}-Q{} - Fidelity CC Quarterly Statement.pdf'
    # YEARLY_FILE_FORMAT = "{} - Fidelity CC Year-End Statement.pdf"
    DATE_FORMAT = '%m/%d/%Y'
    SPLIT_TEXT = 'Closing Date:'

    @staticmethod
    def match(text):
        return __class__.MATCH_TEXT in text

    def extract(self, text):
        return self._pre_post_split_extraction_(text)
