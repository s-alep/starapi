from sqlmodel import SQLModel,  Field, Relationship
from datetime import datetime
from typing import Optional, List

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
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    height: int = Field(index=True)
    mass: int = Field(index=True)
    hair_colour: str = Field(index=True)
    eye_colour : str = Field(index=True)
    birth_year : str = Field(index=True)
    gender : str = Field(index=True)
    starships: List["Starship"] = Relationship(back_populates="characters", link_model=CharacterStarshipLink)
    films: List["Film"] = Relationship(back_populates="characters", link_model=CharacterFilmLink)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Film(SQLModel, table=True):
    __tablename__ = 'film'
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    opening_crawl: str = Field(index=True)
    director: str = Field(index=True)
    producer: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    characters: List[Character] = Relationship(back_populates="films", link_model=CharacterFilmLink)
    starships: List["Starship"] = Relationship(back_populates="films", link_model=StarshipFilmLink)

class Starship(SQLModel, table=True):
    __tablename__ = 'starship'
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    model: str = Field(index=True)
    manufacturer: str = Field(index=True)
    cost_in_credits: int = Field(index=True)
    length: int = Field(index=True)
    max_atmosphering_speed : int = Field(index=True)
    crew: str = Field(index=True)
    passengers : int = Field(index=True)
    cargo_capacity : int = Field(index=True)
    consumables: int = Field(index=True)
    hyperdrive_rating: int = Field(index=True)
    mglt: int = Field(index=True)
    starship_class: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    characters: List[Character] = Relationship(back_populates="starships", link_model=CharacterStarshipLink)
    films: List[Film] = Relationship(back_populates="starships", link_model=StarshipFilmLink)
