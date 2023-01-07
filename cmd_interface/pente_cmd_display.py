
import requests 
import sys 
import os
import keyboard


# NOTE: this will only work on linux for now
class PenteCmdDisplay():
  def __init__(self) -> None:
    self.current_page_build_func = self.splash_page

    # after each printing of a screen this variable will be set, 
    #   if true the game will feild input from the user
    self.expect_input = True 

    self.terminal_cols, self.terminal_rows = os.get_terminal_size() 

    continuePlaying = True
    page_res = None 

    self.refresh_current_page(message=None)

    while continuePlaying:
      
      if (self.terminal_cols, self.terminal_rows) != os.get_terminal_size():
        self.refresh_current_page(message=None)
        self.terminal_cols, self.terminal_rows = os.get_terminal_size() 

    if page_res:
      if self.current_page_build_func == self.splash_page:
        if page_res = 1: # play online 
          pass
        elif page_res == 2:
          pass
        else:
          self.refresh_current_page("")
           

    page_res = None


  def refresh_current_page(self, message):
    """Helper function to rebuild the page after user input"""
    os.system("clear")
    self.current_page_build_func()


  def splash_page(self):
    page = ""
    indent = " " * int(self.terminal_cols / 6)
    options = {
      1: "Play Online",
      2: "Play AI"
    }

    page += self.build_header("Welcome to Pente!")

    for option_num, option_label in options.items():
      page += indent + str(option_num) + ") " + option_label + "\n"

    print(page)
    user_input = input("\nSelect by typing in num: ")
    return user_input
    
  
  def online_game_selection_page(self):
    page = ""
    indent = " " * int(self.terminal_cols / 6)
    options = { # fill with games avalible to current player
      
    }

    page += self.build_header("Welcome to Pente!")

    for option_num, option_label in options.items():
      page += indent + str(option_num) + ") " + option_label + "\n"

    print(page)
    user_input = input("\nSelect by typing in num: ")
    return user_input

  
  def build_header(self, title_contents: str) -> str:
    spacing = " " * int((self.terminal_cols / 2 - len(title_contents) / 2) - 1)

    header = "-" * self.terminal_cols + "\n"
    header += "|" + spacing + title_contents + spacing + "|" + "\n"
    header += "-" * self.terminal_cols + "\n"

    return header
    


if __name__=="__main__":
  display = PenteCmdDisplay()
  