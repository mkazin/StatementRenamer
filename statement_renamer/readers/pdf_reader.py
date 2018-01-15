import io
from pdfminer import high_level, pdfdocument
from .reader import Reader
from .reader import ReaderException


class PdfReader(Reader):

    def parse(self, fname):
        """ Assumes the input file [fname] is small enough to read in its entirety\
            into memory.  This should be fixed to use a temporary file otherwise. """

        outfp = io.StringIO()
        with open(fname, "rb") as fp:

            try:
                high_level.extract_text_to_fp(fp, **locals())
            except pdfdocument.PDFTextExtractionNotAllowed as e:
                raise ReaderException(e)

        outfp.seek(0)
        contents = outfp.read()

        return contents
