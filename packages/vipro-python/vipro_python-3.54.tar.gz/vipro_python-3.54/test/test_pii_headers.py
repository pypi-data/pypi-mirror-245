# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

import pandas as pd
from vipro_python.lacf.pii_headers import extract_postcode_from_address, extract_postcode_from_address_series

def test_extract_pcode():
  addr, pcode = extract_postcode_from_address('10 Cyber Road_x000D_Colchester_x000D_CO4 5NF')
  assert pcode == 'CO4 5NF'
  assert addr == '10 Cyber Road_x000D_Colchester_x000D_'

def test_extract_pcode_series():
  s = pd.Series(data=['10 Cyber Road_x000D_Colchester_x000D_CO4 5NF'], index=['address_1'])
  a, p = extract_postcode_from_address_series(s)
  s['address_1'] = a
  s['postcode'] = p
  assert s['postcode'] == 'CO4 5NF'
  assert s['address_1'] == '10 Cyber Road_x000D_Colchester_x000D_'