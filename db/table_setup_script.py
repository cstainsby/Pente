# --------------------------------------------------------------------------
# FILE: table_setup_script.py
# NAME: Cole Stainsby
# DESC: A python script which creates or updates the tables stored in the 
#       sqlite database
# --------------------------------------------------------------------------


import sqlite3


conn = sqlite3.connect("pente.db")

def update_table_prompt(table_name) -> bool:
  delete_table_res_raw = input("Do you want to update table \"" + table_name + "\" [y/n]")

  if delete_table_res_raw == "y":
    return True 
  return False

if conn:
  # remove all tables to prepare for changes
  # TODO: setup basic migration system to ensure not all data is deleted IF NECESSARY

  if update_table_prompt("PenteGame"):
    conn.execute("DROP TABLE IF EXISTS PenteGame;")

    conn.execute("""
      CREATE TABLE PenteGame (
        game_id INT,
        grid_length INT NOT NULL,

        PRIMARY KEY (game_id),

        CONSTRAINT valid_game_id CHECK (game_id >= 0)
      );
    """)
  
  if update_table_prompt("PlayerType"):
    conn.execute("DROP TABLE IF EXISTS PlayerType;")
    
    # this table is somewhat static so I will add the types in the setup script
    # other values shouldn't be added to this anywhere other than here 
    conn.execute("""
      CREATE TABLE PlayerType (
        player_type CHAR(20),

        PRIMARY KEY (player_type)
      );
    """)
    conn.execute("""INSERT INTO PlayerType (player_type) VALUES ("RANDOM");""")
    conn.execute("""INSERT INTO PlayerType (player_type) VALUES ("AI");""")
    conn.execute("""INSERT INTO PlayerType (player_type) VALUES ("HUMAN");""")

  if update_table_prompt("PlayersList"):
    conn.execute("DROP TABLE IF EXISTS PlayersList;")
    
    conn.execute("""
      CREATE TABLE PlayersList (
        game_id INT,
        player_num INT,
        player_type CHAR(20) NOT NULL,

        PRIMARY KEY (game_id, player_num),
        FOREIGN KEY (game_id) REFERENCES PenteGame(game_id),
        FOREIGN KEY (player_type) REFERENCES PlayerType(player_type),

        CONSTRAINT valid_player_num CHECK (player_num >= 0)
      );
    """)

  if update_table_prompt("GameWins"):
    conn.execute("DROP TABLE IF EXISTS GameWins;")
    
    conn.execute("""
      CREATE TABLE GameWins (
        game_id INT,
        player_num INT,

        PRIMARY KEY (game_id, player_num)
        FOREIGN KEY (game_id) REFERENCES PenteGame(game_id),
        FOREIGN KEY (player_num) REFERENCES PlayersList(player_num)
      );
    """)

  if update_table_prompt("Placements"):
    conn.execute("DROP TABLE IF EXISTS Placements;")
    
    conn.execute("""
      CREATE TABLE Placements (
        game_id INT, 
        place_num INT,
        player_num INT NOT NULL,
        place_x INT NOT NULL,
        place_y INT NOT NULL,

        PRIMARY KEY (game_id, place_num),
        FOREIGN KEY (game_id) REFERENCES PenteGame(game_id),
        FOREIGN KEY (player_num) REFERENCES PlayersList(player_num),

        CONSTRAINT valid_place_num CHECK (place_num >= 0)
      );
    """)
  
  if update_table_prompt("Captures"):
    conn.execute("DROP TABLE IF EXISTS Captures;")
    
    # instead of statically saying which positions were involved in the capture 
    # I will state the direction of the capture. It is up to the game itself
    # to determine if the capture was valid before storing it.

    # I'm doing this because if I ever decide to allow changing the rules on how many 
    # peices can be captured at once this will be a much better solution 

    # number mapping to direction 
    #   1  2  3
    #    \ | /
    # 0 -- x -- 4
    #    / | \
    #   7  6  5
    conn.execute("""
      CREATE TABLE Captures (
        game_id INT, 
        cap_num INT,
        player_num INT NOT NULL,
        place_x INT NOT NULL,
        place_y INT NOT NULL,

        cap_direction INT NOT NULL,

        PRIMARY KEY (game_id, cap_num),
        FOREIGN KEY (game_id) REFERENCES PenteGame(game_id),
        FOREIGN KEY (player_num) REFERENCES PlayersList(player_num),

        CONSTRAINT valid_cap_num CHECK (cap_num >= 0),
        CONSTRAINT valid_cap_direction CHECK (cap_direction >= 0 AND cap_direction <= 7)
      );
    """)


