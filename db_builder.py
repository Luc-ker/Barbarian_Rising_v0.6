import sqlite3
import os

# Good for capturing mid line comments
def process_line(line: str) -> str:
    return line[:line.find("#")].strip()

def remove_brackets(line: str) -> str:
    return line[1:-1]

def extract_line_info(line: str, header: str) -> str:
    return line.removeprefix(header).strip()

def create_insert_command(tbl_name, info):
    if type(info) is list:
        return f"INSERT INTO {tbl_name} VALUES (\"{"\",\"".join(info)}\");"
    elif type(info) is str:
        return f"INSERT INTO {tbl_name} VALUES (\"{info.replace(",", "\",\"")}\");"
    else:
        raise TypeError("info needs to be a list or a string!")

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

def missing_db():
    db_list = [
        "ability_info", "attacks",
        "barb_costs", "battle_info",
        "battle_stats", "power_info",
        "power_stats", "storage_data",
        "times", "troop_info",
        "troop_stats", "weapon_info",
        "weapon_stats"
    ]
    for db in db_list:
        if not os.path.exists(f"./Data/{db}.db"):
            return True
    return False

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
    DB_NAME = "troop_stats"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
        connection = sqlite3.connect(DB_PATH)
        troop = None
        cursor = connection.cursor()
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            elif line[0] == "[":
                connection.commit()
                troop = remove_brackets(line)
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
                battler = line.split(",")
                sqlInsertCommand = create_insert_command(troop, battler)
                cursor.execute(sqlInsertCommand)
                connection.commit()
    print("Troop stats databases updated.")

def update_barb_costs():
    DB_NAME = "barb_costs"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        troop = None
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            elif line[0] == "[":
                troop = remove_brackets(line)
                sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {troop}(
                    level int,
                    elixir_cost int,
                    gold_cost int,
                    PRIMARY KEY(level)
                );"""
                cursor.execute(sqlCreateCommand)
            else:
                costs = line.split(",")
                sqlInsertCommand = create_insert_command(troop, costs)
                cursor.execute(sqlInsertCommand)
                connection.commit()
    print("Barb costs databases updated.")

def update_attacks():
    DB_NAME = "attacks"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
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
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
        info = []
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            elif line.startswith("IntName:"):
                if info != []:
                    sqlInsertCommand = create_insert_command("ATTACKS", info)
                    cursor.execute(sqlInsertCommand)
                    connection.commit()
                info = [""] * 11
                info[0] = extract_line_info(line, "IntName:")
            elif line.startswith("Name:"):
                info[1] = extract_line_info(line, "Name:")
            elif line.startswith("Element:"):
                info[2] = extract_line_info(line, "Element:")
            elif line.startswith("Power:"):
                info[3] = extract_line_info(line, "Power:")
            elif line.startswith("Target:"):
                info[4] = extract_line_info(line, "Target:")
            elif line.startswith("EffectCode:"):
                info[5] = extract_line_info(line, "EffectCode:")
            elif line.startswith("EffectChance:"):
                info[6] = extract_line_info(line, "EffectChance:")
            elif line.startswith("EffectTurns:"):
                info[7] = extract_line_info(line, "EffectTurns:")
            elif line.startswith("Flags:"):
                info[8] = extract_line_info(line, "Flags:")
            elif line.startswith("ShieldDamage:"):
                info[9] = extract_line_info(line, "ShieldDamage:")
            elif line.startswith("Description:"):
                info[10] = extract_line_info(line, "Description")
        if info != []:
            sqlInsertCommand = create_insert_command("ATTACKS", info)
            cursor.execute(sqlInsertCommand)
            connection.commit()
    print("Attack database updated.")

def update_weapon_info():
    DB_NAME = "weapon_info"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
        sqlCreateCommand = """CREATE TABLE IF NOT EXISTS WEAPONS (
            id int,
            internal_name varchar(255),
            display_name varchar(255),
            weapon_type varchar(255),
            stats varchar(255),
            th_available int,
            description varchar(510),
            PRIMARY KEY(internal_name)
        );"""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
        info = []
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            elif line.startswith("ID:"):
                if info != []:
                    sqlInsertCommand = create_insert_command("WEAPONS", info)
                    cursor.execute(sqlInsertCommand)
                    connection.commit()
                info = [""] * 7
                info[0] = extract_line_info(line, "ID:")
            elif line.startswith("IntName:"):
                info[1] = extract_line_info(line, "IntName:")
            elif line.startswith("Name:"):
                info[2] = extract_line_info(line, "Name:")
            elif line.startswith("Type:"):
                info[3] = extract_line_info(line, "Type:")
            elif line.startswith("Stats:"):
                info[4] = extract_line_info(line, "Stats:")
            elif line.startswith("TH_available:"):
                info[5] = extract_line_info(line, "TH_available:")
            elif line.startswith("Description:"):
                info[6] = extract_line_info(line, "Description:")
        if info != []:
            sqlInsertCommand = create_insert_command("WEAPONS", info)
        cursor.execute(sqlInsertCommand)
        connection.commit()
    print("Weapon info database updated.")

def update_weapon_stats():
    DN_NAME = "weapon_stats"
    DB_PATH = f"./Data/{DN_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DN_NAME}.txt", "r") as f1:
        connection = sqlite3.connect(DB_PATH)
        weapon = None
        cursor = connection.cursor()
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            elif line[0] == "[":
                connection.commit()
                weapon = remove_brackets(line)
                sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {weapon}(
                    level int,
                    cost int,
                    mults varchar(255),
                    PRIMARY KEY(level)
                    );"""
                cursor = connection.cursor()
                cursor.execute(sqlCreateCommand)
            else:
                stats = line.split(",")
                sqlInsertCommand = create_insert_command(weapon, stats)
                cursor.execute(sqlInsertCommand)
                connection.commit()
    print("Weapon stats databases updated.")

def update_troop_info():
    DB_NAME = "troop_info"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
        sqlCreateCommand = """CREATE TABLE IF NOT EXISTS TROOPS (
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
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
        info = []
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            elif line.startswith("IntName:"):
                if info != []:
                    sqlInsertCommand = create_insert_command("TROOPS", info[:-1])
                    cursor.execute(sqlInsertCommand)
                    connection.commit()
                info = [""] * 11
                info[0] = extract_line_info(line, "IntName:")
            elif line.startswith("Name:"):
                info[1] = extract_line_info(line, "Name:")
            elif line.startswith("Ability:"):
                info[2] = extract_line_info(line, "Ability:")
            elif line.startswith("Moves:"):
                info[3] = extract_line_info(line, "Moves:")
            elif line.startswith("Weaknesses:"):
                info[4] = extract_line_info(line, "Weaknesses:")
            elif line.startswith("Resistances:"):
                info[5] = extract_line_info(line, "Resistances:")
            elif line.startswith("Shield:"):
                info[6] = extract_line_info(line, "Shield:")
            elif line.startswith("Flying:"):
                info[7] = extract_line_info(line, "Flying:")
            elif line.startswith("Description:"):
                info[8] = extract_line_info(line, "Description:")
            elif line.startswith("Evolution:"):
                info[9] = extract_line_info(line, "Evolution:")
            elif line.startswith("MaxLevel:"):
                info[10] = extract_line_info(line, "MaxLevel:")
        if info != []:
            sqlInsertCommand = create_insert_command("TROOPS", info[:-1])
            cursor.execute(sqlInsertCommand)
            connection.commit()
    print("Troop info database updated.")

def update_battles():
    STATS_DB_PATH = "./Data/battle_stats.db"
    INFO_DB_PATH = "./Data/battle_info.db"
    if os.path.exists(STATS_DB_PATH):
        os.remove(STATS_DB_PATH)
    if os.path.exists(INFO_DB_PATH):
        os.remove(INFO_DB_PATH)
    with open("./Stats/battles.txt", "r") as f1:
        sqlCreateCommand = """CREATE TABLE IF NOT EXISTS BATTLES(
            battle_id varchar(255),
            wave_sizes varchar(255),
            stamina varchar(255),
            reward varchar(255),
            PRIMARY KEY(battle_id)
        );"""
        connection_info = sqlite3.connect(INFO_DB_PATH)
        connection_stats = sqlite3.connect(STATS_DB_PATH)
        cursor_info = connection_info.cursor()
        cursor_stats = connection_stats.cursor()
        cursor_info.execute(sqlCreateCommand)
        connection_info.commit()
        battle = None
        battle_info = []
        troop_info = []
        id = 0
        for line in f1:
            line = process_line(line)
            if line == "":
                continue
            elif line[0] == "[":
                if battle_info != []:
                    sqlInsertCommand = create_insert_command("BATTLES", battle_info)
                    cursor_info.execute(sqlInsertCommand)
                    connection_info.commit()
                    battle_info = []
                if troop_info != []:
                    sqlInsertCommand = create_insert_command(battle, troop_info)
                    cursor_stats.execute(sqlInsertCommand)
                    connection_stats.commit()
                    troop_info = []
                battle = remove_brackets(line)
                id = 0
                battle_info = [""] * 4
                battle_info[0] = battle
                sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {battle} (
                    id int,
                    troop_internal_name varchar(255),
                    level int,
                    ability varchar(255),
                    attacks varchar(255),
                    PRIMARY KEY(id)
                );"""
                cursor_stats.execute(sqlCreateCommand)
            elif line.startswith("WaveSizes:"):
                battle_info[1] = extract_line_info(line, "WaveSizes:")
            elif line.startswith("Stamina:"):
                battle_info[2] = extract_line_info(line, "Stamina:")
            elif line.startswith("Reward:"):
                battle_info[3] = extract_line_info(line, "Reward:")
            elif line.startswith("Troop:"):
                if troop_info != []:
                    sqlInsertCommand = create_insert_command(battle, troop_info)
                    cursor_stats.execute(sqlInsertCommand)
                    connection_stats.commit()
                id += 1
                troop_info = [""] * 5
                troop = extract_line_info(line, "Troop:").split(",")
                troop_info[0] = str(id)
                troop_info[1] = troop[0]
                troop_info[2] = troop[1]
            elif line.startswith("Ability:"):
                troop_info[2] = extract_line_info(line, "Ability:")
            elif line.startswith("Attacks:"):
                troop_info[3] = extract_line_info(line, "Attacks:")
        sqlInsertCommand = create_insert_command("BATTLES", battle_info)
        cursor_info.execute(sqlInsertCommand)
        connection_info.commit()
        sqlInsertCommand = create_insert_command(battle, troop_info)
        cursor_stats.execute(sqlInsertCommand)
        connection_stats.commit()
    print("Battle databases updated.")

def update_abilities():
    DB_NAME = "ability_info"
    DB_PATH = f"./Data/{DB_NAME}.db"
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        sqlCreateCommand = """CREATE TABLE IF NOT EXISTS ABILITIES(
            internal_name varchar(255),
            display_name varchar(255),
            timing varchar(255),
            description varchar(510),
            PRIMARY KEY(internal_name)
        );"""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            else:
                ability = line.split(",", 4)
                sqlInsertCommand = f"""INSERT INTO ABILITIES VALUES ("{ability[0]}","{ability[1]}","{ability[2]}","{ability[3]}");"""
                cursor.execute(sqlInsertCommand)
                connection.commit()
    print("Ability info database updated.")

def update_power_info():
    DB_NAME = "power_info"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
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
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
        info = []
        for line in f1:
            line = process_line(line)
            if line == "":
                continue
            elif line.startswith("ID:"):
                if info != []:
                    sqlInsertCommand = create_insert_command("POWERS", info)
                    cursor.execute(sqlInsertCommand)
                    connection.commit()
                info = [""] * 10
                info[0] = extract_line_info(line, "ID:")
            elif line.startswith("IntName:"):
                info[1] = extract_line_info(line, "IntName:")
            elif line.startswith("Name:"):
                info[2] = extract_line_info(line, "Name:")
            elif line.startswith("Cooldown:"):
                info[3] = extract_line_info(line, "Cooldown:")
            elif line.startswith("Type:"):
                info[4] = extract_line_info(line, "Type:")
            elif line.startswith("Element:"):
                info[5] = extract_line_info(line, "Element:")
            elif line.startswith("ShieldDamage:"):
                info[6] = extract_line_info(line, "ShieldDamage:")
            elif line.startswith("Target:"):
                info[7] = extract_line_info(line, "Target:")
            elif line.startswith("Description:"):
                info[8] = extract_line_info(line, "Description:")
            elif line.startswith("Evolution:"):
                info[9] = extract_line_info(line, "Evolution:")
        if info != []:
            sqlInsertCommand = create_insert_command("POWERS", info)
            cursor.execute(sqlInsertCommand)
            connection.commit()
    print("Power info database updated.")

def update_power_stats():
    DB_NAME = "power_stats"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
        connection = sqlite3.connect(DB_PATH)
        power = None
        cursor = connection.cursor()
        for line in f1:
            line = process_line(line)
            if line == "":
                pass
            elif line[0] == "[":
                connection.commit()
                power = remove_brackets(line)
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
                stats = line.split(",")
                sqlInsertCommand = create_insert_command(power, stats)
                cursor.execute(sqlInsertCommand)
                connection.commit()
    print("Power stats database updated.")

def create_player_table():
    DB_PATH = "./Data/player_data.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    connection = sqlite3.connect(DB_PATH)
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
    DB_NAME = "storage_data"
    DB_PATH = f"./Data/{DB_NAME}.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    connection = sqlite3.connect(DB_PATH)
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
    with open(f"./Stats/{DB_NAME}.txt", "r") as f1:
        for line in f1:
            line = process_line(line)
            if line == "":
                continue
            info = line.split(",")
            sqlInsertCommand = create_insert_command("STORAGES", info)
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
    if missing_db() or should_update():
        update_all_databases()
        print("All databases complete.")
        return True
    else:
        print("Not updating databases.")
        return False

if __name__ == '__main__':
    update_all_databases()
