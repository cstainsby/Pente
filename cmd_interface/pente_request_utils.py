# --------------------------------------------------------------------------
# FILE: pente_request_utils.py
# NAME: Cole Stainsby
# DESC: This file contains all of the necessary backend request functions
#       the cmd interface will be using 
# --------------------------------------------------------------------------

import requests
import json

# possible endpoints for backend 
LOCAL_ENDPOINT = "http://localhost:8000"

chosen_endpoint_head = LOCAL_ENDPOINT

def get_joinable_games():
  # return None if invalid 400 response
  endpoint = chosen_endpoint_head + "/play/games"
  res = requests.get(endpoint)

  if not res.ok:
    return None 

  return res.content


def post_game(game_title: str, num_players: int):
  endpoint = chosen_endpoint_head + "/play/games"

  #TODO make identifiers for people
  game_info_json = {
    "game_title": game_title,
    "created_by": "",
    "num_players": num_players
  }

  print("post game info json", game_info_json)

  res = requests.post(endpoint, json=game_info_json)

  print("post response", res.text)