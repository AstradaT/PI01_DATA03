from sqlalchemy.orm import Session
from . import models, schemas


def get_race(db: Session, race_id: int):
    return db.query(models.Race).filter(models.Race.id == race_id).first()


#def get_races_per_year(db: Session):
    #return db.query(models.Race.year, func.count(models.Race.id).label('count_id')).group_by(models.Race.year)
    #.query(models.Race).group_by(models.Race.year)