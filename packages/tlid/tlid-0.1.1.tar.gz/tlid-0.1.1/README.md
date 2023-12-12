# tlid

## Installation

```sh
pip install tlid
```

## Usage:
```python

import tlid

# Get TLID
tlid_str = tlid.get_tlid()
print(tlid_str)  # Outputs: YYMMDDHHMMSS

# Get TLID with milliseconds
tlid_milli = tlid.get_milliseconds()
print(tlid_milli)  # Outputs: YYMMDDHHMMSSmmm

# Get TLID for different time granularities
print(tlid.get_seconds())  # Outputs: YYMMDDHHMMSS
print(tlid.get_minutes())  # Outputs: YYMMDDHHMM
print(tlid.get_hour())     # Outputs: YYMMDDHH
print(tlid.get_day())      # Outputs: YYMMDD
print(tlid.get_month())    # Outputs: YYMM
print(tlid.get_year())     # Outputs: YY

# Check if a string has a TLID
print(tlid.has_tlid('Hello 210101010101 World'))  # Outputs: True

# Extract TLID from a string
print(tlid.extract_tlid('Hello 210101010101 World'))  # Outputs: 210101010101

# Clean a string from its TLID
print(tlid.clean_tlid('Hello 210101010101 World'))  # Outputs: Hello World

# Convert a TLID string to a datetime object
print(tlid.to_date('210101010101'))  # Outputs: 2021-01-01 01:01:01

```

