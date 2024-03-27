import requests

client_id = '25c561e06c384a0c8a24901dc80f8114'
client_secret = 'f7e84ccb68384876a6b3264eb3d74d77'
auth_url = 'https://accounts.spotify.com/api/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}

auth_response = requests.post(auth_url, data=data)
access_token = auth_response.json().get('access_token')

# URL base de la API de Spotify
BASE_URL = "https://api.spotify.com/v1"

# Cabeceras (headers) necesarias para la solicitud
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"

}

# Endpoint al que deseas hacer la solicitud (por ejemplo, obtener información de un artista)
track_id = "11dFghVXANMlKmJXsNCbNl"
endpoint = f"{BASE_URL}/tracks/{track_id}"

# Realizar la solicitud GET a la API de Spotify
response = requests.get(endpoint, headers=headers)

# Verificar el estado de la respuesta
if response.status_code == 200:
    # La solicitud fue exitosa
    artist_info = response.json()
    # Aquí puedes procesar la información obtenida del artista
    print(artist_info)
else:
    # La solicitud no fue exitosa
    print(f"Error al hacer la solicitud: {response.status_code} - {response.text}")
