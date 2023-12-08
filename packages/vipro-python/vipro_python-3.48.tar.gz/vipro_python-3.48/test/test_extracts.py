# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

from vipro_python.core.extracts import csv_skip_rows

tests = {

  "standard": {
    "expected": 0,
    "delimiter": ",",
    "input": """Current Claim Number,Full Name,Date of Birth,NI Number,Full Property Address,Finance Item Code,Finance Item Description
00000111,Mr Tom Thumb,12/07/1984,JA111222A,"10, Cyber Way, Richmond, Essex, AA10 3AB",CB,child benefit"""
  },

  "tendring": {
    "expected": 3,
    "delimiter": ",",
    "input": """,,,,,,
,Report Title,,,,,
,,,,,,
Current Claim Number,Full Name,Date of Birth,NI Number,Full Property Address,Finance Item Code,Finance Item Description
00000111,Mr Tom Thumb,12/07/1984,JA111222A,"10, Cyber Way, Richmond, Essex, AA10 3AB",CB,child benefit""",
  },

}

def test_skip_rows():
  for named in tests:
    tt = tests[named]
    got = csv_skip_rows(tt['input'], tt['delimiter'])
    expected = tt['expected']
    assert got == expected, f"{named}: csv_skip_rows() expected={expected}, got={got}"
