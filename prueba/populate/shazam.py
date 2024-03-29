import requests


def shazam_api():

    url = "https://shazam.p.rapidapi.com/shazam-songs/get-details"

    querystring = {"id": "40333609", "locale": "en-US"}

    headers = {
        "X-RapidAPI-Key": "f878f743a2mshfbe080de1a87735p1cc141jsn9d3de2ceb655",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
