from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException


class HanscomExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class HanscomDateExtractor(DateExtractor):

    EXCEPTION = HanscomExtractorException
    DATE_FORMAT = '%m-%d-%y'
    SEARCH_TEXT = 'ACCT#  1'
    END_TEXT = 'PREVIOUS BALANCE'
    MATCH_TEXT = (
        'DATETRANSACTION DESCRIPTIONAMOUNTFINANCECHARGEBALANCEMEMBER '
        'NO.ENDING DATEBRANCH')
    FILE_FORMAT = '{:02}-{:02}-Hanscom.pdf'

    @staticmethod
    def match(text):
        return (HanscomDateExtractor.MATCH_TEXT in text)

    def extract(self, text):

        start_date = None
        end_date = None

        start = 0
        while True:
            start = text.find(self.__class__.SEARCH_TEXT, start + 1)

            self.__handle_search_failure__(start < 0)

            start += len(self.__class__.SEARCH_TEXT)
            end = text.find(self.__class__.END_TEXT, start + 1)

            try:
                parts = text[start:end].split('THRU')

                start_date = datetime.strptime(
                    parts[0].strip(), self.__class__.DATE_FORMAT)

                end_date = datetime.strptime(
                    parts[1].strip(), self.__class__.DATE_FORMAT)
                break

            except ValueError:
                print(
                    "ValueError at index: [{}:{}] - [{}]"
                    .format(start, end, text[start:end]))
                pass

        return ExtractedData(start_date, end_date)
