import pytest 

from pente import PenteGame


# ------------------------------------------------------------------
# test initialization
# ------------------------------------------------------------------
def test_initialization():
  for i in range(3, 100, 2):
    print(i)
    game = PenteGame(i)

    assert game.GRID_LENGTH == i
    assert game.GAME_BOARD == [[0 for i in range(game.GRID_LENGTH)] for j in range(game.GRID_LENGTH)]

    assert len(game.players) == 2
    assert game.current_player_turn == 0
    assert game.pairs_captured == [0] * 2
    assert len(game.game_log) == 0
    
# ------------------------------------------------------------------
# test placement 
# ------------------------------------------------------------------
def test_single_placement():
  game = PenteGame(9)
  game.register_move(1, 4, 2)
  
  assert game.GAME_BOARD[2][4] == 1


def test_multiple_placements():
  game = PenteGame(9)

  placement_coordinates = {
    1: [(4,2), (5,7), (1,8), (3,2), (4,4), (6,2), (6,7), (1,1), (0,7), (8,8)],
    2: [(3,3)]
  }

  for player_key in placement_coordinates.keys():
    for x, y in placement_coordinates[player_key]:
      game.register_move(player_key, x, y)

  print(game.GAME_BOARD)

  for i in range(9):
    for j in range(9):
      if placement_coordinates[1].count((j, i)) == 1:
        assert game.GAME_BOARD[i][j] == 1
      elif placement_coordinates[2].count((j, i)) == 1:
        assert game.GAME_BOARD[i][j] == 2
      else: 
        assert game.GAME_BOARD[i][j] == 0
  

def test_placement_out_of_bounds():
  game = PenteGame(9)
  assert game.register_move(1, 9, 9) == IndexError
  assert game.register_move(1, -1, 4) == IndexError
  assert game.register_move(1, 5, -100) == IndexError


def test_placement_with_invalid_type():
  game = PenteGame(9)
  assert game.register_move(1, "squirrel", 2) == TypeError


def test_placement_on_an_occupied_intersection():
  game = PenteGame(9)
  game.register_move(1, 5, 7)
  
  assert game.GAME_BOARD[7][5] == 1
  
  assert game.register_move(2, 5, 7) == ValueError

# ------------------------------------------------------------------
#  test get last move
# ------------------------------------------------------------------

def test_get_last_move():
  game = PenteGame(9)

  # no moves played 
  assert game.get_last_move() == None 

  game.register_move(1, 1, 4)

  print(game.game_log)
  print(len(game.game_log))
  assert game.get_last_move() == ("PLACEMENT", 1, 1, 4)

def test_get_last_move_after_multiple_moves():
  game = PenteGame(9)

  # no moves played 
  assert game.get_last_move() == None 

  game.register_move(1, 1, 4)
  game.register_move(2, 3, 2)
  game.register_move(1, 7, 6)
  game.register_move(2, 5, 5)

  print(game.game_log)
  print(len(game.game_log))
  assert game.get_last_move() == ("PLACEMENT", 2, 5, 5)


def test_get_last_move_after_multiple_moves_and_capture():
  game = PenteGame(9)

  # no moves played 
  assert game.get_last_move() == None 

  game.register_move(1, 1, 4)
  game.register_move(2, 3, 2)
  game.register_move(1, 7, 6)
  game.register_move(2, 5, 5)

  game.game_log.append(("CAPTURE", 1, [
    (1,2), (2,2), (3,2), (4,2)
  ])) # manually add a capture log

  print(game.game_log)
  print(len(game.game_log))
  assert game.get_last_move() == ("PLACEMENT", 2, 5, 5)

# ------------------------------------------------------------------
#  test get directional lists from point 
# ------------------------------------------------------------------
def test_empty_board():
  game = PenteGame(9)

  # from center 
  left_diag_list, right_diag_list, horizontal_list, vertical_list = game.get_directional_lists_from_point(4, 4)
  assert len(left_diag_list) == 9
  assert len(right_diag_list) == 9
  assert len(horizontal_list) == 9
  assert len(vertical_list) == 9
  assert left_diag_list.count(0) == 9
  assert right_diag_list.count(0) == 9
  assert horizontal_list.count(0) == 9
  assert vertical_list.count(0) == 9

  # from top left corner
  left_diag_list, right_diag_list, horizontal_list, vertical_list = game.get_directional_lists_from_point(0, 0)
  assert len(left_diag_list) == 9
  assert len(right_diag_list) == 1
  assert len(horizontal_list) == 9
  assert len(vertical_list) == 9
  assert left_diag_list.count(0) == 9
  assert right_diag_list.count(0) == 1
  assert horizontal_list.count(0) == 9
  assert vertical_list.count(0) == 9

# ------------------------------------------------------------------
#  test check five 
# ------------------------------------------------------------------
def test_basic_board_check_five():

  # test all directions
  # horizontal
  game = PenteGame(9)
  for i in range(5):
    game.register_move(1, i, 5)
  
  print(game.game_log[-1])
  assert game.check_five_in_a_row() == True

  # vertical
  game = PenteGame(9)
  for i in range(5):
    game.register_move(1, 5, i)
  
  assert game.check_five_in_a_row() == True

  # left diagonal 
  game = PenteGame(9)
  for i in range(5):
    game.register_move(1, i + 1, i)
  
  assert game.check_five_in_a_row() == True 

  # right diagonal 
  game = PenteGame(9)
  for i in range(5):
    game.register_move(1, 8 - i, i)
  
  assert game.check_five_in_a_row() == True 

def test_negative_check_five():

  game = PenteGame(9)

  assert game.check_five_in_a_row() == False

  for i in range(4):
    game.register_move(1, i + 1, i)
  
  assert game.check_five_in_a_row() == False

def test_with_other_player_plays_check_five():

  # positive example
  game = PenteGame(9)
  for i in range(4):
    game.register_move(1, i + 1, i)
  game.register_move(2, 6, 5)
  game.register_move(1, 5, 4) # must be the most recently registered move for check to work
  
  assert game.check_five_in_a_row() == True 


  # negative example
  game = PenteGame(9)
  for i in range(4):
    game.register_move(1, i + 1, i)
  game.register_move(2, 5, 4) # this will block the sequence
  game.register_move(1, 6, 5) # must be the most recently registered move for check to work
  
  assert game.check_five_in_a_row() == False

# ------------------------------------------------------------------
#  test coordinate postion to diagonal position conversions
# ------------------------------------------------------------------
def test_right_diagonal_conversion():
  game = PenteGame(9)
  game.register_move(1, 3, 2)
  game.pretty_print_game()
  assert game.coordinates_in_2d_plane_to_right_diagonal_position(3, 2) == 3 # index 3 of 5 total indices
  

# ------------------------------------------------------------------
#  test captures
# ------------------------------------------------------------------
# def test_no_expected_captures():
#   game = PenteGame(9)
#   game.register_move(1, 4, 2)

#   BEFORE_GAME_STATE = game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert BEFORE_GAME_STATE == AFTER_GAME_STATE


# def test_simple_capture_vertical_above():

#   game = PenteGame(9)
#   game.register_move(1, 4, 2)
#   game.register_move(2, 4, 3)
#   game.register_move(2, 4, 4)
#   game.register_move(1, 4, 5) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 4, 2)
#   expected_game.register_move(1, 4, 5)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE


# def test_simple_capture_vertical_below():

#   game = PenteGame(9)
#   game.register_move(1, 4, 5)
#   game.register_move(2, 4, 3)
#   game.register_move(2, 4, 4)
#   game.register_move(1, 4, 2) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 4, 2)
#   expected_game.register_move(1, 4, 5)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE

# def test_simple_capture_horizontal_left():

#   game = PenteGame(9)
#   game.register_move(1, 3, 2)
#   game.register_move(2, 4, 2)
#   game.register_move(2, 5, 2)
#   game.register_move(1, 6, 2) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 3, 2)
#   expected_game.register_move(1, 6, 2)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE

# def test_simple_capture_horizontal_right():

#   game = PenteGame(9)
#   game.register_move(1, 6, 2)
#   game.register_move(2, 4, 2)
#   game.register_move(2, 5, 2)
#   game.register_move(1, 3, 2) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 3, 2)
#   expected_game.register_move(1, 6, 2)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE

# def test_simple_capture_left_diagonal_left():

#   game = PenteGame(9)
#   game.register_move(1, 3, 2)
#   game.register_move(2, 4, 3)
#   game.register_move(2, 5, 4)
#   game.register_move(1, 6, 5) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 3, 2)
#   expected_game.register_move(1, 6, 5)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE

# def test_simple_capture_left_diagonal_left():

#   game = PenteGame(9)
#   game.register_move(1, 6, 5)
#   game.register_move(2, 4, 3)
#   game.register_move(2, 5, 4)
#   game.register_move(1, 3, 2) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 3, 2)
#   expected_game.register_move(1, 6, 5)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE

# def test_simple_capture_right_diagonal_left():

#   game = PenteGame(9)
#   game.register_move(2, 2, 7)
#   game.register_move(1, 3, 6)
#   game.register_move(2, 4, 5)
#   game.register_move(2, 5, 4)
#   game.register_move(1, 6, 3) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 3, 6)
#   expected_game.register_move(1, 6, 3)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE

# def test_simple_capture_right_diagonal_right():

#   game = PenteGame(9)
#   game.register_move(1, 2, 3)
#   game.register_move(2, 4, 5)
#   game.register_move(2, 3, 4)
#   game.register_move(1, 5, 6) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 3, 6)
#   expected_game.register_move(1, 2, 3)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()
#   game.pretty_print_game()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE

# def test_multiple_capture():
#   game = PenteGame(9)
#   game.register_move(1, 4, 2)
#   game.register_move(2, 4, 3)
#   game.register_move(2, 4, 4)
#   game.register_move(2, 5, 6)
#   game.register_move(2, 6, 7)
#   game.register_move(1, 4, 5) # capturing move
#   game.pretty_print_game()

#   expected_game = PenteGame(9)
#   expected_game.register_move(1, 4, 2)
#   expected_game.register_move(1, 4, 5)
#   EXPECTED_GAME_STATE = expected_game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert EXPECTED_GAME_STATE == AFTER_GAME_STATE


# ------------------------------------------------------------------
#  test players
# ------------------------------------------------------------------

def test_player_initialization():
  pass