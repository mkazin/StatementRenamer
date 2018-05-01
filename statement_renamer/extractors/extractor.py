import abc


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

    @abc.abstractmethod
    def rename(self, extracted_data):
        """ Return a string with a new name for the file.
        """


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
