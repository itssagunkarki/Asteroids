import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

nasa_api_key = os.environ.get('NASA_API_KEY')

def _call_api(url: str, timeout:int = 500) -> dict:
    with requests.Session() as session:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()

    return response


class NasaData():
    def get_data_of_timerange(self, start_date: str, end_date: str) -> json:
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={nasa_api_key}"

        data = _call_api(url)

        return data.json()