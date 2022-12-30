# --------------------------------------------------------------------------
# FILE: database.py
# NAME: Cole Stainsby
# DESC: Contains a sqlite database for storing game data, I chose sqlite 
#       for its simplicity and the lack of complexity of the data I will 
#       be storing
# --------------------------------------------------------------------------

import sqlite3
import time

class PenteDatabase():
  def __init__(self) -> None:
    self.conn = sqlite3.connect("pente.db")

  def has_valid_connection(self) -> bool:
    if self.conn:
      return True
    else: # has invalid connection
      attempts_made = 0
      self.conn = sqlite3.connect("pente.db")

      while not self.conn and attempts_made < 5:  # keep attempting to connect only make 5 attempts
        time.sleep(2)                             # wait before trying to reconnect again
        self.conn = sqlite3.connect("pente.db")
    
    if self.conn:
      return True 
    return False
    
  
  def insert_game(self, game_log):
    pass