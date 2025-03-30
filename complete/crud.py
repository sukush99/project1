""" SQLAlchemy CRUD operations for FastAPI """

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date

# mapping fo the models to the database
import models

# select top(1) * from player where player_id = {player_id}
def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()


# min_last_changed_date, multi query
def get_players(db: Session,
                skip: int = 0.,
                limit: int = 100,
                min_last_changed_date: date = None,
                last_name : str = None,
                first_name : str = None,):
    query = db.query(models.Player)
    if min_last_changed_date:
        query = query.filter(models.Player.last_changed_date >= min_last_changed_date)
    if last_name:
        query = query.filter(models.Player.last_name == last_name)
    if first_name:
        query = query.filter(models.Player.first_name == first_name)
    return query.offset(skip).limit(limit).all()

#get performance
def get_performances(db: Session,
                    skip: int = 0,
                    limit: int = 100,
                    min_last_changed_date: date = None,):
    query = db.query(models.Performance)
    if min_last_changed_date:
        query = query.filter(models.Performance.last_changed_date >= min_last_changed_date)
    return query.offset(skip).limit(limit).all()

#get league
def get_league(db: Session,
               league_id: int = None):
    return db.query(models.League).filter(models.League.league_id == league_id).first()


#get leagues
def get_leagues(db : Session,
                skip : int = 0,
                limit : int = 100,
                min_last_changed_date : date = None,
                league_name : int = None):
    query = db.query(models.League).options(joinedload(models.League.teams))
    if min_last_changed_date:
        query = query.filter(models.League.last_changed_date >= min_last_changed_date)
    if league_name:
        query = query.filter(models.League.league_name == league_name)
    return query.offset(skip).limit(limit).all()


#get teams
def get_teams(db: Session,
              skip : int = 0,
              limit : int = 100,
              min_last_changed_date : date = None,
              team_name : str = None,
              league_id : int = None):
    query = db.query(models.Team)
    if min_last_changed_date:
        query = query.filter(models.Team.last_changed_date >= min_last_changed_date)
    if team_name:
        query = query.filter(models.Team.team_name == team_name)
    if league_id:
        query = query.filter(models.Team.league_id == league_id)
    return query.offset(skip).limit(limit).all()


#get some analtical query
def get_player_count(db: Session):
    query = db.query(models.Player)
    return query.count()

def get_team_count(db: Session):
    query = db.query(models.Team)
    return query.count()

def get_league_count(db: Session):
    query = db.query(models.League)
    return query.count()

