"""Create an initial token for testing"""
from datameta_client import api_version
import requests
import os

# get env variables:
url = os.getenv("DATAMETA_URL")
email = os.getenv("DATAMETA_INITIAL_EMAIL")
password = os.getenv("DATAMETA_INITIAL_PASS")


# get key from datameta-app:
request = {
    "email": email,
    "password": password,
    "label": "init_token"
}
response = requests.post(
    f"{url}/api/{api_version}/keys",
    json=request
)
assert response.status_code == 200

# store token in env variable:
token = response.json()["token"]
os.environ["DATAMETA_TOKEN"] = token
print(token)
