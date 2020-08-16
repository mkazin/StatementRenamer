import hashlib
from .reader import Reader, ReaderException


class Md5Reader(Reader):
    """ MD5 hash reader for small files """
    def parse(self, fname):
        '''
        Assumes the input file [fname] is small enough to read in its entirety\
        into memory.  This should be fixed to use a temporary file otherwise.
        '''

        try:
            md5 = hashlib.md5()

            with open(fname, "rb") as fp:
                md5.update(fp.read())

            return md5.hexdigest()
        except Exception as ex:
            raise ReaderException(ex)
