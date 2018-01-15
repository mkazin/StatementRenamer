from datetime import datetime


class AscensusDateExtractor(object):  # DateExtractor

    DATE_FORMAT = '%m/%d/%y'

    def extract(self, text):

        data = {}
        data['start_date'] = None
        data['end_date'] = None

        start = 0
        while True:
            # Search for the first numerical date following "period"
            start = text.find("period", start + 1)

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
                print("ValueError at index: {}".format(start))

        return data
