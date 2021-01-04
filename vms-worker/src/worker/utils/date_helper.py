import datetime

ISO_format = '%Y-%m-%dT%H:%M:%S.%fZ'


def parse_date(datetimestr):
    return datetime.datetime.strptime(datetimestr, ISO_format)


def stringify_date(date: datetime):
    return date.strftime(ISO_format) if date is not None else None
