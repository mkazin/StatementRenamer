from .extractor import DateExtractor, ExtractedData, ExtractorException


class ChaseExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class ChaseDateExtractor(DateExtractor):

    EXCEPTION = ChaseExtractorException
    MATCH_TEXT = 'www.chase.com/creditcards'
    PRE_DATE_TEXT = 'Opening/Closing Date'
    POST_DATE_TEXT = 'Credit Limit'
    FILE_FORMAT = '{}-{:02} Chase Slate Statement.pdf'
    DATE_FORMAT = '%m/%d/%y'
    SPLIT_TEXT = ' - '

    @staticmethod
    def match(text):
        return (__class__.MATCH_TEXT in text)

    def extract(self, text):
        return self._pre_post_split_extraction_(text)

    def rename(self, extracted_data):
        """ Return a string with a new name for the file.
        """
        return self.__class__.FILE_FORMAT.format(
            extracted_data.get_start_date().year,
            extracted_data.get_start_date().month)
