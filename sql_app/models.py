from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base


class Circuit(Base):
    __tablename__ = 'circuits'

    id = Column(Integer, primary_key=True)
    ref = Column(String, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    alt = Column(Integer, nullable=False)
    url = Column(String, nullable=False)

    race = relationship('Race', back_populates='circuits')


class Constructor(Base):
    __tablename__ = 'constructors'

    id = Column(Integer, primary_key=True)
    ref = Column(String)
    name = Column(String)
    nationality = Column(String)
    url = Column(String)

    result = relationship('Result', back_populates='constructors')


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

    pit_stop = relationship('PitStop', back_populates='drivers')
    result = relationship('Result', back_populates='drivers')


class PitStop(Base):
    __tablename__ = 'pit_stops'

    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    stop = Column(Integer)
    lap = Column(Integer)
    time = Column(String)
    duration = Column(Float)
    milliseconds = Column(Integer)

    driver = relationship('Driver', back_populates='pit_stops')


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

    circuit = relationship('Circuit', back_populates='races')
    result = relationship('Result', back_populates='races')


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
    positionOrder = Column(Integer)
    points = Column(Integer)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)
    fastestLap = Column(Integer)
    rank = Column(Integer)
    fastestLapTime = Column(Float)
    fastestLapSpeed = Column(Float)
    statusId = Column(Integer)
    
    race = relationship('Race', back_populates='results')
    driver = relationship('Driver', back_populates='results')
    constructor = relationship('Constructor', back_populates='results')