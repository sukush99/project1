from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

import crud
import schemas
from database import SessionLocal

api_description = """ 
This API provides read-only access to info from the SportsWorldCentral
(SWC) Fantasy Football API.
The endpoints are grouped into the following categories:

## Analytics
Get information about the health of the API and counts of leagues, teams,
and players.

## Player
You can get a list of NFL players, or search for an individual player by
player_id.

## Scoring
You can get a list of NFL player performances, including the fantasy points
they scored using SWC league scoring.

## Membership
Get information about all the SWC fantasy football leagues and the teams in them.
"""

#FastAPI constructor with additional details added for OpenAPI Specification
app = FastAPI(
    description=api_description, 
    title="Sports World Central (SWC) Fantasy Footbal API", 
    version="0.1" 
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["analytics"],
          summary="Get Analytics Overview",
          description="Fetch a general overview of analytics related to the system.",
          response_description="Returns an overview of the analytics in JSON format.",
          operation_id="get_analytics_overview")
async def root():
    return {"message": "API health check successful!"}

@app.get("/v0/players", response_model=list[schemas.Player], tags=["player"],
          summary="Get All Players",
          description="Retrieve a list of all players from the database.",
          response_description="A list of player objects with player details.",
          operation_id="get_all_players")
def read_players(skip: int = Query(0, description="The number of items toskip at the beginning of API call."),
                limit: int = Query(100, description="The number of records to returnafter the skipped records."),
                min_last_changed_date: date = Query(None, description="The minimum date of change that you want to return records. Exclude any records changed before this."),
                first_name: str = Query(None, description="The first name of the playersto return"),
                last_name: str = Query(None, description="The last name of the playersto return"),
                db: Session = Depends(get_db)):
    players = crud.get_players(db,
                              skip=skip,
                              limit=limit,
                              min_last_changed_date=min_last_changed_date,
                              last_name=last_name,
                              first_name=first_name)
    return players



@app.get("/v0/players/{player_id}",
        response_model=schemas.Player,
        summary="Get one player using the Player ID, which is internal to SWC",
        description="If you have an SWC Player ID of a player from another API call such as v0_get_players, you can call this API using the player ID", 
        response_description="One NFL player", 
        operation_id="v0_get_players_by_player_id", 
        tags=["player"])
def read_player(player_id: int,
                db: Session = Depends(get_db)):
    """
    Retrieve a player by their unique Player ID.
    If the player is not found, a 404 error is raised.
    """
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.get("/v0/performances", response_model=list[schemas.Performance], tags=["scoring"],
          summary="Get All Performances",
          description="Retrieve a list of all performances from the database.",
          response_description="A list of performance objects representing individual player performances.",
          operation_id="get_all_performances")
def read_performances(skip: int = Query(0, description="The number of items to skip at the beginning of API call."),
                      limit: int = Query(100, description="The number of records to return after the skipped records."),
                      min_last_changed_date: date = Query(None, description="The minimum date of change that you want to return records."),
                      db: Session = Depends(get_db)):
    """
    Retrieve all performances within the specified range of records.
    Filters can be applied for performances updated after a given date.
    """
    performances = crud.get_performances(db,
                                         skip=skip,
                                         limit=limit,
                                         min_last_changed_date=min_last_changed_date)
    return performances

@app.get("/v0/leagues/{league_id}", response_model=schemas.League, tags=["membership"],
          summary="Get League by ID",
          description="Retrieve a specific league by its ID.",
          response_description="The details of a league with the given ID.",
          operation_id="get_league_by_id")
def read_league(league_id: int,
                db: Session = Depends(get_db)):
    """
    Fetch league details by its ID.
    If no league is found, a 404 error is returned.
    """
    league = crud.get_league(db, league_id=league_id)
    if league is None:
        raise HTTPException(status_code=404, detail="League not found")
    return league

@app.get("/v0/leagues", response_model=list[schemas.League], tags=["membership"],
          summary="Get All Leagues",
          description="Retrieve a list of all leagues from the database.",
          response_description="A list of league objects representing different leagues.",
          operation_id="get_all_leagues")
def read_leagues(skip: int = Query(0, description="The number of items to skip at the beginning of API call."),
                 limit: int = Query(100, description="The number of records to return after the skipped records."),
                 min_last_changed_date: date = Query(None, description="The minimum date of change to filter records."),
                 league_name: str = Query(None, description="The league name to filter records."),
                 db: Session = Depends(get_db)):
    """
    Retrieve a list of all leagues from the database.
    Optionally, you can filter leagues by their name or the minimum change date.
    """
    leagues = crud.get_leagues(db,
                               skip=skip,
                               limit=limit,
                               min_last_changed_date=min_last_changed_date,
                               league_name=league_name)
    return leagues

@app.get("/v0/teams", response_model=list[schemas.Team], tags=["membership"],
          summary="Get All Teams",
          description="Retrieve a list of all teams in the system.",
          response_description="A list of team objects representing different teams.",
          operation_id="get_all_teams")
def read_teams(skip: int = Query(0, description="The number of items to skip at the beginning of API call."),
               limit: int = Query(100, description="The number of records to return after the skipped records."),
               min_last_changed_date: date = Query(None, description="The minimum date of change to filter records."),
               team_name: str = Query(None, description="The team name to filter records."),
               league_id: int = Query(None, description="The league ID to filter teams."),
               db: Session = Depends(get_db)):
    """
    Retrieve a list of teams in the system.
    Filters can be applied for team names, league ID, or the minimum change date.
    """
    teams = crud.get_teams(db,
                           skip=skip,
                           limit=limit,
                           min_last_changed_date=min_last_changed_date,
                           team_name=team_name,
                           league_id=league_id)
    return teams

@app.get("/v0/counts/", response_model=schemas.Counts, tags=["analytics"],
          summary="Get System Counts",
          description="Retrieve the count of players, teams, and leagues in the system.",
          response_description="Returns a count of players, teams, and leagues.",
          operation_id="get_system_counts")
def get_count(db: Session = Depends(get_db)):
    """
    Fetch the counts for players, teams, and leagues from the database.
    Returns the total number of players, teams, and leagues.
    """
    counts = schemas.Counts(
        league_count=crud.get_league_count(db),
        team_count=crud.get_team_count(db),
        player_count=crud.get_player_count(db)
    )
    return counts