# --------------------------------------------------------------------------
# FILE: pente.py
# NAME: Cole Stainsby
# DESC: Contains the main functionality of the Pente game
# --------------------------------------------------------------------------

import random 
import numpy as np
import math
from termcolor import colored

class PenteGame():
  def __init__(self, GRID_LENGTH = 19, player_dict = {1: "RANDOM", 2: "RANDOM"}) -> None:
    # NOTE: GRID_LENGTH must be an odd number >= 3
    if GRID_LENGTH < 3 or GRID_LENGTH % 2 != 1:
      return 

    self.GRID_LENGTH = GRID_LENGTH
    self.GAME_BOARD = [[0 for i in range(self.GRID_LENGTH)] for j in range(self.GRID_LENGTH)]

    # create players based off player dict
    self.players = []
    for player_id in player_dict.keys():
      player_type = player_dict[player_id] # should be a string detailing what type the player is
      new_player = Player(player_id=player_id, play_type_option=player_type)
      self.players.append(new_player)    

    self.current_player_turn = 0

    self.pairs_captured = [0] * len(self.players) # parallel to players, keeps track of the number of pairs that players captured

    # a log of each move made in the game
    # NOTE: every log message will have a type in the first col
    self.LOG_TYPE_IDS = { # a dict which helps uniquley label each of the log messages
      "PLACEMENT": 0,  # labels each stone placed | shape: (log_id, player_id_who_placed, x, y)
      "CAPTURE": 1,    # for labeling a capture   | shape: (log_id, player_id_who_captured,  [ordered (x, y) of all stones involved])
      "WIN": 2         # labels the victor        | shape: (log_id, player_id)
    }
    self.game_log = [] 

  def pretty_print_game(self) -> None:
    """NAME: pretty_print_game
    
    DESC: a pretty printer for the current game state
    """
    player_color_mapping = {
      0: "white", 
      1: "green",
      2: "blue"
    }


    print("      ", end="")
    for i in range(self.GRID_LENGTH):
      i_indent = "  " + " " * (2 - len(str(i)))
      print(i, end=i_indent)
    print()

    for i in range(self.GRID_LENGTH):
      i_indent = " " * (2 - len(str(i)))
      print("   ", "----" * self.GRID_LENGTH)
      print(i, " ", end=i_indent)
      for j in range(self.GRID_LENGTH):
        grid_val = self.GAME_BOARD[i][j]
        val_indent = " " * (2 - len(str(grid_val)))
        print("|", colored(grid_val, player_color_mapping[grid_val]), end=val_indent)
      print()
    print()

  
  def main_game_loop(self) -> None:
    """NAME: main_game_loop

    DESC: Contains the main loop which pente runs through
    """
    # game ends when a player captures 5 pairs from the other player
    # or if they get 5 in a row

    five_in_row_found = False 
    five_pairs_captured = False

    player_counter = 0
    
    while not five_in_row_found and not five_pairs_captured:
      curr_player = self.players[player_counter]

      # have player generate their move 
      x, y = curr_player.make_turn_choice(self.GAME_BOARD)

      # register players move with board
      self.register_move(curr_player.player_id , x, y)

      five_in_row_found = self.check_five_in_a_row()

      self.capture_capturable_surrounding_stones()

      player_counter = (player_counter + 1) % len(self.players)


  def register_move(self, player_id: int, x: int, y: int):
    """NAME: main_game_loop

    DESC: updates the game state and log every time a move is made 
    """ 

    if not isinstance(player_id, int) or not isinstance(x, int) or not isinstance(y, int):
      return TypeError


    # cannot play out of bounds 
    if y >= len(self.GAME_BOARD) or y < 0 or x >= len(self.GAME_BOARD[0]) or x < 0: 
      return IndexError

    # cannot play on top of a space thats occupied
    if self.GAME_BOARD[y][x] != 0:
      return ValueError
    
    # print("play successfully registered at x:", x, "y:", y, "for player", player_id)

    self.GAME_BOARD[y][x] = player_id
    self.game_log.append(("PLACEMENT", player_id, x, y))

  
  def get_last_move(self):
    """NAME: get_last_move

    DESC: uses the game log to find the last move that was made 
    """ 
    last_move = None
    log_index = len(self.game_log) - 1 # start at end of list 

    while(log_index >= 0 and self.game_log[log_index][0] != "PLACEMENT"):
      log_index -= 1
    
    if log_index >= 0:
      last_move = self.game_log[log_index]
    
    return last_move


  def get_directional_lists_from_point(self, x, y):
    """NAME: get_directional_lists_from_point

    DESC: Helper function which finds the lists of all intersections which form an intersecting line with the given x, y pair
          e.g. given diagram where x is the point
              \ | /          
              - x -          
              / | \          
          - the \ portions are the left diagonal 
          - the / portions are the right diagonal 
          - the - portions are horizontal 
          - the | portions are vertical
    """

    np_game_board = np.array(self.GAME_BOARD)

    # \ diagonal
    offset = x - y
    left_diag_list = list(np_game_board.diagonal(offset))

    # / diagonal
    offset = len(self.GAME_BOARD) - 1 - x - y
    right_diag_list_reversed = list(np.fliplr(np_game_board).diagonal(offset)) 
    right_diag_list = list(reversed(right_diag_list_reversed)) # because we fliped the list to use .diagonal, reverse it back

    # - horizontal
    horizontal_list = list(np_game_board[y])

    # | vertical
    vertical_list = list(np_game_board[:, x])

    return left_diag_list, right_diag_list, horizontal_list, vertical_list


  def coordinates_in_2d_plane_to_diagonal_position(self, x_cor: int, y_cor: int, direction: str) -> int:
    """NAME: coordinates_in_2d_plane_to_diagonal_position

    DESC: Given the diagonal system described in get_directional_lists_from_point function docstring
          this function will locate the position within a diagonal from its 2D coordinate couterpart
    
    ARGS: 
      x_cor: x coordinate within the 2D matrix
      y_cor: y coordinate within the 2D matrix
      direction: string (NOTE: either "LEFT" or "RIGHT") telling the algo. what type the diagonal is

    RETS: 
      position: index in a diagonal 
    """

    # all we need to do is transform the input coordinates like we are flipping the matrix on its x axis 
    # to make it behave the same as the right diagonal
    midpoint_index = int((self.GRID_LENGTH - 1) / 2)
    adjusted_x_cor = 0
    adjusted_y_cor = 0

    grid_diagonal_lengths = [i for i in range(1, self.GRID_LENGTH + 1)] + [i for i in range(self.GRID_LENGTH - 1, 0, -1)]

    if direction == "LEFT": # left must have its coordinates reflected across x axis to work
      adjusted_x_cor = x_cor
      if midpoint_index < y_cor:
        adjusted_y_cor = int(abs(abs(midpoint_index - y_cor) - midpoint_index))
      else:
        adjusted_y_cor = int(abs(abs(midpoint_index - y_cor) + midpoint_index))

    elif direction == "RIGHT": # right needs no transformations
      adjusted_x_cor = x_cor
      adjusted_y_cor = y_cor
    
    diag_position_index = adjusted_x_cor + adjusted_y_cor                   # finds the diagonal position within the grid, 
                                                                            #     used to get index of length
    curr_diag_length = grid_diagonal_lengths[diag_position_index]           # get the current diagonal length
    offset_from_right_diagonal = (adjusted_x_cor - adjusted_y_cor) / 2      # determines the offset from the "right diagonal" 
                                                                            #     from the center point
    middle_index_in_right_diagonal = ((curr_diag_length - 1) / 2)              
    position = offset_from_right_diagonal + middle_index_in_right_diagonal  # the middle index plus the offset yeilds the position 
                                                                            #     within the left diagonal 
    return int(position)


  def check_five_in_a_row(self) -> bool:
    """NAME: check_five_in_a_row

    DESC: using the directional lists from the last played point, check if the most recent play created a 
          sequence of five stones, all placed by a single player, in a row
    """
    if len(self.game_log) == 0: # following code relies on knowing what the last play was
      return False              # catch this if the log is empty
    
    _, player_id, intersection_x_played_on, intersection_y_played_on = self.get_last_move()

    left_diag_list, right_diag_list, horizontal_list, vertical_list = self.get_directional_lists_from_point(intersection_x_played_on, intersection_y_played_on)

    # package into list in order to cut down on repeated code
    raw_lists = [
      left_diag_list, 
      right_diag_list, 
      horizontal_list, 
      vertical_list
    ]
    for raw_list in raw_lists:
      # find the longest string of player_id and return true if 
      # there is one greater than 4
      highest_sequence = 0

      for intersection_value in raw_list:
        if intersection_value == player_id:
          highest_sequence += 1
        else: 
          highest_sequence = 0
        
        if highest_sequence > 4:
          self.game_log.append(("WIN", player_id))
          return True 
    
    return False

  def capture_capturable_surrounding_stones(self) -> None:
    """NAME: capture_capturable_surrounding_stones

    DESC: using the directional lists from the last played point, check if the most recent play created a 
          sequence of (placed stone -> two stones with same id -> another stone with same id value as placed stone)
          if so delete the two middle stones. All directions will be checked. 
    """

    _, player_id, intersection_x_played_on, intersection_y_played_on = self.get_last_move()

    left_diag_list, right_diag_list, horizontal_list, vertical_list = self.get_directional_lists_from_point(intersection_x_played_on, intersection_y_played_on)
    
    left_diag_index_played_on = self.coordinates_in_2d_plane_to_diagonal_position(intersection_x_played_on, intersection_y_played_on, "LEFT")
    right_diag_index_played_on = self.coordinates_in_2d_plane_to_diagonal_position(intersection_x_played_on, intersection_y_played_on, "RIGHT")
    
    # package into list in order to cut down on repeated code
    # shape: [(index_of_new_placement, the list)]
    raw_lists = [
      (left_diag_index_played_on, left_diag_list),   
      (right_diag_index_played_on,  right_diag_list),  
      (intersection_x_played_on, horizontal_list), 
      (intersection_y_played_on, vertical_list)
    ]
    for raw_list_index, (place_index, raw_list) in enumerate(raw_lists):
      if len(raw_list) >= 4: # not worth considering rows which cant contain enough stones to make a capture sequence 
        # ls_values will contain all values to the left of the placement index, rs_values to the right
        ls_values = raw_list[:place_index]
        rs_values = raw_list[place_index + 1:] # NOTE: adding 1 to make rs non-inclusve to placement spot

        # for the "left" side values 
        if len(ls_values) >= 3 and ls_values[-2] == ls_values[-1] and ls_values[place_index - 3] == player_id:
          # then pieces at indices -2 and -1 should be "captured", 
          # base on the raw list index, "direction" of list, replace game_board values 
          if raw_list_index == 0: # left diagonal 
            self.GAME_BOARD[intersection_y_played_on - 1][intersection_x_played_on - 1] = 0
            self.GAME_BOARD[intersection_y_played_on - 2][intersection_x_played_on - 2] = 0
          elif raw_list_index == 1: # right diagonal 
            self.GAME_BOARD[intersection_y_played_on + 1][intersection_x_played_on - 1] = 0
            self.GAME_BOARD[intersection_y_played_on + 2][intersection_x_played_on - 2] = 0
          elif raw_list_index == 2: # horizontal
            self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on - 1] = 0
            self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on - 2] = 0
          elif raw_list_index == 3: # vertical 
            self.GAME_BOARD[intersection_y_played_on - 1][intersection_x_played_on] = 0
            self.GAME_BOARD[intersection_y_played_on - 2][intersection_x_played_on] = 0
            

        # for the "right" side values 
        if len(rs_values) >= 3 and rs_values[1] == rs_values[0] and rs_values[2] == player_id:
          # then pieces at indices -2 and -1 should be "captured", 
          # base on the raw list index, "direction" of list, replace game_board values 
          if raw_list_index == 0: # left diagonal 
            self.GAME_BOARD[intersection_y_played_on + 1][intersection_x_played_on + 1] = 0
            self.GAME_BOARD[intersection_y_played_on + 2][intersection_x_played_on + 2] = 0
          elif raw_list_index == 1: # right diagonal 
            # print("check RIGHTDIAG:", intersection_x_played_on + 2, intersection_y_played_on - 2)
            # print("rs vals", rs_values)
            self.GAME_BOARD[intersection_y_played_on - 1][intersection_x_played_on + 1] = 0
            self.GAME_BOARD[intersection_y_played_on - 2][intersection_x_played_on + 2] = 0
          elif raw_list_index == 2: # horizontal
            self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on + 1] = 0
            self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on + 2] = 0
          elif raw_list_index == 3: # vertical 
            self.GAME_BOARD[intersection_y_played_on + 1][intersection_x_played_on] = 0
            self.GAME_BOARD[intersection_y_played_on + 2][intersection_x_played_on] = 0
    
    # self.pretty_print_game()

    

  def start(self):

    self.main_game_loop()

    self.finish()
  

  def finish(self):
    """After the game is over, write data to file"""
    pass



class Player():
  def __init__(self, player_id: int, play_type_option: str) -> None:
    self.player_id = player_id # each player gets an id 

    self.PLAY_DESCISION_OPTIONS = [
      "RANDOM",
      "AI",
      "HUMAN"
    ]

    # selected play type option
    if self.PLAY_DESCISION_OPTIONS.count(play_type_option) == 1:
      self.selected_play_type_option = play_type_option
    else:
      return TypeError
    

  
  def make_turn_choice(self, game_board: list):
    """NAME: make_turn_choice

    DESC: given game state and predefined player type, make a move

    RET: returns a tuple choice, which contains (x, y) 
    """

    board_length = len(game_board)

    # a compiled list of index options corresponding to intersections which can be played on
    current_choices = [(x, y) for y in range(board_length) for x in range(board_length) if game_board[y][x] == 0]
    choice = None

    if self.selected_play_type_option == "RANDOM":
      random.shuffle(current_choices)
      choice = current_choices[0] 
      # print("current rand player (id:" + str(self.player_id) + ") choice: " + str(choice))

    elif self.selected_play_type_option == "AI":
      # TODO: implement model
      pass 

    elif self.selected_play_type_option == "PLAYER":
      # TODO: implement player
      pass 

    return choice 


if __name__ == "__main__":
  game = PenteGame()
  game.start()