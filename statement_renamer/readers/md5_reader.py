import hashlib
from .reader import Reader, ReaderException


class Md5Reader(Reader):

    def parse(self, fname):
        """ Assumes the input file [fname] is small enough to read in its entirety\
            into memory.  This should be fixed to use a temporary file otherwise. """

        try:
            m = hashlib.md5()

            with open(fname, "rb") as fp:
                m.update(fp.read())

            return m.hexdigest()
        except Exception as e:
            raise ReaderException(e)
