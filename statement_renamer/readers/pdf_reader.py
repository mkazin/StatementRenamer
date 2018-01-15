import io
from pdfminer import high_level
from .reader import Reader


class PdfReader(Reader):

    def parse(self, fname):
        """ Assumes the input file [fname] is small enough to read in its entirety\
            into memory.  This should be fixed to use a temporary file otherwise. """

        outfp = io.StringIO()
        with open(fname, "rb") as fp:
            high_level.extract_text_to_fp(fp, **locals())

        outfp.seek(0)
        contents = outfp.read()

        return contents
