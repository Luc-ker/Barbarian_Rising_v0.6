import sqlite3
import os

def get_stats(ability):
  if os.path.exists("./Data/ability_info.db"):
    connection = sqlite3.connect("./Data/ability_info.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM ABILITIES WHERE internal_name = "{ability}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

class Ability():
  internal_name = ""
  display_name = ""
  description = ""

  def __init__(self, ability):
    details = get_stats(ability)
    if type(details) != tuple:
      raise TypeError

    self.internal_name = details[0]
    self.display_name = details[1]
    self.trigger_timing = details[2]
    self.description = details[3]

  def __str__(self):
    return self.display_name
