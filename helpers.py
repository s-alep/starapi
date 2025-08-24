import requests
import json
import logging

SERVER_URL = 'localhost:8000'

def get_data_from_swapi():
    CHARACTER_EP = "https://swapi.info/api/people"
    FILM_EP = "https://swapi.info/api/films"
    STARSHIP_EP = "https://swapi.info/api/starships"
    film_data = None
    char_data = None
    starsh_data = None
    try:
        response = requests.get(CHARACTER_EP)
        response.raise_for_status()
        char_data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching character data from SWAPI: {e}")
        return None, None, None, f"Error fetching character data from SWAPI: {e}"

    try:
        response = requests.get(FILM_EP)
        response.raise_for_status()
        film_data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching film data from SWAPI: {e}")
        return None, None, None, f"Error fetching film data from SWAPI: {e}"

    try:
        response = requests.get(STARSHIP_EP)
        response.raise_for_status()
        starsh_data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching starship data from SWAPI: {e}")
        return None, None, None, f"Error fetching starship data from SWAPI: {e}"
    return char_data, film_data, starsh_data, None



def get_mock_data():
    film_data = None
    character_data = None
    starsh_data = None

    try:
        with open('json/films.json', 'r') as f:
            film_data = json.load(f)
    except FileNotFoundError:
        logging.error("Mock data file 'json/films.json' not found.")
        return None, None, None, "Mock data file 'json/films.json' not found."
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from 'json/films.json': {e}")
        return None, None, None, f"Error decoding JSON from 'json/films.json': {e}"

    try:
        with open('json/characters.json', 'r') as f:
            character_data = json.load(f)
    except FileNotFoundError:
        logging.error("Mock data file 'json/characters.json' not found.")
        return None, None, None, "Mock data file 'json/characters.json' not found."
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from 'json/characters.json': {e}")
        return None, None, None, f"Error decoding JSON from 'json/characters.json': {e}"

    try:
        with open('json/starships.json', 'r') as f:
            starsh_data = json.load(f)
    except FileNotFoundError:
        logging.error("Mock data file 'json/starships.json' not found.")
        return None, None, None, "Mock data file 'json/starships.json' not found."
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from 'json/starships.json': {e}")
        return None, None, None, f"Error decoding JSON from 'json/starships.json': {e}"

    return character_data, film_data, starsh_data, None

def process_char(data : dict ) :
    data.pop('homeworld', None)
    data.pop('species', None)
    data.pop('vehicles', None)
    data.pop('created', None)
    data.pop('edited', None)

    url = data.pop('url', None)
    swapi_id = 0
    if url:
        swapi_id = url.split('/')[-1]
    data['swapi_id'] = swapi_id

    links = { 'films' : [], 'starships' : []}
    ships = data['starships']
    ship_ids = []
    for ship in ships:
        ship_id= int(ship.split('/')[-1])
        ship_ids.append(ship_id)
    links['starships'] = ship_ids
    data['starships'] = []

    films = data['films']
    film_ids = []
    for film in films:
        film_id = int(film.split('/')[-1])
        film_ids.append(film_id)
    links['films'] = film_ids
    data['films'] = []

    return data, links

def process_ship(data:dict):
    links = { 'films' : [], 'characters' : []}
    data.pop('created', None)
    data.pop('edited', None)
    url = data.pop('url', None)
    swapi_id = 0
    if url:
        swapi_id = url.split('/')[-1]
    data['swapi_id'] = swapi_id

    pilots = data['pilots']
    pilot_ids = []
    for pilot in pilots:
        pilot_id= int(pilot.split('/')[-1])
        pilot_ids.append(pilot_id)
    links['characters'] = pilot_ids
    data['pilots'] = []

    films = data['films']
    film_ids = []
    for film in films:
        film_id = int(film.split('/')[-1])
        film_ids.append(film_id)
    links['films'] = film_ids
    data['films'] = []
    return data , links

def process_film(data:dict):
   data.pop('planets', None)
   data.pop('vehicles', None)
   data.pop('species', None)
   data.pop('created', None)
   data.pop('edited', None)

   links = { 'characters' : [], 'starships' : []}
   ships = data['starships']
   ship_ids = []
   for ship in ships:
       ship_id= int(ship.split('/')[-1])
       ship_ids.append(ship_id)
   links['starships'] = ship_ids
   data['starships'] = []
   characters = data['characters']
   char_ids = []
   for character in characters:
       char_id= int(character.split('/')[-1])
       char_ids.append(char_id)
   links['characters'] = char_ids
   data['characters'] = []

   url = data.pop('url', None)
   swapi_id = 0
   if url:
       swapi_id = url.split('/')[-1]
   data['swapi_id'] = swapi_id
   return data, links
