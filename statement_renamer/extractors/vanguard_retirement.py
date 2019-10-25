"""
    ACCOUNT SUMMARY: 07/01/2018 - 09/30/2018AMAZON.COM 401(K) PLAN
    RETIREMENT PLAN STATEMENTAccount BalanceYour Account ProgressYour Retirement Income Outlook
    Retirement Income*Connect with Vanguard®Total Account Balance:
>800-523-1188  >vanguard.com*
"""

from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException


class VanguardRetirementExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class VanguardRetirementDateExtractor(DateExtractor):

    EXCEPTION = VanguardRetirementExtractorException
    DATE_FORMAT = '%m/%d/%Y'
    SEARCH_TEXT = 'ACCOUNT SUMMARY: '
    END_TEXT = 'AMAZON.COM 401(K) PLAN'
    FILE_FORMAT = '{:2}-Q{} Vanguard Retirement Statement.pdf'

    PRE_DATE_TEXT = 'ACCOUNT SUMMARY: '
    POST_DATE_TEXT = 'AMAZON.COM 401(K) PLAN'
    SPLIT_TEXT = ' - '

    @staticmethod
    def match(text):
        return 'RETIREMENT PLAN STATEMENTAccount BalanceYour Account Progress' in text

    def extract(self, text):
        return self._pre_post_split_extraction_(text)

    def rename(self, extracted_data):
        return self._rename_using_quarter_(extracted_data)
