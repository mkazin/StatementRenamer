import abc


class DateExtractor(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def match(text):
        """ Return true if the extractor can handle the provided text.
        """

    @abc.abstractmethod
    def extract(self, text):
        """ Extract data from the provided text.
        """


class ExtractorException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
