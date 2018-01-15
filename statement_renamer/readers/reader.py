from .reader_exception import ReaderException


class Reader(object):
    """ Abstract class serving as a framework for renaming files using
        a run-time injected class and required configuration 
        raises ReaderException on any error in reading file."""

    # def __init__(self):
    #     self.input = input
    #     self.metadata = metadata

    def parse(self, fname):
        raise ReaderException('Use concrete Reader implementation')
