# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

# determine 1st line of the address
from vipro_python.ai.models.addressnet import AddressModel

def test_enc_addr_str():
  model = AddressModel(None, None, None, None)
  res = model.enc_addr('16 Benson Drive, RG77 3TT')
  assert res == '16BENSONDRIVE|RG773TT'

def test_enc_addr_list():
  model = AddressModel(None, None, None, None)
  res = model.enc_addr(['16 Benson Drive', 'RG77 3TT'])
  assert res == '16BENSONDRIVE|RG773TT'
