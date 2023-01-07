from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import json

from .database import PenteDatabase
from . import models
from connection_manager import ConnectionManager 
import pente_game_json_lib

app = FastAPI()
game_connection_manager = ConnectionManager()

origins = [
  "http://localhost",
  "http://localhost:8000",
  "http://localhost:3000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/")
async def test():
  return "hi"


@app.get("/games")
async def get_games():
  """
  DESC: gets a list of games 
  """
  pass


@app.post("/games")
async def post_game():
  """
  DESC: posts a game to the availible games in queue
  """

  pass

@app.post("/games/{game_id}/players")
async def post_game_player_status():
  """
  DESC: used for a player to post their status 

  RETS: 
    status code 
  """
  # if joining confirm that there is enough room for the player

  # TODO confirm that the player attempting to join/leave or whatever is the same person making the request

  return

@app.websocket("/games/{game_id}/connect")
async def game_connect(websocket: WebSocket, game_conn_id: int):
  
  await game_connection_manager.connect_player_to_game(websocket, game_conn_id)
  try:
    while 1:
      received_json = await websocket.receive_json()

      # determine the "type" of the contents the socket just recieved
      # NOTE the json should contain a 
      game_connection_manager.broadcast_message_in_game(game_conn_id, received_json) 
  
  except WebSocketDisconnect:
    game_connection_manager.remove_player_from_game(game_conn_id)

    disconnect_json_msg = pente_game_json_lib.disconnect_message()
    await game_connection_manager.broadcast_message_in_game(game_conn_id, disconnect_json_msg)
