# --------------------------------------------------------------------------
# FILE: connection_manager.py
# NAME: Cole Stainsby
# DESC: A manager class which holds information related to currently open
#       games and who is connected to them.
#       This code leverages websockets to create a publisher-subscriber 
#       pattern where users will receive only the information they need 
#       relative to which games they are connected to.
# --------------------------------------------------------------------------

from fastapi import  WebSocket, WebSocketDisconnect
from typing import List
import json


class PenteGameConnectionManager():
  def __init__(self) -> None:
    # dict containing all connection_id's mapped to a connection object
    # game info dict should include
    # GameConnectionList, 
    # str,                # game title
    # int,                # num_players 
    # str,                # created by

    self.open_games = {}

  def get_availble_connection(self) -> int:
    """Have the connection manager find and return a valid connection key
    """
    all_keys = [i for i in range(0, len(self.open_games))]
    used_keys = self.open_games.keys()

    # try filling in any keys which have ended
    availible_keys = [key for key in all_keys if not key in used_keys]

    if len(availible_keys) == 0: 
      # all keys in [0, len(open_games)] taken, increase num game connections by one
      return len(self.open_games)

    return availible_keys[0]

  def create_game(self, conn_id, game_title: str, num_players: int, created_by: str):
    if not conn_id in self.open_games:
      conn_list = GameConnectionList()
      info_dict = {
        "game_title": game_title,
        "num_players": num_players,
        "created_by": created_by,
        "conn_list": conn_list
      }

      self.open_games.update({conn_id: info_dict})

  def get_open_games(self):
    return self.open_games

  def connect_player_to_game(self, websocket: WebSocket, game_conn_id: int) -> None:
    # confirm that the game being joined exists
    if game_conn_id in self.open_games:
      conn_list = self.open_games[game_conn_id]
      conn_list.connect_player(websocket)
    else:
      # create game if it doesn't exist
      conn_list = GameConnectionList()
      conn_list.connect_player(websocket)
      self.open_games.update({game_conn_id: conn_list})

      self.open_games.update({game_conn_id: GameConnectionList})

  def remove_player_from_game(self, game_conn_id: int) -> None:
    if game_conn_id in self.open_games:
      self.open_games.pop(game_conn_id)
  
  def broadcast_message_in_game(self, game_conn_id: int, message: json):
    self.open_games[game_conn_id].broadcast_json_to_all_players(message)


class GameConnectionList():
  def __init__(self) -> None:
    self.connected_player_websockets: List[WebSocket] = []
  
  def __len__(self):
    return len(self.connected_player_websockets)
  
  async def connect_player(self, websocket: WebSocket):
    await websocket.accept()
    self.connected_player_websockets.append(websocket)
  
  def disconnect_player(self, websocket: WebSocket):
    self.connected_player_websockets.remove(websocket)

  async def broadcast_json_to_all_players(self, game_state_json: json):
    for connection in self.connected_player_websockets:
      await connection.send_json(game_state_json)
  



