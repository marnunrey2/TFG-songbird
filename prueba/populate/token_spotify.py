import spotipy
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

print(access_token)
# Obtenemos los datos de la aplicación
#CLIENT_ID = "25c561e06c384a0c8a24901dc80f8114"
#CLIENT_SECRET = "f7e84ccb68384876a6b3264eb3d74d77"
#REDIRECT_URI = "https://developer.spotify.com/dashboard"
#
#credentials = spotipy.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
#spotipy.SpotifyClientCredentials()
#
## Creamos el cliente de Spotify
#sp = spotipy.Spotify(client_credentials_manager=)
#    
#
## Obtenemos el token de acceso
#auth_url = sp.auth_url(scope="user-read-private")
#print(auth_url)