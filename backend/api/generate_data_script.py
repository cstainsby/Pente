# --------------------------------------------------------------------------
# FILE: generate_data_script.py
# NAME: Cole Stainsby
# DESC: A python script which generates Pente game data by specifying 
#       game run settings and running said games n times 
# --------------------------------------------------------------------------

from pente.pente import PenteGame


def generate_data(num_game_iters: int, grid_length: int, player_settings: dict):
  
  for i in range(num_game_iters):
    if i % 10 == 0: print("current itter", i)
    pente_game = PenteGame(GRID_LENGTH=grid_length, player_dict=player_settings)

    pente_game.start()


if __name__ == "__main__":
  # -------------------------------
  #   define run settings here
  # -------------------------------
  NUM_ITERS = 1000
  GRID_LENGTH = 19 # 19 is standard
  PLAYER_SETTINGS = {
    1: "RANDOM", 
    2: "RANDOM"
  }
  # -------------------------------

  generate_data(NUM_ITERS, GRID_LENGTH, PLAYER_SETTINGS)