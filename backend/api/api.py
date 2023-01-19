# --------------------------------------------------------------------------
# FILE: api.py
# NAME: Cole Stainsby
# DESC: Contains all fastapi endpoints in this project
# --------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware

import json

from .db.database import PenteDatabase
from .pente.pente import PenteGame
from . import models
from .connection_manager import PenteGameConnectionManager 

app = FastAPI()
game_connection_manager = PenteGameConnectionManager()
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

@app.get("/play/games")
async def get_open_games_info():
  """
  DESC: gets a list of games from the connection manager
  """
  open_games = game_connection_manager.get_open_games()

  returned_list = []

  for key, info_dict in open_games.items():
    returned_list.append({
      "connection_key": key,
      "game_title": info_dict["game_title"],
      "num_players": info_dict["num_players"],
      "created_by": info_dict["created_by"],
      "curr_player_count": len(info_dict["conn_list"])
    })
  
  return {"open_game_list": returned_list}
  


@app.post("/play/games")
async def post_game(playableGame: models.PlayableGame):
  """
  DESC: posts a game to the availible games in queue
        this is done through the connection manager
  """

  conn_key = game_connection_manager.get_availble_connection()

  game_connection_manager.create_game(
    conn_key, 
    playableGame.game_title, 
    playableGame.num_players,
    playableGame.created_by
  )

  return playableGame


# @app.websocket("/games/{game_id}/connect")
# async def game_connect(websocket: WebSocket, game_conn_id: int):
  
#   await game_connection_manager.connect_player_to_game(websocket, game_conn_id)
#   try:
#     while 1:
#       received_json = await websocket.receive_json()

#       # determine the "type" of the contents the socket just recieved

#       # determine if 
#       game_connection_manager.broadcast_message_in_game(game_conn_id, received_json)


  
  # except WebSocketDisconnect:
  #   game_connection_manager.remove_player_from_game(game_conn_id)

  #   disconnect_json_msg = pente_game_json_lib.disconnect_message()
  #   await game_connection_manager.broadcast_message_in_game(game_conn_id, disconnect_json_msg)





@app.post("/play/games/ai")
async def post_placement_in_ai_game(gamePlacement: str = Query(..., title="The current game state")):
  # TODO: there might be a more efficient way to pass information but this will be the quickest to get running 

  # rather than have the game running on the backend 
  # hold the game state on the frontend and when a move is played post the game state and the most recent move

  # fill a game with the frontends info 
  game = PenteGame()
  game.GAME_BOARD = gamePlacement.game_state
  
  # perform the most recent placement
  game.register_move(
    gamePlacement.player_id,
    gamePlacement.x_cor,
    gamePlacement.y_cor
  )

  # based on this placement, get a response from the ai
  # this will be in the form of a new returned game state 
  # as well as a log that can be attached to the frontends current log 

  # TODO for now just return without making a play

  res = {
    "new_game_board": game.GAME_BOARD,
    "new_game_log": game.game_log
  }
  print("backend returning res", res)

  return res