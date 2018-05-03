from datetime import datetime, timedelta
from .extractor import DateExtractor, ExtractedData, ExtractorException
import re
import sys


class RcnExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class RcnDateExtractor(DateExtractor):

    EXCEPTION = RcnExtractorException
    DATE_FORMAT = '%m/%d/%Y'
    # SEARCH_RE = r'(\d{2}/\d{2}/\d{4})'
    SEARCH_EXPRESSIONS = [
        r'Bill Date(\d{2}/\d{2}/\d{4})Due Date',
        r'Payment Due Date:(\d+/\d+/\d{4})',
        # r'(\d{2}/\d{2}-\d{2}/\d{2})',
        r'page \d+ of \d+(\d{2}/\d{2}/\d{4})']
    # r'(\d+/\d+/\d{4})']
    # SEARCH_RE = r'Bill Date(\d{2}/\d+/\d{4})'
    # SEARCH_RE = r'Payment Due Date:(\d+/\d+/\d{4})'
    FILE_FORMAT = '{:02}-{:02}-RCN.pdf'

    @staticmethod
    def match(text):
        return '1-800-RING-RCN' in text.replace('.', '-')


    def extract(self, text):
        start_date = None
        end_date = None

        
    def __old_extract__(self, text):

        start_date = None
        end_date = None
        # TODO: probably fails edge cases around year transition. Might need to
        # return the month as well to ensure years on start & end date are correct.
        # Those things are becoming a PITA.
        year = self.__extract_year__(text)

        # print('__extract_end_date__')
        p = re.compile(r'(\d{2})/(\d{2})\ ?-\ ?(\d{2})/(\d{2})')
        match = p.findall(text)[0]
        # print('Match: ', match)
        end_date = datetime(year, int(match[2]), int(match[3]))

        start_date = datetime(year, int(match[0]), int(match[1]))
        # print('returning', end_date)

        # for exp in self.__class__.SEARCH_EXPRESSIONS:
        #     p = re.compile(exp)
        #     print('\tTrying to match pattern: {}'.format(exp))
        #     matches = p.findall(text)
        #     print('Matches: ', matches)
        #     if len(matches) > 0:
        #         print('\tMatched!')
        #         break

        # if len(matches) == 0:
        #     raise self.__class__.EXCEPTION(
        #         type(self).__name__ + ': No matches found in text')

        # for curr_match in matches:

        #     try:
        #         end_date = datetime.strptime(
        #             curr_match, self.__class__.DATE_FORMAT)

        #         start_date = end_date.replace(day=1)

        #         break

        #     except ValueError:
        #         print("ValueError at curr_match: [{}]".format(curr_match))
        #         pass

        return ExtractedData(start_date, end_date)

    def __extract_year__(self, text):
        # print('__extract_year__')
        for exp in self.__class__.SEARCH_EXPRESSIONS:
            p = re.compile(exp)
            # print('\tTrying to match pattern: {}'.format(exp))
            matches = p.findall(text)
            # print('Matches: ', matches)
            if len(matches) > 0:
                # print('\tMatched!')
                break

        if len(matches) == 0:
            raise self.__class__.EXCEPTION(
                type(self).__name__ + ': No matches found in text')

        for curr_match in matches:
            # print('curr_match: ', curr_match)
            try:
                the_date = datetime.strptime(
                    curr_match, self.__class__.DATE_FORMAT)

                break

            except ValueError:
                print("ValueError at curr_match: [{}]".format(curr_match))
                pass

        # print('returning', the_date.year)
        return the_date.year

    def rename(self, extracted_data):

        # If the majority of the period falls was in the prior month,
        # rewind to the previous month's final day
        output_date = extracted_data.get_end_date()
        if output_date.day < (
                output_date - extracted_data.get_start_date()).days:
            output_date = output_date.replace(day=1) - timedelta(days=1)

        return self.__class__.FILE_FORMAT.format(
            output_date.year, output_date.month)


# Handy utility function courtesy of Augusto Men of StackOverflow:
# https://stackoverflow.com/questions/42950/get-last-day-of-the-month-in-python
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)
