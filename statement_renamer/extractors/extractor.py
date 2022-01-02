""" This module provides the basic structure for extracting data from files. """
import abc
from datetime import datetime


class ExtractorException(Exception):
    """ Base class for exceptions during date extraction """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class NoMatchingExtractor(ExtractorException):
    """ Exception denoting no matching extractor was found for a single file. """
    def __init__(self, *args, **kwargs):
        super.__init_subclass__()


class DateExtractor(metaclass=abc.ABCMeta):
    """
    Abstract base class providing abstract and utility functions for extracting data from text

    I'm tried to make it as painless as possible to implement an DateExtractor.

    Complete the following steps:

    1) Decide on a naming convention. If you use month and year, you may simply define FILE_FORMAT
    on your class, which will be used within the default rename() implementation, which takes two
    parameters: first the year and then the month.
    Alternatively, you should override rename().

    To output quarter rather than month (e.g. "2020-Q3 - Quarterly Statement.pdf"), you use
    _rename_using_quarter_() to have the integer corresponding to the quarter passed as the second
    parameter (year starts in January, one-indexed)

    2) Implement the abstract match() method.

    3) Date extraction from documents containing a date range can sometimes be done using a
    simple algorithm of searching for text before and after the dates of interest and looking
    on either side of a delimiter. To use this built-in functionality, you must define the
    following on your class:
        PRE_DATE_TEXT - text appearing just before the start date
        POST_DATE_TEXT = text appearing just after the end date
        SPLIT_TEXT = text between start end end dates
        DATE_FORMAT = the format of the dates

    I highly recommend using a Test-Driven-Development approach:
    * Use the --extract-only flag to extract the text to see what your extractor will.
    * Clone an existing unit test and paste key snippets of that extracted text (removing any
      private data, obviously)
    * Perform a rename on the extractor name- I've tried to make this part painless
    """
    EXCEPTION = ExtractorException
    PRE_DATE_TEXT = None
    POST_DATE_TEXT = None
    SPLIT_TEXT = None
    DATE_FORMAT = None
    FILE_FORMAT = None

    @staticmethod
    @abc.abstractmethod
    def match(text):
        """ Return true if the extractor can handle the provided text.
        """

    @abc.abstractmethod
    def extract(self, text):
        """ Extract data from the provided text.
            Return class is ExtractedData, used in rename()
        """

    def rename(self, extracted_data):
        """
            Return a string with a new name for the file.
            Defaults to using month and year.
        """
        return self._rename_using_month_(extracted_data)

    def __handle_search_failure__(self, condition):
        if condition:
            raise self.__class__.EXCEPTION(
                type(self).__name__ + ': Expected text not found')

    def _pre_post_split_extraction_(self, text):
        """
            Pre-defined extraction method using:
            * Two strings to locate the date range
            * A split value to separate start from end dates
        """
        start = text.find(self.PRE_DATE_TEXT) + len(self.PRE_DATE_TEXT)
        end = text.find(self.__class__.POST_DATE_TEXT)

        extracted = text[start:end].split(self.SPLIT_TEXT)

        self.__handle_search_failure__(len(extracted) < 2)

        start_date = datetime.strptime(extracted[0], self.DATE_FORMAT)
        end_date = datetime.strptime(extracted[1], self.DATE_FORMAT)
        return ExtractedData(start_date, end_date)

    def _rename_using_month_(self, extracted_data):
        """
            Pre-defined rename method using an extractor class' FILE_FORMAT string as the string,
            having parameter #0 as the year and parameter #1 as the month.
        """
        return self.__class__.FILE_FORMAT.format(
            extracted_data.get_end_date().year,
            extracted_data.get_end_date().month)

    def _rename_using_quarter_(self, extracted_data):
        """
            Pre-defined rename method using an extractor class' FILE_FORMAT string as the string,
            having parameter #0 as the year and parameter #1 as the quarter.
        """
        return self.__class__.FILE_FORMAT.format(
            extracted_data.get_end_date().year,
            extracted_data.get_end_date().month // 3)


class ExtractedData():
    """ Data object for the data found in the text passed to a DateExtractor """
    def __init__(self, start_date, end_date):
        self.data = {}
        self.data['start_date'] = start_date
        self.data['end_date'] = end_date

    def get_start_date(self):
        """ Getter for start date """
        return self.data['start_date']

    def get_end_date(self):
        """ Getter for end date """
        return self.data['end_date']

    def set_hash(self, file_hash):
        self.data['hash'] = file_hash

    def get_hash(self):
        return self.data['hash']

    def set_source(self, source_path):
        self.data['source_path'] = source_path

    def get_source(self):
        return self.data['source_path']

    def set_field(self, field_name, value):
        self.data[field_name] = value

    def get_field(self, field_name):
        return self.data[field_name]

    def __repr__(self):
        return '(ExtractedData:: {} - {})'.format(
            self.get_start_date(),
            self.get_end_date())
