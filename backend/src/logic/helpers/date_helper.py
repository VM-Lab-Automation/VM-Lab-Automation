from datetime import datetime

ISO_format = '%Y-%m-%dT%H:%M:%S.%fZ'


class DateHelper:

    @staticmethod
    def date_to_ISO_string(date: datetime):
        return date.strftime(ISO_format)

    @staticmethod
    def datetime_from_ISO_string(date: str):
        return datetime.strptime(date, ISO_format)
