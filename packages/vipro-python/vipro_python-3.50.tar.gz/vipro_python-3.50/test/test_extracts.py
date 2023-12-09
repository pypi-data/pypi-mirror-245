# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

from vipro_python.core.extracts import csv_skip_rows, read_extract

# TODO: remove all local excel tests when not on dev machine
# def test_read_local_excel_xls():
#   df = read_extract(r'/Users/work/Desktop/pan-essex-nov2023/full-extract-drop/basildon/HousingRegister_20230901.xls')
#   assert df is not None
#   assert len(df) > 10
#   print(f"columns {df.columns}")

# def test_read_local_excel_xlsx():
#   df = read_extract(r'/Users/work/Desktop/pan-essex-nov2023/full-extract-drop/braintree/Data Matching for Benefits Sep 2023.xlsx')
#   assert df is not None
#   assert len(df) > 10
#   print(f"columns {df.columns}")


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
