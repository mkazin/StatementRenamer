
from .extractor import DateExtractor, ExtractorException


class ExtractorFactory(object):
    """ AbstractDataFactory for DateExtractors """

    @staticmethod
    def get_matching_extractor(text):
        """ Return the first DateExtractor which can handle the provided text. """

        for extractor in DateExtractor.__subclasses__():
            if extractor.match(text):
                return extractor()

        raise ExtractorException('No matching extractor found.')
