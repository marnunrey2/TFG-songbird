import requests

### Paso 2. Access token
client_id = "amzn1.application-oa2-client.7c0d83cb1c9d4f048bfa5e9b4f390806"
client_secret = (
    "amzn1.oa2-cs.v1.9287a294bb74d3afd078534e40484585d191601050eacaa08709598335ea5012"
)

url = "https://api.amazon.com/auth/o2/token"

redirect_uri = "https://api.music.amazon.dev/"
code = "ANoZJJUUjclIzkCdkfzw"
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
