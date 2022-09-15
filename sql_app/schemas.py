# This file contains the Pydantic models
from pydantic import BaseModel


class Circuit(BaseModel):
    id: int
    ref: str
    name: str
    location: str
    country: str
    lat: float
    long: float
    alt: int
    url: str

    class Config:
        orm_mode = True


class Constructor(BaseModel):
    id: int
    ref: str
    name: str
    nationality: str
    url: str

    class Config:
        orm_mode = True


class Driver(BaseModel):
    id: int
    ref: str
    number: int | None
    code: str | None
    name: str
    forename: str
    surname: str
    dob: str
    nationality: str
    url: str

    class Config:
        orm_mode = True


class LapTime(BaseModel):
    ix: int
    race_id: int
    driver_id: int
    lap: int
    position: int
    time: str
    milliseconds: int

    class Config:
        orm_mode = True


class PitStop(BaseModel):
    ix: int
    race_id: int
    driver_id: int
    stop: int
    lap: int
    time: str
    duration: float
    milliseconds: int

    class Config:
        orm_mode = True


class Qualifying(BaseModel):
    id: int
    race_id: int
    driver_id: int
    constructor_id: int
    number: int
    position: int
    q1: str | None
    q2: str | None
    q3: str | None

    class Config:
        orm_mode = True


class Race(BaseModel):
    id: int
    year: int
    round: int
    circuit_id: int
    name: str
    date: str
    time: str
    url: str

    class Config:
        orm_mode = True


class Result(BaseModel):
    id: int
    race_id: int
    driver_id: int
    constructor_id: int
    number: int | None
    grid: int
    position: int | None
    position_text: str
    position_order: int
    points: int
    laps: int
    time: str | None
    milliseconds: int | None
    fastest_lap: int | None
    rank: int | None
    fastest_lap_time: str | None
    fastest_lap_speed: float | None
    status_id: int

    class Config:
        orm_mode = True