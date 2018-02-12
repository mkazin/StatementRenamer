from datetime import datetime
from .extractor import DateExtractor, ExtractorException


class AscensusExtractorException(ExtractorException):

    def __init__(self, *args, **kwargs):
        ExtractorException.__init__(self, *args, **kwargs)


class AscensusDateExtractor(DateExtractor):

    DATE_FORMAT = '%m/%d/%y'

    @staticmethod
    def match(text):
        return 'Visit us at https://www.planservices.com/' in text

    def extract(self, text):

        data = {}
        data['start_date'] = None
        data['end_date'] = None

        start = 0
        while True:
            # Search for the first numerical date following "period"
            start = text.find("period", start + 1)

            if start < 0:
                raise AscensusExtractorException(
                    type(self).__name__ + ': Expected text not found')

            try:
                int(text[start + 7])
                parts = text[start + 7:].strip().split(' ')
                data['start_date'] = datetime.strptime(
                    parts[0], AscensusDateExtractor.DATE_FORMAT)
                data['end_date'] = datetime.strptime(
                    parts[2], AscensusDateExtractor.DATE_FORMAT)
                break
            # except NumberError:
            #     print("ValueError at index: {}".format(start))
            except ValueError:
                # print("ValueError at index: {}".format(start))
                pass

        return data
