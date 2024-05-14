import sqlite3
import os

def add_update():
  if os.path.exists("./Data/times.db"):
    os.remove("./Data/times.db")
  connection = sqlite3.connect("./Data/times.db")
  sqlCreateCommand = """CREATE TABLE IF NOT EXISTS TIMES(
    file varchar(255),
    last_modified float,
    PRIMARY KEY(file)
  );"""
  cursor = connection.cursor()
  cursor.execute(sqlCreateCommand)
  for file in os.listdir("./Stats/"):
    file = f"./Stats/{file}"
    sqlInsertCommand = f"""INSERT INTO TIMES VALUES ("{file}",{os.path.getmtime(file)});"""
    cursor.execute(sqlInsertCommand)
    connection.commit()

def should_update():
  sqlCommand = """SELECT * FROM times;"""
  connection = sqlite3.connect("./Data/times.db")
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  result = cursor.fetchall()
  for file in os.listdir("./Stats/"):
    file = f"./Stats/{file}"
    last_modified = os.path.getmtime(file)
    for i, x in result:
      if i == file and x != last_modified:
        return True
  return False

def update_troop_stats():
  with open("./Stats/troop_stats.txt", "r") as f1:
    if os.path.exists("./Data/troop_stats.db"):
      os.remove("./Data/troop_stats.db")
    connection = sqlite3.connect("./Data/troop_stats.db")
    troop = None
    cursor = connection.cursor()
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[0] == "[":
        connection.commit()
        troop = line[1:-2]
        sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {troop}(
          level int,
          hp int,
          attack int,
          defense int,
          speed int,
          ability_level int,
          PRIMARY KEY(level)
        );"""
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
      else:
        battler = line[:-1].split(",")
        if len(battler) < 9:
          battler = battler + [0] * (9 - len(battler))
        sqlInsertCommand = f"""INSERT INTO {troop} VALUES (
          "{battler[0]}","{battler[1]}","{battler[2]}",
          "{battler[3]}","{battler[4]}","{battler[5]}"
        );"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Troop stats databases updated.")

def update_barb_costs():
  with open("./Stats/barb_costs.txt", "r") as f1:
    if os.path.exists("./Data/barb_costs.db"):
      os.remove("./Data/barb_costs.db")
    connection = sqlite3.connect("./Data/barb_costs.db")
    cursor = connection.cursor()
    troop = None
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif "[" in line:
        troop = line[1:-2]
        sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {troop}(
          level int,
          elixir_cost int,
          gold_cost int,
          PRIMARY KEY(level)
        );"""
        cursor.execute(sqlCreateCommand)
      else:
        costs = line[:-1].split(",")
        sqlInsertCommand = f"""INSERT INTO {troop} VALUES (
          "{costs[0]}","{costs[1]}","{costs[2]}"
        );"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Barb costs databases updated.")

def update_attacks():
  with open("./Stats/attacks.txt", "r") as f1:
    if os.path.exists("./Data/attacks.db"):
      os.remove("./Data/attacks.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS ATTACKS(
      internal_name varchar(255),
      display_name varchar(255),
      element varchar(255),
      power int,
      target varchar(255),
      effect_code varchar(255),
      effect_chance int,
      effect_turns int,
      flags varchar(100),
      shield_damage int,
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/attacks.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    info = []
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[:8] == "IntName:":
        if info != []:
          sqlInsertCommand = f"""INSERT INTO ATTACKS VALUES (
            "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
            "{info[4]}","{info[5]}","{info[6]}","{info[7]}",
            "{info[8]}","{info[9]}","{info[10]}"
          );"""
          cursor.execute(sqlInsertCommand)
          connection.commit()
        info = [""] * 11
        info[0] = line[9:-1]
      elif line[:5] == "Name:":
        info[1] = line[6:-1]
      elif line[:8] == "Element:":
        info[2] = line[9:-1]
      elif line[:6] == "Power:":
        info[3] = line[7:-1]
      elif line[:7] == "Target:":
        info[4] = line[8:-1]
      elif line[:11] == "EffectCode:":
        info[5] = line[12:-1]
      elif line[:13] == "EffectChance:":
        info[6] = line[14:-1]
      elif line[:12] == "EffectTurns:":
        info[7] = line[13:-1]
      elif line[:6] == "Flags:":
        info[8] = line[7:-1]
      elif line[:13] == "ShieldDamage:":
        info[9] = line[14:-1]
      elif line[:12] == "Description:":
        info[10] = line[13:-1]
  if info != []:
    sqlInsertCommand = f"""INSERT INTO ATTACKS VALUES (
      "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
      "{info[4]}","{info[5]}","{info[6]}","{info[7]}",
      "{info[8]}","{info[9]}","{info[10]}"
    );"""
    cursor.execute(sqlInsertCommand)
    connection.commit()
  print("Attack database updated.")

def update_weapon_info():
  with open("./Stats/weapon_info.txt", "r") as f1:
    if os.path.exists("./Data/weapon_info.db"):
      os.remove("./Data/weapon_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS WEAPONS(
      id int,
      internal_name varchar(255),
      display_name varchar(255),
      weapon_type varchar(255),
      stats varchar(255),
      th_available int,
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/weapon_info.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    info = []
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[:3] == "ID:":
        if info != []:
          sqlInsertCommand = f"""INSERT INTO WEAPONS VALUES (
            "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
            "{info[4]}","{info[5]}","{info[6]}"
          );"""
          cursor.execute(sqlInsertCommand)
          connection.commit()
        info = [""] * 7
        info[0] = line[4:-1]
      elif line[:8] == "IntName:":
        info[1] = line[9:-1]
      elif line[:5] == "Name:":
        info[2] = line[6:-1]
      elif line[:5] == "Type:":
        info[3] = line[6:-1]
      elif line[:6] == "Stats:":
        info[4] = line[7:-1]
      elif line[:13] == "TH_available:":
        info[5] = line[14:-1]
      elif line[:12] == "Description:":
        info[6] = line[13:-1]
    if info != []:
      sqlInsertCommand = f"""INSERT INTO WEAPONS VALUES (
        "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
        "{info[4]}","{info[5]}","{info[6]}"
      );"""
      cursor.execute(sqlInsertCommand)
      connection.commit()
  print("Weapon info database updated.")

def update_weapon_stats():
  with open("./Stats/weapon_stats.txt", "r") as f1:
    if os.path.exists("./Data/weapon_stats.db"):
      os.remove("./Data/weapon_stats.db")
    connection = sqlite3.connect("./Data/weapon_stats.db")
    weapon = None
    cursor = connection.cursor()
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[0] == "[":
        connection.commit()
        weapon = line[1:-2]
        sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {weapon}(
          level int,
          cost int,
          mults varchar(255),
          PRIMARY KEY(level)
        );"""
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
      else:
        stats = line[:-1].split(",")
        sqlInsertCommand = f"""INSERT INTO {weapon} VALUES (
          "{stats[0]}","{stats[1]}","{stats[2]}"
        );"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Weapon stats databases updated.")

def update_troop_info():
  with open("./Stats/troop_info.txt", "r") as f1:
    if os.path.exists("./Data/troop_info.db"):
      os.remove("./Data/troop_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS TROOPS(
      internal_name varchar(255),
      display_name varchar(255),
      ability varchar(255),
      attacks varchar(255),
      weaknesses varchar(255),
      resistances varchar(255),
      shield int,
      flying varchar(255),
      description varchar(510),
      evolution varchar(255),
      PRIMARY KEY(internal_name)
      );"""
    connection = sqlite3.connect("./Data/troop_info.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    info = []
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[:8] == "IntName:":
        if info != []:
          sqlInsertCommand = f"""INSERT INTO TROOPS VALUES (
            "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
            "{info[4]}","{info[5]}","{info[6]}","{info[7]}",
            "{info[8]}","{info[9]}"
          );"""
          cursor.execute(sqlInsertCommand)
          connection.commit()
        info = [""] * 11
        info[0] = line[9:-1]
      elif line[:5] == "Name:":
        info[1] = line[6:-1]
      elif line[:8] == "Ability:":
        info[2] = line[9:-1]
      elif line[:6] == "Moves:":
        info[3] = line[7:-1]
      elif line[:11] == "Weaknesses:":
        info[4] = line[12:-1]
      elif line[:12] == "Resistances:":
        info[5] = line[13:-1]
      elif line[:7] == "Shield:":
        info[6] = line[7:-1]
      elif line[:7] == "Flying:":
        info[7] = line[8:-1]
      elif line[:12] == "Description:":
        info[8] = line[13:-1]
      elif line[:10] == "Evolution:":
        info[9] = line[11:-1]
      elif line[:9] == "MaxLevel:":
        info[10] = line[10:-1]
  if info != []:
    sqlInsertCommand = f"""INSERT INTO TROOPS VALUES (
      "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
      "{info[4]}","{info[5]}","{info[6]}","{info[7]}",
      "{info[8]}","{info[9]}"
    );"""
    cursor.execute(sqlInsertCommand)
    connection.commit()
  print("Troop info database updated.")

def update_battles():
  with open("./Stats/battles.txt", "r") as f1:
    if os.path.exists("./Data/battle_stats.db"):
      os.remove("./Data/battle_stats.db")
    if os.path.exists("./Data/battle_info.db"):
      os.remove("./Data/battle_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS BATTLES(
      battle_id varchar(255),
      wave_sizes varchar(255),
      stamina varchar(255),
      reward varchar(255),
      PRIMARY KEY(battle_id)      
    );"""
    connection_info = sqlite3.connect("./Data/battle_info.db")
    connection_stats = sqlite3.connect("./Data/battle_stats.db")
    cursor_info = connection_info.cursor()
    cursor_stats = connection_stats.cursor()
    cursor_info.execute(sqlCreateCommand)
    connection_info.commit()
    battle = None
    battle_info = []
    troop_info = []
    id = 0
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[0] == "[":
        if battle_info != []:
          sqlInsertCommand = f"""INSERT INTO BATTLES VALUES (
            "{battle}","{battle_info[0]}","{battle_info[1]}","{battle_info[2]}"
          );"""
          cursor_info.execute(sqlInsertCommand)
          connection_info.commit()
          battle_info = []
        if troop_info != []:
          sqlInsertCommand = f"""INSERT INTO {battle} VALUES (
            "{id}","{troop_info[0]}","{troop_info[1]}","{troop_info[2]}","{troop_info[3]}"
          );"""
          cursor_stats.execute(sqlInsertCommand)
          connection_stats.commit()
          troop_info = []
        battle = line[1:-2]
        id = 0
        battle_info = [""] * 3
        sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {battle}(
          id int,
          troop_internal_name varchar(255),
          level int,
          ability varchar(255),
          attacks varchar(255),
          PRIMARY KEY(id)
        );"""
        cursor_stats.execute(sqlCreateCommand)
      elif line[:10] == "WaveSizes:":
        battle_info[0] = line[11:-1]
      elif line[:8] == "Stamina:":
        battle_info[1] = line[9:-1]
      elif line[:7] == "Reward:":
        battle_info[2] = line[8:-1]
      elif line[:6] == "Troop:":
        if troop_info != []:
          sqlInsertCommand = f"""INSERT INTO {battle} VALUES (
            "{id}","{troop_info[0]}","{troop_info[1]}","{troop_info[2]}","{troop_info[3]}"
          );"""
          cursor_stats.execute(sqlInsertCommand)
          connection_stats.commit()
          troop_info = []
        troop_info = [""] * 4
        troop = line[7:-1].split(",")
        troop_info[0] = troop[0]
        troop_info[1] = troop[1]
        id += 1
      elif line[:8] == "Ability:":
        troop_info[2] = line[9:-1]
      elif line[:8] == "Attacks:":
        troop_info[3] = line[9:-1]
    sqlInsertCommand = f"""INSERT INTO BATTLES VALUES (
        "{battle}","{battle_info[0]}","{battle_info[1]}","{battle_info[2]}"
      );"""
    cursor_info.execute(sqlInsertCommand)
    connection_info.commit()
    sqlInsertCommand = f"""INSERT INTO {battle} VALUES (
      "{id}","{troop_info[0]}","{troop_info[1]}","{troop_info[2]}","{troop_info[3]}"
    );"""
    cursor_stats.execute(sqlInsertCommand)
    connection_stats.commit()
  print("Battle databases updated.")

def update_abilities():
  with open("./Stats/ability_info.txt", "r") as f1:
    if os.path.exists("./Data/ability_info.db"):
      os.remove("./Data/ability_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS ABILITIES(
      internal_name varchar(255),
      display_name varchar(255),
      timing varchar(255),
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/ability_info.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        ability = line[:-1].split(",")
        desc = ",".join(ability[2:-1] + [ability[-1]])
        sqlInsertCommand = f"""INSERT INTO ABILITIES VALUES ("{ability[0]}","{ability[1]}","{ability[2]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Ability info database updated.")

def update_power_info():
  with open("./Stats/power_info.txt", "r") as f1:
    if os.path.exists("./Data/power_info.db"):
      os.remove("./Data/power_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS POWERS(
      id int,
      internal_name varchar(255),
      display_name varchar(255),
      cooldown int,
      type varchar(255),
      element varchar(255),
      shield_damage int,
      target varchar(255),
      description varchar(510),
      evolution varchar(255),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/power_info.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    info = []
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[:3] == "ID:":
        if info != []:
          sqlInsertCommand = f"""INSERT INTO POWERS VALUES (
            "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
            "{info[4]}","{info[5]}","{info[6]}","{info[7]}",
            "{info[8]}","{info[9]}"
          );"""
          cursor.execute(sqlInsertCommand)
          connection.commit()
        info = [""] * 10
        info[0] = line[4:-1]
      elif line[:8] == "IntName:":
        info[1] = line[9:-1]
      elif line[:5] == "Name:":
        info[2] = line[6:-1]
      elif line[:9] == "Cooldown:":
        info[3] = line[10:-1]
      elif line[:5] == "Type:":
        info[4] = line[6:-1]
      elif line[:8] == "Element:":
        info[5] = line[9:-1]
      elif line[:13] == "ShieldDamage:":
        info[6] = line[14:-1]
      elif line[:7] == "Target:":
        info[7] = line[8:-1]
      elif line[:12] == "Description:":
        info[8] = line[13:-1]
      elif line[:10] == "Evolution:":
        info[9] = line[11:-1]
    if info != []:
      sqlInsertCommand = f"""INSERT INTO POWERS VALUES (
        "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
        "{info[4]}","{info[5]}","{info[6]}","{info[7]}",
        "{info[8]}","{info[9]}"
      );"""
      cursor.execute(sqlInsertCommand)
      connection.commit()
  print("Power info database updated.")

def update_power_stats():
  with open("./Stats/power_stats.txt", "r") as f1:
    if os.path.exists("./Data/power_stats.db"):
      os.remove("./Data/power_stats.db")
    connection = sqlite3.connect("./Data/power_stats.db")
    power = None
    cursor = connection.cursor()
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[0] == "[":
        connection.commit()
        power = line[1:-2]
        sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {power}(
          level int,
          power int,
          TH_needed int,
          cost int,
          PRIMARY KEY(level)
        );"""
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
      else:
        stats = line[:-1].split(",")
        sqlInsertCommand = f"""INSERT INTO {power} VALUES (
          "{stats[0]}","{stats[1]}","{stats[2]}","{stats[3]}"
        );"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Power stats database updated.")

def create_player_table():
  if os.path.exists("./Data/player_data.db"):
    os.remove("./Data/player_data.db")
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlCreateCommand = """CREATE TABLE IF NOT EXISTS PLAYERS(
    id int,
    username varchar(255),
    password varchar(255),
    name varchar(255),
    th_level int,
    gold int,
    elixir int,
    weapon_ore int,
    d_elixir int,
    unlocked_powers varchar(255),
    active_powers varchar(255),
    power_limit int,
    swords varchar(510),
    shields varchar(510),
    difficulties varchar(255),
    settings varchar(255),
    stamina int,
    barb_name varchar(255),
    barb_lv int,
    barb_active_attacks varchar(510),
    barb_unlocked_attacks varchar(510),
    barb_max_attacks int,
    barb_sword varchar(255),
    barb_shield varchar(255),
    last_login float,
    PRIMARY KEY(id)
  );"""
  cursor.execute(sqlCreateCommand)
  print("Player data reset.")

def update_storage_data():
  if os.path.exists("./Data/storage_data.db"):
    os.remove("./Data/storage_data.db")
  connection = sqlite3.connect("./Data/storage_data.db")
  cursor = connection.cursor()
  sqlCreateCommand = """CREATE TABLE IF NOT EXISTS STORAGES(
    th int,
    max_gold int,
    max_elixir int,
    max_weapon_ore int,
    max_d_elixir int,
    PRIMARY KEY(th)
  );"""
  cursor.execute(sqlCreateCommand)
  with open("./Stats/storages.txt", "r") as f1:
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        info = line.split(",")
        sqlInsertCommand = f"""INSERT INTO STORAGES VALUES (
          "{info[0]}","{info[1]}","{info[2]}","{info[3]}",
          "{info[4]}"
        );"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Storage data updated.")

def update_all_databases():
  update_attacks()
  update_abilities()
  update_troop_info()
  update_troop_stats()
  update_barb_costs()
  update_battles()
  update_power_info()
  update_power_stats()
  update_weapon_info()
  update_weapon_stats()
  update_storage_data()
  add_update()

def main():
  if not should_update():
    print("Not updating databases.")
    return False
  else:
    update_all_databases()
    print("All databases complete.")

if __name__ == '__main__':
  main()
