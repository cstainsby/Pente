# --------------------------------------------------------------------------
# FILE: pente.py
# NAME: Cole Stainsby
# DESC: Contains the main functionality of the Pente game
# --------------------------------------------------------------------------

import random 
import numpy as np
import math

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
    for i in range(self.GRID_LENGTH):
      print(self.GAME_BOARD[i])
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

      # have player generate their move 
      x, y = self.player[player_counter].make_choice()

      # register players move with board
      self.register_move(player_counter, x, y)

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
    print("right diag list", right_diag_list)
    self.pretty_print_game()
    print("after reverse", right_diag_list)

    # - horizontal
    horizontal_list = list(np_game_board[y])

    # | vertical
    vertical_list = list(np_game_board[:, x])

    return left_diag_list, right_diag_list, horizontal_list, vertical_list


  def coordinates_in_2d_plane_to_right_diagonal_position(self, x_cor: int, y_cor: int) -> int:
    postion = 0

    center_index = (self.GRID_LENGTH - 1) / 2

    x_offset_from_center = center_index - x_cor
    y_offset_from_center = center_index - y_cor
    diagonal_offset = abs(x_offset_from_center - y_offset_from_center)
    print("diagonal offset", diagonal_offset)

    # equation to find num elements at given diagonal
    num_elements_in_diagonal = -abs(center_index - diagonal_offset) - diagonal_offset + 1
    print("num elements", num_elements_in_diagonal)

    # the more extreme the difference between these two the futher the point is from the left diagonal
    offset_difference = abs(x_offset_from_center) - abs(y_offset_from_center)
    # if offset_difference > 0:
    #   position = num_elements_in_diagonal / 2
    # else:
    #   postition

      


    return postion

  def coordinates_in_2d_plane_to_left_diagonal_position(self, x_cor, y_cor):

    generated_list_of_coordinates = [] 
    # each position within the diagonal will always have their x_cor and y_cor sum to the same thing
    postion = 0

    # abs(grid_size - x + y) = num elements in diagonal
    self.grid_length - x_cor + y_cor



    return postion


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
      # for now I'm going to use a naive approach to finding the five in a row 
      # where I will just find the longest string of player_id and return true if 
      # there is one greater than 4
      # TODO: there is a more optimized way to do this
      highest_sequence = 0

      for intersection_value in raw_list:
        if intersection_value == player_id:
          highest_sequence += 1
        else: 
          highest_sequence = 0
        
        if highest_sequence > 4:
          self.game_log.append(("WIN", player_id))
          return True 
      
      print("highest sequence: ", highest_sequence)
    
    return False

  def capture_capturable_surrounding_stones(self) -> None:
    """NAME: capture_capturable_surrounding_stones

    DESC: using the directional lists from the last played point, check if the most recent play created a 
          sequence of (placed stone -> two stones with same id -> another stone with same id value as placed stone)
          if so delete the two middle stones. All directions will be checked. 
    """

    _, player_id, intersection_x_played_on, intersection_y_played_on = self.get_last_move()

    left_diag_list, right_diag_list, horizontal_list, vertical_list = self.get_directional_lists_from_point(intersection_x_played_on, intersection_y_played_on)

    # package into list in order to cut down on repeated code
    # shape: [(index_of_new_placement, the list)]
    print()
    print("right list", right_diag_list)
    print("place index: ", intersection_x_played_on)
    raw_lists = [
      (intersection_y_played_on, left_diag_list),   #TODO fix diag coordinate system
      (intersection_y_played_on,  right_diag_list),  
      (intersection_x_played_on, horizontal_list), 
      (intersection_y_played_on, vertical_list)
    ]
    for raw_list_index, (place_index, raw_list) in enumerate(raw_lists):
      print()
      print("raw list index", raw_list_index)
      print("raw_list", raw_list)
      if len(raw_list) >= 4: # not worth considering rows which cant contain enough stones to make a capture sequence 
        # ls_values will contain all values to the left of the placement index, rs_values to the right
        ls_values = raw_list[:place_index]
        rs_values = raw_list[place_index + 1:] # NOTE: adding 1 to make rs non-inclusve to placement spot

        print("ls vals", ls_values)
        print("rs values", rs_values)
        print("place index", place_index)
        # for the "left" side values 
        if len(ls_values) >= 3 and ls_values[place_index - 3] != player_id:
          non_curr_player_id = ls_values[-1]

          print("ls -2", ls_values[-2])
          print("ls -3", ls_values[-3])
          print(ls_values)

          if ls_values[-2] == non_curr_player_id and ls_values[-3] == player_id:
            # then pieces at indices -2 and -1 should be "captured", 
            # base on the raw list index, "direction" of list, replace game_board values 
            if raw_list_index == 0: # left diagonal 
              self.GAME_BOARD[intersection_y_played_on - 1][intersection_x_played_on - 1] = 0
              self.GAME_BOARD[intersection_y_played_on - 2][intersection_x_played_on - 2] = 0
            elif raw_list_index == 1: # right diagonal 
              print("in ls right diag")
              print(intersection_x_played_on)
              print(intersection_y_played_on)
              self.GAME_BOARD[intersection_y_played_on - 1][intersection_x_played_on + 1] = 0
              self.GAME_BOARD[intersection_y_played_on - 2][intersection_x_played_on + 2] = 0
            elif raw_list_index == 2: # horizontal
              self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on - 1] = 0
              self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on - 2] = 0
            elif raw_list_index == 3: # vertical 
              self.GAME_BOARD[intersection_y_played_on - 1][intersection_x_played_on] = 0
              self.GAME_BOARD[intersection_y_played_on - 2][intersection_x_played_on] = 0
            

        # for the "right" side values 
        if len(rs_values) >= 3 and rs_values[0] != player_id:
          non_curr_player_id = rs_values[0]

          if rs_values[1] == non_curr_player_id and rs_values[2] == player_id:
            # then pieces at indices -2 and -1 should be "captured", 
            # base on the raw list index, "direction" of list, replace game_board values 
            if raw_list_index == 0: # left diagonal 
              self.GAME_BOARD[intersection_y_played_on + 1][intersection_x_played_on + 1] = 0
              self.GAME_BOARD[intersection_y_played_on + 2][intersection_x_played_on + 2] = 0
            elif raw_list_index == 1: # right diagonal 
              print("in rs right diag")
              print(intersection_x_played_on)
              print(intersection_y_played_on)
              self.GAME_BOARD[intersection_y_played_on + 1][intersection_x_played_on - 1] = 0
              self.GAME_BOARD[intersection_y_played_on + 2][intersection_x_played_on - 2] = 0
            elif raw_list_index == 2: # horizontal
              self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on + 1] = 0
              self.GAME_BOARD[intersection_y_played_on][intersection_x_played_on + 2] = 0
            elif raw_list_index == 3: # vertical 
              self.GAME_BOARD[intersection_y_played_on + 1][intersection_x_played_on] = 0
              self.GAME_BOARD[intersection_y_played_on + 2][intersection_x_played_on] = 0

    

  def start(self, num_players: int):
    # order of players in players array determines order, randomize for consistancy
    random.shuffle(self.players())

    self.main_game_loop()

    self.finish()
  

  def finish(self):
    """After the game is over, write data to file"""
    pass



class Player():
  def __init__(self, player_id: int, play_type_option: str) -> None:
    self.player_id = player_id # each player gets an id 

    self.PLAY_DESCISION_OPTIONS = {
      "RANDOM": 0,
      "AI": 1,
      "PLAYER": 99
    }

    # selected play type option
    if list(self.PLAY_DESCISION_OPTIONS.keys()).count(play_type_option) == 1:
      self.selected_play_type_option = self.PLAY_DESCISION_OPTIONS[play_type_option]
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

    if self.selected_play_type_option == self.PLAY_DESCISION_OPTIONS["RANDOM"]:
      random.shuffle(current_choices)
      choice = current_choices[0] 

    elif self.selected_play_type_option == self.PLAY_DESCISION_OPTIONS["AI"]:
      # TODO: implement model
      pass 

    elif self.selected_play_type_option == self.PLAY_DESCISION_OPTIONS["PLAYER"]:
      # TODO: implement player
      pass 

    return choice 


if __name__ == "__main__":
  game = PenteGame()
  game.start(2)