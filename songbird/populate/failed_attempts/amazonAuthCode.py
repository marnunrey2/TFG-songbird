import requests

### Paso 1. Authorization code

client_id = "Amazon client id"
client_secret = (
    "Amazon client secret"
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
# Insert url in navigator, login with amazon credentials and copy the code
