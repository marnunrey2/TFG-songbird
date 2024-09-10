import requests

### Paso 2. Access token
client_id = "Amazon client id"
client_secret = (
    "Amazon client secret"
)

url = "https://api.amazon.com/auth/o2/token"

redirect_uri = "https://api.music.amazon.dev/"
# MODIFY THE CODE
code = "ANNsypoiFVnHFcDtdxUW"

grant_type = "authorization_code"
data = {
    "grant_type": grant_type,
    "code": code,
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}
response = requests.post(url, data=data, headers=headers)

access_token = response.json().get("access_token")
refresh_token = response.json().get("refresh_token")
expires_in = response.json().get("expires_in")
print(access_token)
print(refresh_token)
print(expires_in)
