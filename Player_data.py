import sqlite3
from datetime import datetime

def now():
  return datetime.now()

def should_refresh_stamina(login):
  if type(login) == str:
    login = datetime.strptime(login, '%Y-%m-%d %H:%M:%S.%f')
  return login < now().replace(hour=0, minute=0, second=0, microsecond=0)

def get_new_id():
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlCommand = """SELECT id FROM PLAYERS;"""
  cursor.execute(sqlCommand)
  connection.commit()
  try:
    return cursor.fetchall()[0][0]+1
  except IndexError:
    return 1

def get_acc_with_email(email):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlCommand = f"""SELECT * FROM PLAYERS WHERE username = "{email}";"""
  cursor.execute(sqlCommand)
  connection.commit()
  try:
    return cursor.fetchall()[0][0]+1
  except IndexError:
    return None

def update_player_password(email,password):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlCommand = f"""UPDATE PLAYERS SET password = "{password}"
  WHERE username = "{email}";"""
  cursor.execute(sqlCommand)
  connection.commit()

def update_player_table(player, username="", password=""):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  if player.id == 0:
    player.id = get_new_id()
  unlocked_powers = [
    f"{x.id}:{x.level}:{x.cooldown}" for x in player.unlocked_powers
  ] if len(player.unlocked_powers) > 0 else []
  active_powers = [
    f"{x.id}:{x.level}:{x.cooldown}" for x in player.active_powers
  ] if len(player.active_powers) > 0 else []
  unlocked_attacks = ",".join([x.internal_name for x in player.barb.unlocked_attacks])
  active_attacks = ",".join([x.internal_name for x in player.barb.active_attacks])
  swords = [
    f"{x.id}:{x.level}" for x in player.swords
  ] if len(player.swords) > 0 else []
  shields = [
    f"{x.id}:{x.level}" for x in player.shields
  ] if len(player.shields) > 0 else []
  diffs = ",".join([str(x) for x in list(player.difficulties_unlocked.values())])
  settings = ",".join(player.settings.values())
  try:
    swordID = f"[{player.barb.weapons['sword'].id}:{player.barb.weapons['sword'].level}]"
  except AttributeError:
    swordID = "None"
  try:
    shieldID = f"[{player.barb.weapons['shield'].id}:{player.barb.weapons['shield'].level}]"
  except AttributeError:
    shieldID = "None"
  try:
    sqlInsertCommand = f"""INSERT INTO PLAYERS (
      id, username, password, name, th_level,
      gold, elixir, d_elixir, weapon_ore,
      unlocked_powers, active_powers, power_limit,
      swords, shields, difficulties, settings, stamina,
      barb_name, barb_lv, barb_active_attacks,
      barb_unlocked_attacks, barb_max_attacks,  
      barb_sword, barb_shield, last_login
      ) VALUES (
      "{player.id}","{username}","{password}",
      "{player.name}","{player.th}",
      "{player.gold}","{player.elixir}","{player.d_elixir}",
      "{player.weapon_ore}",
      "{unlocked_powers}","{active_powers}","{player.power_limit}",
      "{swords}","{shields}","{diffs}","{settings}",
      "{player.stamina}","{player.barb.internal_name}",
      "{player.barb.level}","{active_attacks}",
      "{unlocked_attacks}","{player.barb.max_attacks}",
      "{swordID}","{shieldID}","{now()}"
    );"""
    cursor.execute(sqlInsertCommand)
  except sqlite3.IntegrityError:
    sqlInsertCommand = f"""UPDATE PLAYERS SET
      th_level = "{player.th}",
      name = "{player.name}",
      gold = "{player.gold}",
      elixir = "{player.elixir}",
      weapon_ore = "{player.weapon_ore}",
      d_elixir = "{player.d_elixir}",
      unlocked_powers = "{unlocked_powers}",
      active_powers = "{active_powers}",
      power_limit = "{player.power_limit}",
      swords = "{swords}",
      shields = "{shields}",
      difficulties = "{diffs}",
      settings = "{settings}",
      stamina = "{player.stamina}",
      barb_name = "{player.barb.internal_name}",
      barb_lv = "{player.barb.level}",
      barb_active_attacks = "{active_attacks}",
      barb_unlocked_attacks = "{unlocked_attacks}",
      barb_max_attacks = "{player.barb.max_attacks}",
      barb_sword = "{swordID}",
      barb_shield = "{shieldID}",
      last_login = "{now()}"
      WHERE id = {player.id}
    ;"""
    cursor.execute(sqlInsertCommand)
  connection.commit()

def delete_player_data(player):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlInsertCommand = f"""DELETE FROM players
    WHERE id = {player.id}
  ;"""
  cursor.execute(sqlInsertCommand)
  connection.commit()  

def load_player_data(username, password):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlCommand = f"""SELECT * FROM PLAYERS WHERE username = "{username}" AND password = "{password}";"""
  cursor.execute(sqlCommand)
  try:
    return cursor.fetchall()[0]
  except IndexError:
    return ""

def get_powers():
  connection = sqlite3.connect("./Data/power_info.db")
  cursor = connection.cursor()
  sqlCommand = """SELECT internal_name FROM POWERS ORDER BY id ASC;"""
  cursor.execute(sqlCommand)
  connection.commit()
  result = cursor.fetchall()
  return [x[0] for x in result[:10]]

def get_weapons(type):
  connection = sqlite3.connect("./Data/weapon_info.db")
  cursor = connection.cursor()
  sqlCommand = f"""SELECT internal_name FROM WEAPONS WHERE weapon_type = "{type}" ORDER BY id ASC;"""
  cursor.execute(sqlCommand)
  connection.commit()
  result = cursor.fetchall()
  return [x[0] for x in result[:6]]

def test_data():
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  try:
    sqlInsertCommand = f"""INSERT INTO PLAYERS (
      id, username, password, name, th_level,
      gold, elixir, d_elixir, weapon_ore,
      unlocked_powers, active_powers, power_limit,
      swords, shields, difficulties, settings, stamina,
      barb_name, barb_lv, barb_active_attacks,
      barb_unlocked_attacks, barb_max_attacks,  
      barb_sword, barb_shield, last_login
      ) VALUES (
      "1","jlee4889@gmail.com","sdfds","A","1",
      "500","500","0","0",
      "['7:1:0', '9:1:0']","['7:1:0', '9:1:0']","3",
      "['101:1']","['201:1']",
      "2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
      "Instant,Purple","240",
      "BARBARIAN","3","SLASH","SLASH","2",
      "None","None","{now()}"
    );"""
    cursor.execute(sqlInsertCommand)
  except sqlite3.IntegrityError:
    sqlInsertCommand = f"""UPDATE PLAYERS SET
      th_level = "8",
      name = "A",
      gold = "2000",
      elixir = "2000",
      weapon_ore = "1000",
      d_elixir = "10000",
      unlocked_powers = "['101:3:0', '2:2:0', '4:1:0', '5:2:0', '7:1:0', '8:1:0', '9:1:0', '10:1:0']",
      active_powers = "['101:3:0', '5:2:0']",
      power_limit = "2",
      swords = "['101:1','103:8']",
      shields = "['201:1','203:8']",
      difficulties = "2,1,1,1,3,1,1,1,1,1,1,1,1,1,1,1,2,3",
      settings = "Instant,Purple",
      stamina = "240",
      barb_name = "BARBARIAN",
      barb_lv = "40",
      barb_active_attacks = "SLASH",
      barb_unlocked_attacks = "SLASH",
      barb_max_attacks = 1,
      barb_sword = "None",
      barb_shield = "None",
      last_login = "{now()}"
      WHERE id = 1
    ;"""
    cursor.execute(sqlInsertCommand)
  print("Test data inserted.")
  connection.commit()
  
def test_data2():
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlInsertCommand = f"""INSERT INTO PLAYERS (
    id, username, password, name, th_level,
    gold, elixir, d_elixir, weapon_ore,
    unlocked_powers, active_powers, power_limit,
    swords, shields, difficulties, settings, stamina,
    barb_name, barb_lv, barb_active_attacks,
    barb_unlocked_attacks, barb_max_attacks,  
    barb_sword, barb_shield, last_login
    ) VALUES (
    "2","lucker4889@gmail.com","sdfds","A","2",
    "6220","500","0","0",
    "['1:2:0']","['1:2:0']","1",
    "[]","[]",
    "3,2,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1",
    "Instant,Purple","175",
    "BARBARIAN","10","SLASH","SLASH","1",
    "None","None","{now()}"
  );"""
  cursor.execute(sqlInsertCommand)
  print("Test data inserted.")
  connection.commit()