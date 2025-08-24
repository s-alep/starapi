from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class CharacterStarshipLink(SQLModel, table=True):
    __tablename__ = "character_starship_link"
    character_id: Optional[int] = Field(default=None, foreign_key="character.id", primary_key=True)
    starship_id: Optional[int] = Field(default=None, foreign_key="starship.id", primary_key=True)

class CharacterFilmLink(SQLModel, table=True):
    __tablename__ = "character_film_link"
    character_id: Optional[int] = Field(default=None, foreign_key="character.id", primary_key=True)
    film_id: Optional[int] = Field(default=None, foreign_key="film.id", primary_key=True)

class StarshipFilmLink(SQLModel, table=True):
    __tablename__ = "starship_film_link"
    starship_id: Optional[int] = Field(default=None, foreign_key="starship.id", primary_key=True)
    film_id: Optional[int] = Field(default=None, foreign_key="film.id", primary_key=True)

class Character(SQLModel, table=True):
    __tablename__ = 'character'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    height: str = Field(index=True)
    mass: str = Field(index=True)
    hair_color: str = Field(index=True)
    eye_color : str = Field(index=True)
    birth_year : str = Field(index=True)
    gender : str = Field(index=True)
    swapi_id :int = Field(index=True)
    starships: List["Starship"] = Relationship(back_populates="characters", link_model=CharacterStarshipLink)
    films: List["Film"] = Relationship(back_populates="characters", link_model=CharacterFilmLink)
    created: datetime | None = Field(default_factory=datetime.utcnow)

class Film(SQLModel, table=True):
    __tablename__ = 'film'
    id: int | None= Field(default=None, primary_key=True)
    title: str = Field(index=True)
    episode_id : int = Field(index=True)
    opening_crawl: str = Field(index=True)
    director: str = Field(index=True)
    producer: str = Field(index=True)
    release_date: str = Field(index=True)
    swapi_id :int = Field(index=True)
    created: datetime | None = Field(default_factory=datetime.utcnow)
    characters: List[Character] = Relationship(back_populates="films", link_model=CharacterFilmLink)
    starships: List["Starship"] = Relationship(back_populates="films", link_model=StarshipFilmLink)

class Starship(SQLModel, table=True):
    __tablename__ = 'starship'
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    model: str = Field(index=True)
    manufacturer: str = Field(index=True)
    cost_in_credits: str = Field(index=True)
    length: str = Field(index=True)
    max_atmosphering_speed : str = Field(index=True)
    crew: str = Field(index=True)
    passengers : str = Field(index=True)
    cargo_capacity : str = Field(index=True)
    consumables: str = Field(index=True)
    hyperdrive_rating: str = Field(index=True)
    MGLT: str = Field(index=True)
    starship_class: str = Field(index=True)
    swapi_id :int = Field(index=True)
    created: datetime = Field(default_factory=datetime.utcnow)
    characters: List[Character] = Relationship(back_populates="starships", link_model=CharacterStarshipLink)
    films: List[Film] = Relationship(back_populates="starships", link_model=StarshipFilmLink)

# Simplified nested models (used when these objects appear as nested relationships)
class CharacterNested(BaseModel):
    id: int
    name: str

class FilmNested(BaseModel):
    id: int
    title: str

class StarshipNested(BaseModel):
    id: int
    name: str

# Full models for main API responses (with nested relationships)
class CharacterRead(BaseModel):
    id: int
    name: str
    height: str
    mass: str
    hair_color: str
    eye_color: str
    birth_year: str
    gender: str
    starships: List[StarshipNested] = []
    films: List[FilmNested] = []

class FilmRead(BaseModel):
    id: int
    title: str
    episode_id: int
    director: str
    producer: str
    release_date: str
    opening_crawl: str
    starships: List[StarshipNested] = []
    characters: List[CharacterNested] = []

class StarshipRead(BaseModel):
    id: int
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: str
    MGLT: str
    starship_class: str
    films: List[FilmNested] = []
    characters: List[CharacterNested] = []

