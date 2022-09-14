from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func
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
    races = db.query(models.Race.year, func.count(models.Race.id)).group_by(models.Race.year).order_by(func.count(models.Race.id))
    return races


#@app.get("/races/", response_model=list[schemas.Race])
#def read_races(db:Session=Depends(get_db)):
#    races = db.query(models.Race).all()
#    return races


#@app.get("/races/{race_id}", response_model=schemas.Race)
#def read_race(race_id: int, db: Session = Depends(get_db)):
#    db_race = crud.get_race(db, race_id=race_id)
#    if db_race is None:
#        raise HTTPException(status_code=404, detail="Race not found")
#    return db_race


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


"""
conexion = pymysql.connect (host='localhost', database='TP1', user ='root', password='xxxx#')

cursor = conexion.cursor()
cursor.execute(" SELECT year, count(year) as 'cantidad carreras corridas en el anio' FROM races GROUP BY year ORDER BY count(year) DESC LIMIT 1;  ")
for year in cursor:
    print ("Anio con mas carreras", year)

conexion.close()
"""