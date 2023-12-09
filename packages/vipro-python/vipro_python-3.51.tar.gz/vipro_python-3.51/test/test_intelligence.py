# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

# import json
# import os
from vipro_python.core.oauth2 import Service #, ClientCredentials
# from vipro_python.ai.intelligence import IntelligenceService

def test_service():
  ep = Service('usa', '123', 'foobar', 'https://example.org').authority_token_endpoint().token_url
  assert ep == 'https://example.org/usa/authority/v/123/instances/foobar/auth/token'

# def test_intelligence():
#   # acquire
#   client_id = os.environ.get('CLIENT_ID')
#   client_secret = os.environ.get('CLIENT_SECRET')
#   auth_instance = os.environ.get('AUTH_INSTANCE')
#   assert client_id != None
#   assert client_secret != None
#   assert auth_instance != None
#   london = Service('london', '20230811', auth_instance)
#   credentials = ClientCredentials(london.authority_token_endpoint(), client_id, client_secret)
#   token = credentials.get_token('intelligence', 'openid profile intelligence')
#   api = IntelligenceService(london, token)
#   # act
#   response = api.execute('pii-headers', 'addr1,pcost,forename,lname')
#   # assert
#   assert 'response' in response
#   assert len(response['response']) > 0
#   map = json.loads(response['response'][0]['message']['content'])
#   assert 'addr1' in map
#   assert 'pcost' in map
#   assert 'forename' in map
#   assert 'lname' in map
#   assert map['addr1'] == 'address_line_1'
