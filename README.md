# Starapi

## Building Instructions
- Use python 3.13.7

- Install sqlite
  - For windows comes with python installation
  - For mac `brew install sqlite`
  - For linux `sudo apt install sqlite`

- Setup Virtual Environment
  - python venv -m .venv
    - For windows ./.venv/Scripts/activate
    - For bash source .venv/bin/activate

- Install requirements
 - pip install -r requirements.txt

## Running 

- Run the program 
`fastapi run main.py`
- first run the **/import_swapi_data endpoint** to fetch and store the data from SWAPI
- visit the **/docs** to see the available routes 
