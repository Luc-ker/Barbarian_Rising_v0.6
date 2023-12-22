import sqlite3
from Troop import Troop

def get_enemy_names(battle):
  connection_stats = sqlite3.connect("./Data/battle_stats.db")
  connection_info = sqlite3.connect("./Data/battle_info.db")
  cursor_info = connection_info.cursor()
  cursor_stats = connection_stats.cursor()
  
  sqlQueryCommand = f"""SELECT * FROM BATTLES WHERE battle_id = "{battle}";"""
  cursor_info.execute(sqlQueryCommand)
  battle_info = cursor_info.fetchall()[0]
  
  wave_sizes = battle_info[1].split(",")
  id = 0
  names = []
  levels = []
  for wave, wave_size in enumerate(wave_sizes):
    names.append([])
    levels.append([])
    for i in range(int(wave_size)):
      id += 1
      sqlQueryCommand = f"""SELECT * FROM {battle} WHERE id = {id};"""
      cursor_stats.execute(sqlQueryCommand)
      troop = cursor_stats.fetchall()[0]
      names[wave].append(troop[1])
      levels[wave].append(troop[2])
  return names, levels

def create_enemies(battle):
  connection_stats = sqlite3.connect("./Data/battle_stats.db")
  connection_info = sqlite3.connect("./Data/battle_info.db")
  cursor_info = connection_info.cursor()
  cursor_stats = connection_stats.cursor()
  
  sqlQueryCommand = f"""SELECT * FROM BATTLES WHERE battle_id = "{battle}";"""
  cursor_info.execute(sqlQueryCommand)
  battle_info = cursor_info.fetchall()[0]
  
  wave_sizes = battle_info[1].split(",")
  id = 0
  enemies = []
  for wave, wave_size in enumerate(wave_sizes):
    enemies.append([])
    for i in range(int(wave_size)):
      id += 1
      sqlQueryCommand = f"""SELECT * FROM {battle} WHERE id = {id};"""
      cursor_stats.execute(sqlQueryCommand)
      troop_info = cursor_stats.fetchall()[0]
      troop = Troop(troop_info[1], troop_info[2])
      if troop_info[3] != "":
        troop.ability = troop.change_ability(troop_info[3])
      if troop_info[4] != "":
        troop.active_attacks = []
        attacks = troop_info[4].split(",")
        for attack in attacks:
          troop.learn_attack(attack, True)
      enemies[wave].append(troop)
  return enemies

def get_battle_info(battle):
  connection = sqlite3.connect("./Data/battle_info.db")
  cursor = connection.cursor()
  
  sqlQueryCommand = f"""SELECT stamina,reward FROM BATTLES WHERE battle_id = "{battle}";"""
  cursor.execute(sqlQueryCommand)
  return cursor.fetchall()[0]
  
  