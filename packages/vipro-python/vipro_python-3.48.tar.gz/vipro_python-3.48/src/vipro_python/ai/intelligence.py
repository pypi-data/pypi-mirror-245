import requests
import json

class IntelligenceService:
  def __init__(self, service, token):
    self.token = token
    self.service = service

  def execute(self, named: str, message: str):
    """ call into the intelligence api """
    endpoint = self.service.ep('intelligence', ['chatgpt', 'assignments', named, 'execute'])
    payload = { 'message': message }
    res = requests.post(endpoint, data=json.dumps(payload), headers={
      'Authorization': f"{self.token['token_type']} {self.token['access_token']}"
    })
    if res.status_code != 200:
      raise Exception(f"Status: {res.status_code}: {res.text}")
    return res.json()
