""" MD5 hash reader for files on disk """
import hashlib
from .reader import Reader, ReaderException


class Md5Reader(Reader):
    """ Primary class """

    CHUNK_SIZE = 8192

    def parse(self, fname):
        """ Reads the provided file from disk in chunks and returns an MD5 hash its content """

        try:
            md5 = hashlib.md5()

            with open(fname, "rb") as fp:

                chunk = fp.read(Md5Reader.CHUNK_SIZE)
                while chunk:
                    md5.update(chunk)
                    chunk = fp.read(Md5Reader.CHUNK_SIZE)

            return md5.hexdigest()
        except Exception as ex:
            raise ReaderException(ex)
