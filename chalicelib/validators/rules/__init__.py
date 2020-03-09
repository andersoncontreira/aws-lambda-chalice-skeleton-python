import datetime

from dateutil.parser import parser, isoparse


class DateTimeRule:
    def __init__(self, str_date, iso_format=True):
        self.str_date = str_date
        self.format = '%Y-%M-%DT%H:%M:%S'
        self.iso_format = iso_format

    def validate(self):
        """
        :exception: Exception
        :return:
        """
        try:
            if self.iso_format:
                isoparse(self.str_date)
            else:
                date_parser = parser()
                date_parser.parse(self.str_date, None)
        except Exception as err:
            raise Exception('Invalid date format', err)
        return True