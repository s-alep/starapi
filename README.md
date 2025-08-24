# Starapi

## Building Instructions
- Use python > 3.12

- Setup Virtual Environment
  - uvloop does not support windows yet. If on windows use WSL.

  - `sudo apt install python3`
  - `cd /path/to/starapi`
  - `python3 -m venv  .venv`
  - `source .venv/bin/activate`

- Install requirements
 - `pip install -r requirements.txt`

## Running

- Run the program
`fastapi run main.py`
- first run the **/import_swapi_data endpoint** to fetch and store the data from SWAPI
- visit the **/docs** to see the available routes

