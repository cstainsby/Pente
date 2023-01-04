# --------------------------------------------------------------------------
# FILE: database.py
# NAME: Cole Stainsby
# DESC: Contains a sqlite database for storing game data, I chose sqlite 
#       for its simplicity and the lack of complexity of the data I will 
#       be storing
# --------------------------------------------------------------------------

import sqlite3
import time

from pente.pente import PenteGame

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
    
  
  def insert_game(self, pente_game: PenteGame):
    
    game_id = self.get_number_of_games_played()

    # insert PenteGame 
    self.conn.execute("""
      INSERT INTO PenteGame (game_id, grid_length) VALUES ({}, {});
    """.format(game_id, pente_game.GRID_LENGTH))

    # insert PlayersList 
    for player in pente_game.players:
      player_num = player.player_id
      player_type = player.selected_play_type_option

      self.conn.execute("""
        INSERT INTO PlayersList (game_id, player_num, player_type)
          VALUES ({}, {}, {});
      """.format(game_id, player_num, player_type))

    # insert game winner
    # there should be a winning post in the game log in the last postion 
    winner_log = pente_game.game_log[-1]
    winning_player_id = winner_log[1]

    self.conn.execute("""
      INSERT INTO GameWins (game_id, player_num)
        VALUES ({}, {});
    """.format(game_id, winning_player_id))

    # insert all placements 
    for place_num, log in enumerate(pente_game.game_log):
      if log[0] == "PLACEMENT": #NOTE: as defined in pente.py the first col will define log type
        player_id_who_placed = log[1]
        place_x = log[2]
        place_y = log[3]

        self.conn.execute("""
          INSERT INTO Placements (game_id, place_num, player_num, place_x, place_y)
            VALUES ({}, {}, {}, {}, {});
        """.format(game_id, place_num, player_id_who_placed, place_x, place_y))
    
    # insert all captures
    for place_num, log in enumerate(pente_game.game_log):
      if log[0] == "CAPTURE": #NOTE: as defined in pente.py the first col will define log type
        player_id_who_captured = log[1]
        place_x = log[2]
        place_y = log[3]

        self.conn.execute("""
          INSERT INTO Placements (game_id, place_num, player_num, place_x, place_y)
            VALUES ({}, {}, {}, {}, {});
        """.format(game_id, place_num, player_id_who_placed, place_x, place_y))

  def get_game_by_game_id(self):
    game_log = []

    return game_log


  # ----------------------------------------------------------------------------------------------
  #   analytics queries 
  # ----------------------------------------------------------------------------------------------
  def get_number_of_games_played(self):
    num_games = 0
    if self.has_valid_connection():
      cur = self.conn.execute("SELECT COUNT(*) FROM PenteGame;")
      (num_games, ) = cur.fetchone()
    
    return num_games


  def get_number_of_wins_by_player_type(self, player_type: str):
    num_wins_by_player_type = 0
    if self.has_valid_connection():
      cur = self.conn.execute("""
        SELECT COUNT(*) 
        FROM GameWins g
          JOIN PlayersList pl USING (game_id, player_num)
        WHERE pl.player_type = \"{}\"
      """.format(player_type))
      (num_wins_by_player_type, ) = cur.fetchone()
    return num_wins_by_player_type

