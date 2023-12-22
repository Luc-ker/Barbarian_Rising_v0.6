import sqlite3
import os

def get_base_stats(power, level):
  if os.path.exists("./Data/power_stats.db"):
    connection = sqlite3.connect("./Data/power_stats.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM {power} WHERE level = {level};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

def get_power_info(power):
  if os.path.exists("./Data/power_info.db"):
    connection = sqlite3.connect("./Data/power_info.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM POWERS WHERE internal_name = "{power}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

def get_power_from_id(id):
  if os.path.exists("./Data/power_info.db"):
    connection = sqlite3.connect("./Data/power_info.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM POWERS WHERE id = "{id}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0][1]

def get_max_level(power):
  if os.path.exists("./Data/power_stats.db"):
    connection = sqlite3.connect("./Data/power_stats.db")
  else:
    raise FileNotFoundError("/Data/power_stats.db was not found.")
  sqlCommand = f"""SELECT level FROM {power};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[-1][0] 
  
class Power():
  def __init__(self, power, level=1, cooldown=None):
    power = power.upper().replace(" ","")
    info = get_power_info(power)
    dbstats = get_base_stats(power, level)
    if type(info) != tuple:
      raise TypeError
  
    self.id = info[0]
    self.internal_name = info[1]
    self.display_name = info[2]
    self.initial_cooldown = info[3]
    if cooldown is None:
      self.cooldown = 0
    else:
      self.cooldown = cooldown
    self.type = info[4]
    self.element = info[5]
    self.shield_damage = info[6]
    self.target = info[7]
    self.description = info[8]
    self.power = dbstats[1]
    self.level = level
    self.description = self.description.replace("{power}", str(self.power))

  def __str__(self):
    return self.display_name
  
  def reset_cooldown(self):
    self.cooldown = self.initial_cooldown

  def on_cooldown(self):
    return self.cooldown > 0

  def can_upgrade(self, player):
    if self.can_evolve(player):
      return 5
    if self.max_level():
      return 4
    stats = get_base_stats(self.internal_name, self.level+1)
    th_req = stats[-2]
    cost = stats[-1]
    if player.th < th_req:
      return 2
    if player.elixir < cost:
      return 3
    return 1

  def level_up(self, player, levels=1):
    for i in range(levels):
      stats = get_base_stats(self.internal_name, self.level+i+1)
      player.elixir -= stats[-1]
    self.level += levels
    self = self.__init__(self.internal_name, self.level)

  def max_level(self):
    return self.level == get_max_level(self.internal_name)

  def can_evolve(self, player):
    evoData = get_power_info(self.internal_name)[9].split(",")    
    if evoData == [""]:
      return False
    cost = int(evoData[2])
    return (self.max_level and player.d_elixir >= cost)

  def evolve(self, player):
    evoData = get_power_info(self.internal_name)[9].split(",")
    player.d_elixir -= int(evoData[2])
    self = Power(evoData[0])
    return self


