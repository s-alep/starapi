from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Character
from helpers import get_data_from_swapi, mockerinos
import gunicorn

app = FastAPI(title='STARAPI')

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "This is STARAPI"}

@app.get('/import_swapi_data')
def import_swapi_data():
    # character_data, film_data, starsh_data = get_data_from_swapi()
    character_data, film_data, starsh_data = mockerinos()
    return [character_data, film_data, starsh_data]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
