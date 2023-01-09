# --------------------------------------------------------------------------
# FILE: api.py
# NAME: Cole Stainsby
# DESC: Contains all fastapi endpoints in this project
# --------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import json

from .database import PenteDatabase
from . import models
from .connection_manager import ConnectionManager 

app = FastAPI()
game_connection_manager = ConnectionManager()
db = PenteDatabase()

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


@app.get("/play/games")
async def get_open_games():
  """
  DESC: gets a list of games from the connection manager
  """
  current_connections = game_connection_manager.get_game_connections()

  res = None
  for conn_info in current_connections:
    print("conn info", conn_info)
    res_item = json.dumps({
      "creator_name": "",
      "num_players": 0
    })

  return "test"


@app.post("/play/games")
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

      # determine if 
      game_connection_manager.broadcast_message_in_game(game_conn_id, received_json)


  
  except WebSocketDisconnect:
    game_connection_manager.remove_player_from_game(game_conn_id)

    disconnect_json_msg = pente_game_json_lib.disconnect_message()
    await game_connection_manager.broadcast_message_in_game(game_conn_id, disconnect_json_msg)
