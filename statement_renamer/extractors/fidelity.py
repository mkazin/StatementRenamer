""" Extractor for Fidelity Brokerage Statements. Does not include employer-sponsored retirement accounts. """
from .extractor import DateExtractor, ExtractorException


class FidelityExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class FidelityDateExtractor(DateExtractor):
    """ Exctractor implementation """
    EXCEPTION = FidelityExtractorException
    MATCH_TEXT = 'Brokerage services provided by Fidelity Brokerage Services LLC (FBS), Member NYSE, SIPC (800) 544-6666'
    PRE_DATE_TEXT = 'INVESTMENT REPORT'
    POST_DATE_TEXT = 'Envelope #'
    FILE_FORMAT = '{}-{:02} - Fidelity Statement.pdf'
    MULTI_MONTH_FILE_FORMAT = '{}-{:02}-{:02} - Fidelity Statement.pdf'
    QUARTERLY_FILE_FORMAT = '{}-Q{} - Fidelity Quarterly Statement.pdf'
    YEARLY_FILE_FORMAT = "{} - Fidelity Year-End Statement.pdf"
    DATE_FORMAT = '%B %d, %Y'
    SPLIT_TEXT = ' - '

    @staticmethod
    def match(text):
        return __class__.MATCH_TEXT in text

    def extract(self, text):
        return self._pre_post_split_extraction_(text)

    def rename(self, extracted_data):
        """ Overriding the base class implementation to handle Fidelity's crazy range of start/end dates:
            which includes: monthly, bi-monthly, quarterly, and year-end statements """
        if extracted_data.get_end_date().month == 12 and \
           extracted_data.get_start_date().month not in (11, 12):
            return self.__class__.YEARLY_FILE_FORMAT.format(
                extracted_data.get_end_date().year)

        elif extracted_data.get_end_date().month - extracted_data.get_start_date().month == 2:
            return self.__class__.QUARTERLY_FILE_FORMAT.format(
                extracted_data.get_end_date().year,
                extracted_data.get_end_date().month // 3)

        elif extracted_data.get_end_date().month != extracted_data.get_start_date().month:
            return self.__class__.MULTI_MONTH_FILE_FORMAT.format(
                extracted_data.get_end_date().year,
                extracted_data.get_start_date().month,
                extracted_data.get_end_date().month)

        return self._rename_using_month_(extracted_data)