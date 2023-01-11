
import sqlite3
import os

from database import PenteDatabase
from ..pente.pente import PenteGame


TEST_DB_NAME = "test_db.db"
test_db = PenteDatabase(TEST_DB_NAME)

def test_post_game():


  test_db



# clean up database
os.remove(TEST_DB_NAME)