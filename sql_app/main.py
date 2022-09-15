from itertools import groupby
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from starlette.responses import RedirectResponse
from fastapi_crudrouter import SQLAlchemyCRUDRouter as CRUDRouter


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/docs/")


@app.get("/races_per_year/")
def get_races_per_year(db: Session=Depends(get_db)):
    q = db.query(models.Race.year, func.count(models.Race.id)).group_by(models.Race.year).order_by(func.count(models.Race.id))
    return q


@app.get("/drivers_first_places/")
def get_drivers_first_places(db: Session=Depends(get_db)):
    sq = db.query(models.Qualifying.driver_id).filter(models.Qualifying.position==1).group_by(models.Qualifying.driver_id).add_columns(func.count(models.Qualifying.driver_id).label('first_places')).subquery()
    q = db.query(models.Driver.id, models.Driver.name, sq.c.first_places).join(sq, models.Driver.id == sq.c.driver_id).order_by(sq.c.first_places.desc()).all()
    return q


@app.get("/races_per_circuit/")
def get_races_per_circuit(db: Session=Depends(get_db)):
    # Nombre del circuito más corrido
    sq = db.query(models.Race.circuit_id)\
        .group_by(models.Race.circuit_id)\
        .add_columns(func.count(models.Race.circuit_id).label('races_count'))\
        .subquery()
    q = db.query(models.Circuit.id, models.Circuit.name, sq.c.races_count)\
        .join(sq, models.Circuit.id == sq.c.circuit_id)\
        .order_by(sq.c.races_count.desc())\
        .all()
    return q


@app.get("/drivers_points/")
def get_drivers_points(db: Session=Depends(get_db)):
    # Piloto con mayor cantidad de puntos en total, cuyo constructor 
    # sea de nacionalidad sea American o British
    sq1 = db.query(models.Constructor)\
        .filter(models.Constructor.nationality.in_(['American', 'British']))\
        .subquery()
    sq2 = db.query(models.Result, sq1).join(sq1, models.Result.constructor_id == sq1.c.id)\
        .group_by(models.Result.driver_id)\
        .add_columns(func.sum(models.Result.points).label('points_total'))\
        .subquery()
    q = db.query(models.Driver.name, sq2.c.points_total)\
        .join(sq2, models.Driver.id == sq2.c.driver_id)\
        .order_by(sq2.c.points_total.desc())\
        .all()
    return q


# Routes for Circuit model
app.include_router(CRUDRouter(
    schema = schemas.Circuit,
    db_model = models.Circuit,
    db = get_db,
    prefix = 'circuits'
))

# Routes for Constructor model
app.include_router(CRUDRouter(
    schema = schemas.Constructor,
    db_model = models.Constructor,
    db = get_db,
    prefix = 'constructors'
))

# Routes for Driver model
app.include_router(CRUDRouter(
    schema = schemas.Driver,
    db_model = models.Driver,
    db = get_db,
    prefix = 'drivers'
))

# Routes for LapTime model
app.include_router(CRUDRouter(
    schema = schemas.LapTime,
    db_model = models.LapTime,
    db = get_db,
    prefix = 'lap_times'
))

# Routes for PitStop model
app.include_router(CRUDRouter(
    schema = schemas.PitStop,
    db_model = models.PitStop,
    db = get_db,
    prefix = 'pit_stops'
))

# Routes for Qualifying model
app.include_router(CRUDRouter(
    schema = schemas.Qualifying,
    db_model = models.Qualifying,
    db = get_db,
    prefix = 'qualifyings'
))

# Routes for Race model
app.include_router(CRUDRouter(
    schema = schemas.Race,
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = True,
    db_model = models.Race,
    db = get_db,
    prefix = 'races'
))

# Routes for Result model
app.include_router(CRUDRouter(
    schema = schemas.Result,
    db_model = models.Result,
    db = get_db,
    prefix = 'results'
))