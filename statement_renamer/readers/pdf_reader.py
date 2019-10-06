import io
from pdfminer import high_level, pdfdocument, pdfparser
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
            except pdfparser.PDFSyntaxError as e:
                raise ReaderException(e)

        outfp.seek(0)
        contents = outfp.read()

        return PdfReader._replace_cids_(contents)

    """ 
        Decodes text encoded in ASCII values
        For example you'll see this in E*Trade:
        (cid:67)(cid:65)(cid:83)(cid:72)(cid:32)(cid:38)(cid:32)(cid:67)(cid:65)(cid:83)(cid:72)(cid:32)(cid:69)
        (cid:81)(cid:85)(cid:73)(cid:86)(cid:65)(cid:76)(cid:69)(cid:78)(cid:84)(cid:83)
    """
    @staticmethod
    def _replace_cids_(contents):
        replacement = contents
        start = replacement.find('(cid:')
        while start >= 0:
            end = replacement.find(')', start+1)
            value = int(replacement[start+5:end])
            replacement = replacement[:start] + chr(value) + replacement[end+1:]
            start = replacement.find('(cid:', start + 1)
        return replacement
