"""
    AsteroidData
"""
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

class AsteroidData():
    """
    returns asteroid data from NASA or predownloaded data
    """
    def __init__(self, start_date='0000-00-00', end_date='0000-00-00') -> None:
        self.start_date = start_date
        self.end_date = end_date

    def get_data_from_nasa(self, save_to_file: bool = False) -> json:
        """
        Gets data of all asteroids near Earth between `start_date` and `end_date`
        """

        nasa_api_key = os.environ['NASA_API_KEY']

        response = requests.get(
            url=f"https://api.nasa.gov/neo/rest/v1/feed?start_date={self.start_date}&end_date={self.end_date}&api_key={nasa_api_key}",
            timeout=1000
            )
        
        data = response.json()
        data['links'] = None #Avoid exposing API Keys

        if save_to_file:
            self._save_to_json("../assets/json/nasa_json.json", data)

        return data
    

    def _save_to_json(self, json_datafile: str, json_data: json):
        #  Write the JSON data to the file
        with open(json_datafile, 'w', encoding="UTF8") as json_file:
            json.dump(json_data, json_file, indent=4)


    def _get_local_data(self, filepath: str) -> json:
        """
        returns pre downloaded json data that was created in previous run of the program
        """
        with open(filepath, 'r', encoding="UTF8") as file:
            data = json.load(file)

        return data
    