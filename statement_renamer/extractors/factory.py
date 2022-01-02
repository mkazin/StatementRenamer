""" Abstract Factory for DateExtractors """
from .extractor import DateExtractor, NoMatchingExtractor
import logging

class ExtractorFactory(object):
    """
    Returns an instance of the first class inheriting from DateExtractor which returns true to
    matching the provided text.

    To those who are unfamiliar with more advanced software design, the Abstract Factory pattern
    allows for automatic handling of any number of derrived classes, without needing to add
    significant class-specific code for each extractor implementated.

    Futher reading at: https://en.wikipedia.org/wiki/Abstract_factory_pattern or your copy of the
    mentioned "Gang Of Four" Design Patterns book.
    """

    @staticmethod
    def get_matching_extractor(text):
        """ Return the first DateExtractor which can handle the provided text. """

        # Optimize: subclasses should be used once. Once an extractor is found,
        #           it should be the first one checked, likely reducing text search time.

        # Implementation note: the "extractor" variable here is the current extractor ***class***
        # being tested for a match. At the return statement it is followed with parentheses to
        # instantiate an object of that class.
        # It's a neat little trick of Python, as is the __subclasses__ getter, which works thanks
        # to the code in extractors/__init__.py .
        # --mkazin
        # log = logging.getLogger('StatementRenamer')
        for extractor in DateExtractor.__subclasses__():
            # log.debug('Testing extractor: {%s} on {%s}', extractor, text)
            if extractor.match(text):
                return extractor()

        raise NoMatchingExtractor('No matching extractor found.')
