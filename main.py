from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Character, Film, Starship, CharacterRead, FilmRead, StarshipRead
from helpers import get_mock_data, get_data_from_swapi, process_char, process_ship, process_film
import uvicorn
from sqlalchemy.orm import selectinload
from typing import List, Annotated, cast

app = FastAPI(title='STARAPI')

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "This is STARAPI"}

model_mapping = {
    'character': Character,
    'film': Film,
    'starship': Starship,
}

@app.get("/characters/search/{name}", response_model=List[CharacterRead])
def search_characters_by_name(
    name: str,
    session: Session = Depends(get_session)
):
    statement = (
        select(Character)
        .where(Character.name.ilike(f"%{name}%")) # type: ignore
        .options(selectinload(Character.starships), selectinload(Character.films)) # type: ignore
    )
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No character found matching '{name}'.")
    return results

@app.get("/films/search/{name}", response_model=List[FilmRead])
def search_films_by_name(
    name: str,
    session: Session = Depends(get_session)
):
    statement = (
        select(Film)
        .where(Film.title.ilike(f"%-{name}%")) # type: ignore
        .options(selectinload(Film.characters), selectinload(Film.starships)) # type: ignore
    )
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No film found matching '{name}'.")
    return results

@app.get("/starships/search/{name}", response_model=List[StarshipRead])
def search_starships_by_name(
    name: str,
    session: Session = Depends(get_session)
):
    statement = (
        select(Starship)
        .where(Starship.name.ilike(f"%{name}%")) # type: ignore
        .options(selectinload(Starship.characters), selectinload(Starship.films)) # type: ignore
    )
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No starship found matching '{name}'.")
    return results

@app.get('/characters/', response_model=List[CharacterRead])
def get_characters(offset: int = 0, limit: Annotated[int, Query(le=100)] = 5, session: Session = Depends(get_session)):
   if offset < 0 or limit < 0:
        raise HTTPException(status_code=404, detail="Limit and Offset can not be negative number")
   statement = (
        select(Character)
        .offset(offset)
        .limit(limit)
        .options(selectinload(Character.starships), selectinload(Character.films)) # type: ignore
    )
   results = session.exec(statement).unique().all()
   if not results:
        raise HTTPException(status_code=404, detail="No characters found.")
   return results

@app.get('/films/', response_model=List[FilmRead])
def get_films(offset: int = 0, limit: Annotated[int, Query(le=100)] = 5, session: Session = Depends(get_session)):
   if offset < 0 or limit < 0:
        raise HTTPException(status_code=404, detail="Limit and Offset can not be negative number")
   statement = (
        select(Film)
        .offset(offset)
        .limit(limit)
        .options(selectinload(Film.characters), selectinload(Film.starships)) # type: ignore
    )
   results = session.exec(statement).unique().all()
   if not results:
        raise HTTPException(status_code=404, detail="No films found.")
   return results

@app.get('/starships/', response_model=List[StarshipRead])
def get_starships(offset: int = 0, limit: Annotated[int, Query(le=100)] = 5, session: Session = Depends(get_session)):

   if offset < 0 or limit < 0:
        raise HTTPException(status_code=404, detail="Limit and Offset can not be negative number")
   statement = (
        select(Starship)
        .offset(offset)
        .limit(limit)
        .options(selectinload(Starship.characters), selectinload(Starship.films)) # type: ignore
    )
   results = session.exec(statement).unique().all()
   if not results:
        raise HTTPException(status_code=404, detail="No starships found.")
   return results

@app.get('/import_swapi_data')
def import_swapi_data(session: Session = Depends(get_session)):
    character_data, film_data, ship_data, error_message = get_data_from_swapi()
    # character_data, film_data, ship_data, error_message = get_mock_data()
    if error_message:
        raise HTTPException(status_code=500, detail=error_message)
    characters = []
    character_links = {}
    if character_data:
        for character in character_data:
            char_dict, links= process_char(character)
            new_char = Character(**char_dict)
            session.add(new_char)
            session.commit()
            characters.append(new_char)
            character_links[new_char.swapi_id] = links

    ships = []
    ship_links = {}
    if ship_data:
        for ship in ship_data:
            ship_dict, links= process_ship(ship)
            new_ship = Starship(**ship_dict)
            session.add(new_ship)
            session.commit()
            ships.append(new_ship)
            ship_links[new_ship.swapi_id] = links

    films = []
    film_links = {}
    if film_data:
        for film in film_data:
            film_dict, links= process_film(film)
            new_film = Film(**film_dict)
            session.add(new_film)
            session.commit()
            films.append(new_film)
            film_links[new_film.swapi_id] = links

    for film in films:
        links = film_links[film.swapi_id]

        char_swapi_ids: List[int] = cast(List[int], links.get('characters', []))
        statement = select(Character).where(Character.swapi_id.in_(char_swapi_ids)) # type: ignore
        film_char_links = session.scalars(statement).all()

        ship_swapi_ids: List[int] = cast(List[int], links.get('starships', []))
        statement = select(Starship).where(Starship.swapi_id.in_(ship_swapi_ids)) # type: ignore
        film_ship_links = session.scalars(statement).all()

        statement = select(Film).where(Film.swapi_id == film.swapi_id)
        film = session.scalars(statement).first()
        if not film:
            continue
        ship_list :List[Starship] = list(film_ship_links)
        char_list :List[Character] = list(film_char_links)
        film.starships.extend(ship_list)
        film.characters.extend(char_list)
        session.add(film)
        session.commit()
    for ship in ships:
        links = ship_links[ship.swapi_id]

        char_swapi_ids: List[int] = cast(List[int], links.get('characters', []))
        statement = select(Character).where(Character.swapi_id.in_(char_swapi_ids)) # type: ignore
        ship_char_links = session.scalars(statement).all()

        statement = select(Starship).where(Starship.swapi_id == ship.swapi_id)
        ship = session.scalars(statement).first()
        if not ship:
            continue
        char_list :List[Character] = list(ship_char_links)
        ship.characters.extend(char_list)
        session.add(ship)
        session.commit()

    return {"message" : "Swapi data imported succesfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
