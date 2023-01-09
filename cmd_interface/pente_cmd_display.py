# --------------------------------------------------------------------------
# FILE: pente_cmd_display.py
# NAME: Cole Stainsby
# DESC: One of the possible ways to interact with the app, I have chosen 
#       to build this as a way to quickly setup a interface where I can 
#       test functionality
# --------------------------------------------------------------------------

import sys 
import os

import pente_request_utils


# NOTE: this will only work on linux for now
class PenteCmdDisplay():
  def __init__(self) -> None:
    self.pages = {
      "splash_page": {
        "options": {
          1: "Play Online",
          2: "Play AI"
        },
        "print_function": self.splash_page_print,
        "input_questions": ["Select numbered option:"],
        "input_function": self.splash_page_get_input
      },

      "online_game_selection_page": {
        "options": {
          'b': "Back",
          'n': "Make A Lobby"
        },
        "print_function": self.online_game_selection_page_print,
        "input_questions": ["""
            Choose Game by number or enter "n" to make your own \n
            \t-> """],
        "input_function": self.online_game_selection_get_input
      },
      
      "post_game_page": {
        "options": {
          'b': "Back"
        },
        "print_function": self.post_game_page_print,
        "input_questions": [
            """
              Game Name: \n
              \t-> """,
            """
              Number Of Players in Game: \n
              \t-> """
          ],
        "input_function": self.post_game_get_input
      }
    }

    self.current_page = "splash_page"

    self.terminal_cols, self.terminal_rows = os.get_terminal_size() 

    continuePlaying = True

    self.refresh_page()

    while continuePlaying:
      page_res = None 
      
      # If the window size is adjusted change the print to reflect that
      if (self.terminal_cols, self.terminal_rows) != os.get_terminal_size():
        self.refresh_page()
        self.terminal_cols, self.terminal_rows = os.get_terminal_size() 
      
      # get user input 
      page_res = self.pages[self.current_page]["input_function"]()

      if page_res:
        # based on what page youre on
        #   unpack the response
        #   act on information provided by user

        if self.current_page == "splash_page":
          if page_res == 1: # switch to online search for games
            self.switch_page("online_game_selection_page")
          elif page_res == 2: # switch to in game page with AI
            pass
        
        elif self.current_page == "online_game_selection_page":
          if page_res == 'b':
            self.switch_page("splash_page")
          elif page_res == 'n':
            self.switch_page("post_game_page")
        
        elif self.current_page == "post_game_page":
          game_name = page_res[0]
          num_players = page_res[1]
          print("uploading game: ", page_res)

          # Post the game to the backend



          
          


  # ----------------------------------------------------------------------------------
  #   Splash Page
  # ----------------------------------------------------------------------------------
  def splash_page_print(self):
    page_info = self.pages["splash_page"]
    page = ""
    indent = " " * int(self.terminal_cols / 6)

    page += self.build_header("Welcome to Pente!")

    for option_num, option_label in page_info["options"].items():
      page += indent + str(option_num) + ") " + option_label + "\n"

    print(page)
  
  def splash_page_get_input(self):
    answers = []
    page_info = self.pages["splash_page"]
    
    questions = page_info["input_questions"]
    for question in questions:
      choice = int(input(question))
      answers.append(choice)

    # verify that the info is of the correct type
    #   return None if invalid
    answer = answers[0] # NOTE always only one answer
    if not (answer == 1 or answer == 2):
      answer = ValueError

    return answer
  
  # ----------------------------------------------------------------------------------
  #   Online Game Selection Page
  # ----------------------------------------------------------------------------------
  def online_game_selection_page_print(self):
    page_info = self.pages["online_game_selection_page"]
    page = ""
    indent = " " * int(self.terminal_cols / 6)

    page += self.build_header("Game Dashboard")

    for option_num, option_label in page_info["options"].items():
      page += indent + str(option_num) + ") " + option_label + "\n"

    print(page)

    # TODO get list of availble games and update options 

    print("\nAvailable Games") 
    # wait for response 
    games = pente_request_utils.get_joinable_games()

    print("games:", games)


  def online_game_selection_get_input(self):
    answers = []
    page_info = self.pages["online_game_selection_page"]
    
    questions = page_info["input_questions"]
    for question in questions:
      choice = input(question)

      if choice == 'b':
        return choice

      answers.append(choice)

    # verify that the info is of the correct type
    #   return None if invalid
    answer = answers[0] # NOTE always only one answer
    
    # if the answer isn't 'n' or 1 or 2
    if not (answer == 'n' or answer == 'b' or int(answer) == 1 or int(answer) == 2):
      answer = ValueError

    return answer

  # ----------------------------------------------------------------------------------
  #   Online Game Selection Page
  # ----------------------------------------------------------------------------------
  def post_game_page_print(self):
    page_info = self.pages["post_game_page"]
    page = ""
    indent = " " * int(self.terminal_cols / 6)

    page += self.build_header("Create Game")

    for option_num, option_label in page_info["options"].items():
      page += indent + str(option_num) + ") " + option_label + "\n"

    pente_request_utils.get_joinable_games()

    print(page)
  
  def post_game_get_input(self):
    answers = []
    page_info = self.pages["post_game_page"]
    
    questions = page_info["input_questions"]
    for question in questions:
      choice = input(question)

      if choice == 'b':
        return choice

      answers.append(choice)

    # verify that the info is of the correct type
    #   return None if invalid
    res = []
    second_answer = int(answers[1]) # NOTE only the second awnser needs to be checked
    
    # if the answer isn't 'n' or 1 or 2
    if not (int(second_answer) < 5):
      res = ValueError
    else:
      res = [answers[0], int(answers[1])]

    return res


  

  # ----------------------------------------------------------------------------------
  #   Utilities
  # ----------------------------------------------------------------------------------
  def build_header(self, title_contents: str) -> str:
    spacing = " " * int((self.terminal_cols / 2 - len(title_contents) / 2) - 1)

    header = "-" * self.terminal_cols + "\n"
    header += "|" + spacing + title_contents + spacing + "|" + "\n"
    header += "-" * self.terminal_cols + "\n"

    return header

  def build_game_portrait(self, creator_name: str, current_player_count: int):
    pass


  def refresh_page(self):
    os.system("clear")
    self.pages[self.current_page]["print_function"]()
  
  def switch_page(self, new_page_name: str):
    self.current_page = new_page_name
    self.refresh_page()
    


if __name__=="__main__":
  display = PenteCmdDisplay()
  