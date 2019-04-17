from datetime import datetime, timedelta


class DateUtil(object):

    """
    Handy utility function courtesy of Augusto Men of StackOverflow:
    https://stackoverflow.com/questions/42950/get-last-day-of-the-month-in-python
    """
    @staticmethod
    def last_day_of_month(any_day):
        next_month = any_day.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)
