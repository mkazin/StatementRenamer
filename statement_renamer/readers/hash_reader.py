""" Hash reader for files on disk """
import hashlib
from .reader import Reader, ReaderException


class HashReader(Reader):
    """ Primary class """

    CHUNK_SIZE = 8192

    def parse(self, fname):
        """ Reads the provided file from disk in chunks and returns an MD5 hash its content """

        try:
            hasher = hashlib.sha256()

            with open(fname, "rb") as fp:

                chunk = fp.read(HashReader.CHUNK_SIZE)
                while chunk:
                    hasher.update(chunk)
                    chunk = fp.read(HashReader.CHUNK_SIZE)

            return hasher.hexdigest()
        except Exception as ex:
            raise ReaderException(ex)
