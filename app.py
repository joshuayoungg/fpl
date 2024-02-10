import os
from dotenv import dotenv_values
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing import List


config = dotenv_values(".env")
app = FastAPI(
    title="Fantasy EPL Formatted API",
    summary="A formatted version of the fantasy epl api",
)

#connect to the mongodb server and connect to the database
def __get_connection():
    client = MongoClient(config["ATLAS_URI"])
    print('Connection Established.')
    return client

client = __get_connection()
db = client.epl
teams_collection = db.get_collection("teams")
print(teams_collection)


class TeamsModel(BaseModel):
    """
    Container for a single student record.
    """
    id: int = Field(...)
    name: str = Field(...)
    name_abb: str = Field(...)
    strength: float = Field(...)
    strength_overall_home: float = Field(...)
    strength_overall_away: float = Field(...)
    past_fixtures: List[dict] = Field(...)
    players_stats: List[dict] = Field(...)
    upcoming_fixtures: List[dict] = Field(...)
    median_expected_goals: float = Field(...)
    total_expected_goals: float = Field(...)
    median_expected_assists: float = Field(...)
    total_expected_assists: float = Field(...)


class TeamsModelCollection(BaseModel):
    """
    A container holding a list of `TeamsModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    teams: List[TeamsModel]


@app.get(
    "/",
    response_description="List all teams",
    response_model=TeamsModelCollection,
    response_model_by_alias=False,
)
def list_students():
    """
    List all of the teams stats data in the database.
    """
    items = teams_collection.find()
    parsed_items = []
    for item in items:
        parsed_items.append(item)
    return TeamsModelCollection(teams=parsed_items)

