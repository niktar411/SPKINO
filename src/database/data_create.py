import requests
import src.database.model

def get_movie_info_omdb(api_key: str, title: str = None, imdb_id: str = None, plot: str = "full") -> dict:

    base_url = "http://www.omdbapi.com/"
    params = {
        "apikey": api_key,
        "plot": plot,
        "r": "json"
    }

    if title:
        params["t"] = title
    if imdb_id:
        params["i"] = imdb_id

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return {}

    data = response.json()
    if data.get("Response") == "False":
        print(f"Ошибка API: {data.get('Error')}")
        return {}

    return data

def create_movie(IMDB_ID: str, API_KEY = '20580e65'):
    data_get = get_movie_info_omdb(api_key=API_KEY, imdb_id=IMDB_ID)
    if data_get:
        return data_get
    else:
        print("film not found")