#!/usr/bin/env python
# tlidcli.py

import argparse
import sys
from . import (get_minutes, get_hour, get_seconds, get_milliseconds,
                  get_month, get_year, get_day)

def main():
        
  # Create the parser
  parser = argparse.ArgumentParser(description='TLID CLI - Generate time-based identifiers.')
  
  # Add arguments
  parser.add_argument('unit', nargs='?', default='minutes',
                      choices=['h', 's', 'ms', 'm', 'M', 'y', 'd'],
                      help='Select the unit of time for TLID generation (default: minutes).')
  
  # Parse the arguments
  args = parser.parse_args()
  
  # Get the TLID based on the selected unit
  if args.unit == 'h':
      print(get_hour())
  elif args.unit == 's':
      print(get_seconds())
  elif args.unit == 'ms':
      print(get_milliseconds())
  elif args.unit == 'm' or args.unit == 'M':
      print(get_month())
  elif args.unit == 'y':
      print(get_year())
  elif args.unit == 'd':
      print(get_day())
  else:
      print(get_minutes())
      
      
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()