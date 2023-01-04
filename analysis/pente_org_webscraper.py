# --------------------------------------------------------------------------
# FILE: pente_org_webscraper.py
# NAME: Cole Stainsby
# DESC: A python script which generates scrapes game data off of pente.org
# --------------------------------------------------------------------------

from bs4 import BeautifulSoup as bs
import requests
import time

from pente_org_certs import pente_org_certs # a separte .py file containing a dictionary with login info

USERNAME = pente_org_certs["username"]
PASSWORD = pente_org_certs["password"]


def log_in(session: requests.Session):
  """NAME: log_in()

  DESC: if while trying to scrape data, we are blocked by a signin request
        post the login info held in pente_org_certs
  """
  sign_in_payload = {
    "name2": USERNAME,
    "password2": PASSWORD
  }

  res = session.post("https://pente.org/gameServer/index.jsp", data=sign_in_payload)

  return session

def write_data_to_file(game_id: int, game_data: str):
  file_path = "data/game{}".format(game_id)
  with open(file_path, "w") as new_file:
    new_file.write(game_data)

def get_data_at_req_endpoint(session: requests.Session, id: int):
  """NAME: get_data_at_req_endpoint()

  DESC: brute force method for getting all the data, this will only need to be run
        once so no real need to optimize it 

  RETS: 
    data(str or None): string representation of game or None if id doesn't exist 
  """
  data = None

  numeric_base_identifier = 50000000000000
  data_id = numeric_base_identifier + id
  base_req_url = "https://pente.org/gameServer/pgn.jsp?g={}".format(data_id)

  # NOTE: no need to parse for info using beautifulsoup, 
  #       source is a plaintext representation of exactly what we need
  source = session.get(base_req_url).text

  # do a check, some of the endpoints in this list will be null
  # if that is the case return None
  soup = bs(source, "html.parser")
  title = soup.find("title")
  if title == None:
    data = source

  return data



def main():
  session = requests.Session()

  # attempt a request for data, if not signed in sign in
  session = log_in(session)

  for game_id in range(2352, 543842): # this number is the highest the database currently goes to
    time.sleep(0.5) # to be kind on their servers
    print("current game id", game_id)
    data = get_data_at_req_endpoint(session, game_id)

    if data:
      write_data_to_file(game_id, data)


if __name__ =="__main__":
  main()