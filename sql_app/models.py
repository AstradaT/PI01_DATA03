# This file contains the SQLAlchemy models for the database
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base


class Circuit(Base):
    __tablename__ = 'circuits'

    id = Column(Integer, primary_key=True)
    ref = Column(String)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(Float)
    long = Column(Float)
    alt = Column(Integer)
    url = Column(String)

    races = relationship('Race', backref='circuit')


class Constructor(Base):
    __tablename__ = 'constructors'

    id = Column(Integer, primary_key=True)
    ref = Column(String)
    name = Column(String)
    nationality = Column(String)
    url = Column(String)

    results = relationship('Result', backref='constructor')


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True)
    ref = Column(String)
    number = Column(Integer)
    code = Column(String)
    name = Column(String)
    forename = Column(String)
    surname = Column(String)
    dob = Column(String)
    nationality = Column(String)
    url = Column(String)

    qualifyings = relationship('Qualifying', backref='driver')


class LapTime(Base):
    __tablename__ = 'lap_times'

    ix = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('races.id'))
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    lap = Column(Integer)
    position = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)


class PitStop(Base):
    __tablename__ = 'pit_stops'

    ix = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('races.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    stop = Column(Integer)
    lap = Column(Integer)
    time = Column(String)
    duration = Column(Float)
    milliseconds = Column(Integer)


class Qualifying(Base):
    __tablename__ = 'qualifyings'

    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('races.id'))
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    constructor_id = Column(Integer, ForeignKey('constructors.id'))
    number = Column(Integer)
    position = Column(Integer)
    q1 = Column(String)
    q2 = Column(String)
    q3 = Column(String)


class Race(Base):
    __tablename__ = 'races'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    circuit_id = Column(Integer, ForeignKey('circuits.id'), nullable=False)
    name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String)
    url = Column(String, nullable=False)

    qualifyings = relationship('Qualifying', backref='race')


class Result(Base):
    __tablename__ = 'results'

    result_id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('races.id'))
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    constructor_id = Column(Integer, ForeignKey('constructors.id'))
    number = Column(Integer)
    grid = Column(Integer)
    position = Column(Integer)
    position_text = Column(Integer)
    position_order = Column(Integer)
    points = Column(Integer)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)
    fastest_lap = Column(Integer)
    rank = Column(Integer)
    fastest_lap_time = Column(Float)
    fastest_lap_speed = Column(Float)
    status_id = Column(Integer)
    