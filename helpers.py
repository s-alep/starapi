import requests
import json

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
        return { "Error Message", "Error fetching Character data"}
    
    try:
        response = requests.get(FILM_EP)
        response.raise_for_status() 
        film_data = response.json()
    except requests.exceptions.RequestException as e:
        return { "Error Message", "Error fetching Film data."}
    
    try:
        response = requests.get(STARSHIP_EP)
        response.raise_for_status() 
        starsh_data = response.json()
    except requests.exceptions.RequestException as e:
        return { "Error Message", "Error fetching Starship data."}
    return char_data, film_data, starsh_data 

def mockerinos():
    film_data = None
    character_data = None
    starsh_data = None

    with open('json/films.json', 'r') as f:
        film_data = json.load(f)
    with open('json/characters.json', 'r') as f:
        character_data = json.load(f)
    with open('json/starships.json', 'r') as f:
        starsh_data = json.load(f)

    return character_data, film_data, starsh_data
