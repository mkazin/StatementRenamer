import abc
from datetime import datetime


class DateExtractor(metaclass=abc.ABCMeta):

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


class ExtractedData(object):

    def __init__(self, start_date, end_date):
        self.data = {}
        self.data['start_date'] = start_date
        self.data['end_date'] = end_date

    def get_start_date(self):
        return self.data['start_date']

    def get_end_date(self):
        return self.data['end_date']

    def set_hash(self, hash):
        self.data['hash'] = hash

    def get_hash(self):
        return self.data['hash']

    def set_source(self, source_path):
        self.data['source_path'] = source_path

    def get_source(self):
        return self.data['source_path']

    def __repr__(self):
        return '(ExtractedData:: {} - {})'.format(
            self.get_start_date(),
            self.get_end_date())


class ExtractorException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
