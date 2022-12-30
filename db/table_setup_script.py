# --------------------------------------------------------------------------
# FILE: table_setup_script.py
# NAME: Cole Stainsby
# DESC: A python script which creates or updates the tables stored in the 
#       sqlite database
# --------------------------------------------------------------------------


import sqlite3


conn = sqlite3.connect("pente.db")


if conn:
  # remove all tables to prepare for changes
  # TODO: setup basic migration system to ensure not all data is deleted IF NECESSARY


  conn.execute("""
    CREATE TABLE PenteGame (
      game_id INT,


      PRIMARY KEY (game_id)
    );
  """)

  conn.execute("""
    CREATE TABLE PlayersList (

    );
  """)

  # this table is somewhat static so I will add the types in the setup script 
  conn.execute("""
    CREATE TABLE PlayerType (
      player_type CHAR(20),

      PRIMARY KEY (player_type)
    );
  """)
  conn.execute("""INSERT INTO PlayerType (player_type) VALUES ("RANDOM");""")
  conn.execute("""INSERT INTO PlayerType (player_type) VALUES ("AI");""")
  conn.execute("""INSERT INTO PlayerType (player_type) VALUES ("HUMAN");""")


  conn.execute("""
    CREATE TABLE GameWins (
      game_id
    );
  """)

