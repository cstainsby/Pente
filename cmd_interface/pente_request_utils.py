# --------------------------------------------------------------------------
# FILE: pente_request_utils.py
# NAME: Cole Stainsby
# DESC: This file contains all of the necessary backend request functions
#       the cmd interface will be using 
# --------------------------------------------------------------------------

import requests

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