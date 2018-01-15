from datetime import datetime


class DateFormatter(object):

    def format(self, date):
        return datetime.strftime(date, '%Y-%m')
