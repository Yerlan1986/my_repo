import requests
from movie.movie_data import secret_keys

BASE_URL = 'http://www.omdbapi.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0',
    'accept': '*/*'
}


def get_movie(data: str) -> dict:

    data = data.replace(' ', '+')
    URL = f"{BASE_URL}"+f"?t={data}&apikey={secret_keys.APIKEY}&"
    responce = requests.get(url=URL, headers=headers).json()

    return responce



