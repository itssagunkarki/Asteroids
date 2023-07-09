import json
from dotenv import load_dotenv


load_dotenv()

# class AsteroidData:
#     def __init__(self, start_date: str = '0000-00-00', end_date: str = '0000-00-00', nasa_api_key: Optional[str] = None) -> None:
#         self.start_date = start_date
#         self.end_date = end_date
#         self.asteroid_data = None
#         self.nasa_api_key = nasa_api_key or os.environ.get('NASA_API_KEY')

#     def get_data_from_nasa(self, save_to_file: bool = False) -> dict:
#         url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={self.start_date}&end_date={self.end_date}&api_key={self.nasa_api_key}"

#         with requests.Session() as session:
#             response = session.get(url, timeout=1000)
#             response.raise_for_status()

#             data = response.json()
#             data['links'] = None  # Avoid exposing API Keys

#         if save_to_file:
#             json_datafile = self._get_data_file_path()
#             self._save_to_json(json_datafile, data)

#         self.asteroid_data = data
#         return data

#     def _save_to_json(self, json_datafile: Path, json_data: dict) -> None:
#         with json_datafile.open('w', encoding="UTF8") as json_file:
#             json.dump(json_data, json_file, indent=4)

#     def _get_local_data(self, filepath: Path) -> dict:
#         with filepath.open('r', encoding="UTF8") as file:
#             data = json.load(file)

#         return data

#     def get_list_all_asteroids(self) -> List[dict]:
#         if self.asteroid_data is None:
#             self.get_data_from_nasa()

#         asteroids = []
#         data = self.asteroid_data

#         for date_key in data['near_earth_objects'].keys():
#             for asteroid_data in data['near_earth_objects'][date_key]:
#                 asteroid = {
#                     "Neo Reference ID": asteroid_data['neo_reference_id'],
#                     "Name": asteroid_data['name'],
#                     "Potentially Hazardous": asteroid_data['is_potentially_hazardous_asteroid'],
#                     "Close Approach Date": asteroid_data['close_approach_data'][0]['close_approach_date_full'],
#                     "Sentry Object": asteroid_data['is_sentry_object']
#                 }
#                 asteroids.append(asteroid)

#         df = pd.DataFrame(asteroids)
#         json_data = df.to_dict(orient='records')
#         return json_data


    

from asteroids.nasa import NasaData

class AsteroidData():
    def __init__(self, start_date: str = '0000-00-00', end_date: str = '0000-00-00') -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.asteroid_data = None
        self.get_data_from_nasa()
    
    def get_data_from_nasa(self) -> json:
        if self.asteroid_data is not None:
            return self.asteroid_data
        
        nasa = NasaData()
        data = nasa.get_data_of_timerange(self.start_date, self.end_date)
        self.asteroid_data = data
        return data

    def get_num_asteroids(self) -> int:
        if self.asteroid_data is None:
            self._get_data_from_nasa()

        data = self.asteroid_data
        return data['element_count']
    


