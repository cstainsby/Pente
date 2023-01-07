

from fastapi import  WebSocket, WebSocketDisconnect
from typing import List
import json

from database import PenteDatabase


class ConnectionManager():
  def __init__(self) -> None:
    # dict containing all connection_id's mapped to a connection object
    self.game_connections: dict[int, GameConnection] = {}

  def connect_player_to_game(self, websocket: WebSocket, game_conn_id: int) -> None:
    # confirm that the game being joined exists
    if game_conn_id in self.game_connections:
      conn = self.game_connections[game_conn_id]
      conn.connect_player(websocket)
    else:
      conn = GameConnection()
      conn.connect_player(websocket)
      self.game_connections.update({game_conn_id: conn})

      self.game_connections.update({game_conn_id: GameConnection})

  def remove_player_from_game(self, game_conn_id: int) -> None:
    if game_conn_id in self.game_connections:
      self.game_connections.pop(game_conn_id)
  
  def broadcast_message_in_game(self, game_conn_id: int, message: json):
    self.game_connections[game_conn_id].broadcast_json_to_all_players(message)


class GameConnection():
  def __init__(self) -> None:
    self.connected_player_websockets: List[WebSocket] = []
  
  async def connect_player(self, websocket: WebSocket):
    await websocket.accept()
    self.connected_player_websockets.append(websocket)
  
  def disconnect_player(self, websocket: WebSocket):
    self.connected_player_websockets.remove(websocket)

  async def broadcast_json_to_all_players(self, game_state_json: json):
    for connection in self.connected_player_websockets:
      await connection.send_json(game_state_json)
  



