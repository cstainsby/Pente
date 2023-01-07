
import json



def disconnect_message(game_id: int, player_id: int):
  return json.dumps({
    "messageTitle": "disconnect",
    "gameID": game_id,
    "playerID": player_id
  })


def connect_message(game_id: int, player_id: int):
  return json.dumps({
    "messageTitle": "connect",
    "gameID": game_id,
    "playerID": player_id
  })


def play_message(game_id: int, player_id: int, place_x: int, place_y: int):
  """
  ARGS:
    player_id: id of player who just played
    game_id: id of the game within the connection list
  """
  return json.dumps({
    "messageTitle": "play",
    "gameID": game_id,
    "whoPlayedPlayerID": player_id,
    "where": {
      "x": place_x,
      "y": place_y
    }
  })

#TODO finish capture message
# def capture_message(game_id: int, player_id: int, place_id: int, place_y: int, ):


def win_message(game_id: int, player_id: int):
  """
  ARGS:
    game_id: id of the game in the connection list
    player_id: id of the player who won
  """
  return json.dumps({
    "messageTitle": "play",
    "gameID": game_id,
    "whoWonPlayerID": player_id
  })

