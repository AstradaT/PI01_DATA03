from itertools import groupby
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func, desc
from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from starlette.responses import RedirectResponse
from fastapi_crudrouter import SQLAlchemyCRUDRouter as CRUDRouter


# Crea las tablas en formulaone.db presentes en models.py
models.Base.metadata.create_all(bind=engine)


description = """
#### Esta API fue creada para consultar la base de datos [Formula 1 World Championship (1950 - 2022)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)🏎🏆.

## Tablas
**circuits**: circuitos en donde se corrieron las carreras<br>
**constructors**: constructores<br>
**drivers**: conductores<br>
**lap_times**: tiempos de vueltas<br>
**pit_stops**: paradas en boxes<br>
**qualifyings**: calificaciones<br>
**races**: carreras<br>
**results**: resultados<br>

## Ejemplo de Uso

**/tabla/** - Leer todas las filas de la tabla.<br>
**/tabla/id** - Leer una sola fila de la tabla.<br>
**/tabla?skip=50&limit=400** - Saltar 50 filas y limitar el resultado a 400 filas.

##### Por defecto, las URLs para **lap_times**, **pit_stops** y **results** devuelven 1000 resultados. Cambia el valor con el parametro **limit=** o pasa a la siguiente página con **skip=**.
Copyright 2022 Tomás Astrada
"""

app = FastAPI(
    title = "Formula 1 World Championship API",
    description = description,
    contact = {
        "name": "Tomás Astrada",
        "url": "https://github.com/AstradaT",
        "email": "tomasastrada907@gmail.com"
    },
    license_info = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0"
    }
)


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


# Año con más carreras
@app.get("/query1/")
def get_query1(db: Session=Depends(get_db)):
    q = db.query(models.Race.year, func.count(models.Race.id).label('races_count'))\
        .group_by(models.Race.year)\
        .order_by(desc('races_count'))\
        .first()
    return q['year']


# Piloto con mayor cantidad de primeros puestos
@app.get("/query2/")
def get_query1(db: Session=Depends(get_db)):
    sq = db.query(models.Qualifying.driver_id)\
        .filter(models.Qualifying.position==1)\
        .group_by(models.Qualifying.driver_id)\
        .add_columns(func.count(models.Qualifying.driver_id).label('first_places'))\
        .subquery()
    q = db.query(models.Driver.id, models.Driver.name, sq.c.first_places)\
        .join(sq, models.Driver.id == sq.c.driver_id)\
        .order_by(sq.c.first_places.desc())\
        .first()
    return q['name']


# Nombre del circuito más corrido
@app.get("/query3/")
def get_query1(db: Session=Depends(get_db)):
    sq = db.query(models.Race.circuit_id)\
        .group_by(models.Race.circuit_id)\
        .add_columns(func.count(models.Race.circuit_id).label('races_count'))\
        .subquery()
    q = db.query(models.Circuit.id, models.Circuit.name, sq.c.races_count)\
        .join(sq, models.Circuit.id == sq.c.circuit_id)\
        .order_by(sq.c.races_count.desc())\
        .first()
    return q['name']


# Piloto con mayor cantidad de puntos en total, cuyo constructor sea de 
# nacionalidad American o British
@app.get("/query4/")
def get_query1(db: Session=Depends(get_db)):
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
        .first()
    return q['name']


@app.get("/races_per_year/")
def get_races_per_year(db: Session=Depends(get_db)):
    # Año con más carreras
    q = db.query(models.Race.year, func.count(models.Race.id).label('races_count'))\
        .group_by(models.Race.year)\
        .order_by(desc('races_count'))\
        .all()
    return q


@app.get("/drivers_first_places/")
def get_drivers_first_places(db: Session=Depends(get_db)):
    # Devuelve diccionario con cada conductor y su cantidad de primeros puestos
    sq = db.query(models.Qualifying.driver_id)\
        .filter(models.Qualifying.position==1)\
        .group_by(models.Qualifying.driver_id)\
        .add_columns(func.count(models.Qualifying.driver_id).label('first_places'))\
        .subquery()
    q = db.query(models.Driver.id, models.Driver.name, sq.c.first_places)\
        .join(sq, models.Driver.id == sq.c.driver_id)\
        .order_by(sq.c.first_places.desc())\
        .all()
    return q


@app.get("/races_per_circuit/")
def get_races_per_circuit(db: Session=Depends(get_db)):
    # Devuelve circuitos y las carreras corridas en cada uno
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
    # Devuelve pilotos cuyos constructores sean American o British junto a sus puntos 
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
    prefix = 'circuits',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))

# Routes for Constructor model
app.include_router(CRUDRouter(
    schema = schemas.Constructor,
    db_model = models.Constructor,
    db = get_db,
    prefix = 'constructors',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))

# Routes for Driver model
app.include_router(CRUDRouter(
    schema = schemas.Driver,
    db_model = models.Driver,
    db = get_db,
    prefix = 'drivers',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))

# Routes for LapTime model
app.include_router(CRUDRouter(
    schema = schemas.LapTime,
    db_model = models.LapTime,
    db = get_db,
    paginate = 1000,
    prefix = 'lap_times',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))

# Routes for PitStop model
app.include_router(CRUDRouter(
    schema = schemas.PitStop,
    db_model = models.PitStop,
    db = get_db,
    paginate = 1000,
    prefix = 'pit_stops',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))

# Routes for Qualifying model
app.include_router(CRUDRouter(
    schema = schemas.Qualifying,
    db_model = models.Qualifying,
    db = get_db,
    paginate = 1000,
    prefix = 'qualifyings',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))

# Routes for Race model
app.include_router(CRUDRouter(
    schema = schemas.Race,
    db_model = models.Race,
    db = get_db,
    prefix = 'races',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))

# Routes for Result model
app.include_router(CRUDRouter(
    schema = schemas.Result,
    db_model = models.Result,
    db = get_db,
    paginate = 1000, 
    prefix = 'results',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
))