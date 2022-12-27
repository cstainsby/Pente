import pytest 

from pente import PenteGame


# ------------------------------------------------------------------
# helper functions
# ------------------------------------------------------------------
def init_empty_game(x_len, y_len):
  game = PenteGame()
  game.GAME_BOARD = [([0] * x_len) for i in range(y_len)]

  return game


# ------------------------------------------------------------------
# test initialization
# ------------------------------------------------------------------
def test_initialization():
  for i in range(100):
    for j in range(100):
      game = init_empty_game(i, j)

      assert game


# ------------------------------------------------------------------
# test placement 
# ------------------------------------------------------------------
def test_single_placement():
  game = init_empty_game(9, 9)
  game.register_move(1, 4, 2)
  
  assert game.GAME_BOARD[2][4] == 1


def test_multiple_placements():
  game = init_empty_game(9, 9)
  game.register_move(1, 4, 2)
  game.register_move(2, 5, 7)
  game.register_move(1, 1, 8)
  game.register_move(2, 3, 2)
  game.register_move(1, 4, 4)
  game.register_move(2, 6, 2)
  game.register_move(1, 6, 7)
  game.register_move(2, 1, 1)
  game.register_move(1, 0, 7)
  game.register_move(2, 8, 8)
  
  assert game.GAME_BOARD[2][4] == 1

def test_placement_out_of_bounds():
  game = init_empty_game(9, 9)
  assert game.register_move(1, 9, 9) == IndexError
  assert game.register_move(1, -1, 4) == IndexError
  assert game.register_move(1, 5, -100) == IndexError


def test_placement_with_invalid_type():
  game = init_empty_game(9, 9)
  assert game.register_move(1, "squirrel", 2) == TypeError


def test_placement_on_an_occupied_intersection():
  game = init_empty_game(9, 9)
  game.register_move(1, 5, 7)
  
  assert game.GAME_BOARD[7][5] == 1
  
  assert game.register_move(2, 5, 7) == ValueError


# ------------------------------------------------------------------
#  test check five 
# ------------------------------------------------------------------
def test_empty_board_check_five():
  game = init_empty_game(9, 9)

  # add a move so that check works
  game.game_log.append(
    (
      0, # player_id
      3, # x_position 
      5  # y_position
    )
  )

  assert game


# ------------------------------------------------------------------
#  test captures
# ------------------------------------------------------------------
# def test_no_capture():
#   game = init_empty_game(9, 9)
#   game.register_move(0, 4, 2)

#   BEFORE_GAME_STATE = game.GAME_BOARD

#   game.capture_capturable_surrounding_stones()

#   AFTER_GAME_STATE = game.GAME_BOARD

#   assert BEFORE_GAME_STATE == AFTER_GAME_STATE


