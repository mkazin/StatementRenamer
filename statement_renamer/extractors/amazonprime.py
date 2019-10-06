from .extractor import DateExtractor, ExtractedData, ExtractorException


class AmazonPrimeExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class AmazonPrimeDateExtractor(DateExtractor):

    EXCEPTION = AmazonPrimeExtractorException
    MATCH_TEXT = 'www.chase.com/amazon'
    PRE_DATE_TEXT = 'Opening/Closing Date'
    POST_DATE_TEXT = 'Credit Access Line'
    FILE_FORMAT = '{}-{:02} AmazonPrime Statement.pdf'
    DATE_FORMAT = '%m/%d/%y'
    SPLIT_TEXT = ' - '

    @staticmethod
    def match(text):
        return (__class__.MATCH_TEXT in text)

    def extract(self, text):
        return self._pre_post_split_extraction_(text)
