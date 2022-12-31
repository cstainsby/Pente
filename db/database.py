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


  # ----------------------------------------------------------------------------------------------
  #   analytics queries 
  # ----------------------------------------------------------------------------------------------
  def get_number_of_games_played(self):
    num_games = 0
    if self.has_valid_connection():
      cur = self.conn.execute("SELECT COUNT(*) FROM PenteGame;")
      num_games = cur.fetchall()
    
    return num_games


  def get_number_of_wins_by_player_type(self, player_type: str):
    if self.has_valid_connection():
      self.conn.execute("""
        SELECT COUNT(*) 
        FROM GameWins g
          JOIN PlayersList pl USING (game_id, player_num)
        WHERE pl.player_type = \"{}\"
      """.format(player_type))
