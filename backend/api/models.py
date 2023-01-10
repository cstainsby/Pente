# --------------------------------------------------------------------------
# FILE: models.py
# NAME: Cole Stainsby
# DESC: Contains all of the fastapi models used for the endpoints
# --------------------------------------------------------------------------

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class PlayableGame(BaseModel):
  game_title: str 
  num_players: int 
  created_by: str