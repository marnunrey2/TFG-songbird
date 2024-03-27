import requests

### Paso 1. Authorization code

client_id = "amzn1.application-oa2-client.7c0d83cb1c9d4f048bfa5e9b4f390806"
client_secret = (
    "amzn1.oa2-cs.v1.9287a294bb74d3afd078534e40484585d191601050eacaa08709598335ea5012"
)
auth_url = "https://www.amazon.com/ap/oa"

scope = "profile"
response_type = "code"
redirect_uri = "https://api.music.amazon.dev/"
data = {
    "client_id": client_id,
    "scope": scope,
    "response_type": response_type,
    "redirect_uri": redirect_uri,
}
response = requests.get(auth_url, data=data)

print(auth_url + "?" + response.request.body)
# https://www.amazon.com/ap/oa?client_id=amzn1.application-oa2-client.7c0d83cb1c9d4f048bfa5e9b4f390806&scope=profile&response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2F
# Insert url in navigator, login with amazon credentials and copy the code
