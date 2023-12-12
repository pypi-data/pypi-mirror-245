# tlid.py

from datetime import datetime

def get_tlid():
    return datetime.now().strftime("%y%m%d%H%M%S")

def get_milliseconds():
    return datetime.now().strftime("%y%m%d%H%M%S%f")[:-3]

def get_seconds():
    return get_tlid()

def get_minutes():
    return datetime.now().strftime("%y%m%d%H%M")

def get_hour():
    return datetime.now().strftime("%y%m%d%H")

def get_day():
    return datetime.now().strftime("%y%m%d")

def get_month():
    return datetime.now().strftime("%y%m")

def get_year():
    return datetime.now().strftime("%y")

def extract_tlid(string):
    digits = ''.join(filter(str.isdigit, string))
    return digits if len(digits) in (12, 15) else None

def has_tlid(string):
    return extract_tlid(string) is not None

def clean_tlid(string):
    tlid = extract_tlid(string)
    return string.replace(tlid, '').strip() if tlid else string

def to_date(tlid_str):
    if len(tlid_str) == 12:
        return datetime.strptime(tlid_str, "%y%m%d%H%M%S")
    elif len(tlid_str) == 15:
        return datetime.strptime(tlid_str, "%y%m%d%H%M%S%f")
    else:
        raise ValueError("Invalid TLID string length.")