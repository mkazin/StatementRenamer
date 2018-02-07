
from .ascensus import AscensusDateExtractor
from .capitolone360 import CapitolOne360DateExtractor
from .exceptions import ExtractorException
from .vanguard import VanguardDateExtractor

extractors = [
    AscensusDateExtractor,
    CapitolOne360DateExtractor,
    VanguardDateExtractor
]


class ExtractorFactory(object):

    @staticmethod
    def get_matching_extractor(text):

        for extractor in extractors:
            if extractor.match(text):
                return extractor()

        raise ExtractorException('No matching extractor found.')
