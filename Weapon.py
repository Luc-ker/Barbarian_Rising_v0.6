import sqlite3
import os

def get_weapon_stats(weapon, level):
  if os.path.exists("./Data/weapon_stats.db"):
    connection = sqlite3.connect("./Data/weapon_stats.db")
  else:
    raise FileNotFoundError("/Data/weapon_stats.db was not found.")
  sqlCommand = f"""SELECT * FROM {weapon} WHERE level = {level};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

def get_weapon_info(weapon):
  if os.path.exists("./Data/weapon_info.db"):
    connection = sqlite3.connect("./Data/weapon_info.db")
  else:
    raise FileNotFoundError("/Data/weapon_info.db was not found.")
  sqlCommand = f"""SELECT * FROM WEAPONS WHERE internal_name = "{weapon}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]  

def get_weapon_from_id(id):
  if os.path.exists("./Data/weapon_info.db"):
    connection = sqlite3.connect("./Data/weapon_info.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM WEAPONS WHERE id = "{id}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0][1]

def get_max_level(weapon):
  if os.path.exists("./Data/weapon_stats.db"):
    connection = sqlite3.connect("./Data/weapon_stats.db")
  else:
    raise FileNotFoundError("/Data/weapon_stats.db was not found.")
  sqlCommand = f"""SELECT level FROM {weapon};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[-1][0] 

class Weapon():
  internal_name = ""
  display_name = ""
  type = ""
  description = ""

  def __init__(self, weapon, level):
    details = get_weapon_info(weapon)
    if type(details) != tuple:
      raise TypeError
    
    self.id = details[0]
    self.level = level
    self.internal_name = details[1]
    self.display_name = details[2]
    self.type = details[3]
    self.stats = {}
    affected_stats = details[4].split(",")
    stats = get_weapon_stats(weapon, level)[2].split(":")
    for i,stat in enumerate(affected_stats):
      self.stats.update({stat: f"{stats[i]}"})
    self.description = details[6]
    percentages = list(self.stats.values())
    if len(percentages) > 1:
      percentages = f"{'%, '.join(percentages[:-1])}% and {percentages[-1]}%"
    else:
      percentages = f"{percentages[0]}%"
    self.description = self.description.replace("{percent}", percentages)

  def can_upgrade(self, player):
    if self.max_level():
      return 6
    if player.th < self.level:
      return 4
    cost = get_weapon_stats(self.internal_name, self.level+1)[1].split(":")
    if player.gold < int(cost[0]) or player.weapon_ore < int(cost[1]):
      return 5
    return 3

  def level_up(self, player, levels=1):
    for i in range(levels):
      cost = get_weapon_stats(self.internal_name, self.level+i+1)[1].split(":")
      player.gold -= int(cost[0])
      player.weapon_ore -= int(cost[1])
    self.level += levels
    self = self.__init__(self.internal_name, self.level)

  def max_level(self):
    return self.level >= get_max_level(self.internal_name)
    