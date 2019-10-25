from datetime import datetime
from .extractor import DateExtractor, ExtractedData, ExtractorException


class AscensusExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class AscensusDateExtractor(DateExtractor):

    DATE_FORMAT = '%m/%d/%y'
    FILE_FORMAT = '{0}-Q{1}-AcensusQuarterly.pdf'

    @staticmethod
    def match(text):
        return 'Visit us at https://www.planservices.com/' in text

    def extract(self, text):

        start_date = None
        end_date = None

        start = 0
        while True:
            # Search for the first numerical date following "period"
            start = text.find("period", start + 1)

            self.__handle_search_failure__(start < 0)

            try:
                int(text[start + 7])
                parts = text[start + 7:].strip().split(' ')
                start_date = datetime.strptime(
                    parts[0], AscensusDateExtractor.DATE_FORMAT)
                end_date = datetime.strptime(
                    parts[2], AscensusDateExtractor.DATE_FORMAT)
                break
            # except NumberError:
            #     print("ValueError at index: {}".format(start))
            except ValueError:
                # print("ValueError at index: {}".format(start))
                pass

        return ExtractedData(start_date, end_date)

    def rename(self, extracted_data):
        return self._rename_using_quarter_(extracted_data)
