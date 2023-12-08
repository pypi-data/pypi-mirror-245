import requests

class Service:
  def __init__(self, location: str, version: str, auth_instance: str, host: str = 'https://apis.vipro.online'):
    self.location = location
    self.version = version
    self.auth_instance = auth_instance
    self.host = host

  def ep(self, named: str, parts: list):
    return f"{self.host}/{self.location}/{named}/v/{self.version}/" + '/'.join(parts)

  def authority_token_endpoint(self):
    return AuthorityTokenEP(self.ep('authority', ['instances', self.auth_instance, 'auth', 'token']))


class AuthorityTokenEP:
  def __init__(self, token_url: str):
    self.token_url = token_url



class ClientCredentials:
  def __init__(self, auth: AuthorityTokenEP, client_id: str, client_secret: str):
    self.auth = auth
    self.client_id = client_id
    self.client_secret = client_secret

  def get_token(self, audience: str, scope: str):
    res = requests.post(self.auth.token_url, {
      'grant_type': 'client_credentials',
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'audience': audience,
      'scope': scope,
    })
    if res.status_code != 200:
      raise Exception(f"response: {res.status_code}: {res.text}")
    return res.json()
