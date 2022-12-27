
from pente import PenteGame

class EventListener():
  
  def __init__(self) -> None:
    self.subscribers = []

  def post():

    pass

  def subscribe(self):
    pass

class PenteCmdDisplay():
  
  def __init__(self) -> None:
    self.game = PenteGame()
    self.listner = EventListener()

    num_players = input("How Many Players Would You Like:")

    self.game.start(num_players)
  


  def update_display(self):
    pass