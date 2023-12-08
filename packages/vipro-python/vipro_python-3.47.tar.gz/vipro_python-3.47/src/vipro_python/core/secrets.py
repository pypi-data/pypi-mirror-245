from google.cloud import secretmanager

def read_secret(gcp_project: str, auth_instance: str, secret_name: str, version: str = 'latest', encoding: str = 'UTF-8'):
  uri = f"projects/{gcp_project}/secrets/{auth_instance}-{secret_name}/versions/{version}"
  client = secretmanager.SecretManagerServiceClient()
  response = client.access_secret_version(request={"name": uri})
  data = response.payload.data
  if encoding is None:
    return data
  return data.decode(encoding)
