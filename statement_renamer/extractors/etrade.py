from .extractor import DateExtractor, ExtractorException


class ETradeExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class ETradeDateExtractor(DateExtractor):

    EXCEPTION = ETradeExtractorException
    MATCH_TEXT = 'visitwww.etrade.com,orcallusat1-800-387-2331'
    PRE_DATE_TEXT = 'Statement Period :  '
    POST_DATE_TEXT = 'Account Type'
    FILE_FORMAT = '{}-{:02} E-Trade Statement.pdf'
    DATE_FORMAT = '%B %d, %Y'
    SPLIT_TEXT = ' - '

    @staticmethod
    def match(text):
        return __class__.MATCH_TEXT in text

    def extract(self, text):
        return self._pre_post_split_extraction_(text)
