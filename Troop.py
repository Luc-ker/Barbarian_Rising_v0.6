import sqlite3
import os
from Weapon import Weapon
from Ability import Ability
from Attack import Attack

def get_base_stats(troop, level):
  if os.path.exists("./Data/troop_stats.db"):
    connection = sqlite3.connect("./Data/troop_stats.db")
  else:
    raise FileNotFoundError("/Data/troop_stats.db was not found.")
  sqlCommand = f"""SELECT * FROM {troop} WHERE level = {level};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

def get_troop_info(troop):
  if os.path.exists("./Data/troop_info.db"):
    connection = sqlite3.connect("./Data/troop_info.db")
  else:
    raise FileNotFoundError("/Data/troop_info.db was not found.")
  sqlCommand = f"""SELECT * FROM TROOPS WHERE internal_name = "{troop}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

def get_upgrade_costs(troop, level):
  if os.path.exists("./Data/barb_costs.db"):
    connection = sqlite3.connect("./Data/barb_costs.db")
  else:
    raise FileNotFoundError("/Data/barb_costs.db was not found.")
  sqlCommand = f"""SELECT * FROM {troop} WHERE level = "{level}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

def get_max_level(troop):
  if os.path.exists("./Data/troop_stats.db"):
    connection = sqlite3.connect("./Data/troop_stats.db")
  else:
    raise FileNotFoundError("/Data/troop_stats.db was not found.")
  sqlCommand = f"""SELECT level FROM {troop};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[-1][0] 

def make_attacks(str):
  return [Attack(x) for x in str.split(",")]
  
class Troop():
  internal_name = None
  name = None
  level = 0
  ability = None
  attacks = []
  
  def __init__(self, troop, level=1, owner=None):
    troop = troop.upper().replace(" ","")
    dbstats = get_base_stats(troop, level)
    info = get_troop_info(troop)
    if type(dbstats) != tuple:
      raise TypeError

    self.internal_name = troop
    self.display_name = info[1]
    self.level = level
    if info[2] != "":
      self.ability = Ability(info[2])
    else:
      self.ability = None

    self.active_attacks = make_attacks(info[3])
    self.unlocked_attacks = make_attacks(info[3])
    self.max_attacks = 1

    self.stats = {
      "hp":dbstats[1],
      "maxHp":dbstats[1],
      "attack":dbstats[2],
      "defence":dbstats[3],
      "speed":dbstats[4],
      "ability_level":dbstats[5],
      "crit_rate": 5,
      "damage_mult": 0,
      "damage_reduction": 0
    }
    self.weapons = {
      "sword": None,
      "shield": None
    }
    self.owner = owner
    self.description = info[8]
    self.base_stats = self.stats.copy()

  def get_sword(self):
    return self.weapons["sword"]

  def get_shield(self):
    return self.weapons["shield"]

  def has_weapon(self, weapon, type):
    return self.weapons[type] is not None and self.weapons[type].internal_name == weapon

  def equip_weapon(self, weapon):
    self.weapons.update({weapon.type: weapon})
    self.calc_stats()

  def unequip_weapon(self, weaponType):
    self.weapons.update({weaponType: None})
    self.calc_stats()

  def equipped(self, weapon):
    if type(weapon) is not Weapon:
      raise TypeError("The weapon needs to be a Weapon class object.")
    return weapon is self.weapons[weapon.type]

  def calc_stats(self):
    stats = get_base_stats(self.internal_name, self.level)
    if type(stats) != tuple:
      raise TypeError
    self.stats.update({
      "hp":stats[1],
      "maxHp":stats[1],
      "attack":stats[2],
      "defence":stats[3],
      "speed":stats[4],
      "ability_level":stats[5],
      "crit_rate": 5,
      "damage_mult": 0,
      "damage_reduction": 0
    })
    for weapon in self.weapons.values():
      if weapon is not None:
        for stat, modifier in weapon.stats.items():
          if stat in ["crit_rate","damage_mult","damage_reduction"]:
            self.stats.update({stat: self.stats[stat] + int(modifier)})
          else:
            self.stats.update({stat: self.stats[stat] * (1+int(modifier)/100)})

  def level_up(self, player, levels=1):
    for i in range(levels):
      stats = self.get_upgrade_costs(self.level+i+1)
      player.elixir -= stats[1]
      player.gold -= stats[2]
    self.level += levels
    self.calc_stats()

  def get_upgrade_costs(self, level):
    return get_upgrade_costs(self.internal_name, level)

  def max_level(self):
    return self.level >= get_max_level(self.internal_name)

  def can_evolve(self, player):
    evoData = get_troop_info(self.internal_name)[9].split(",")
    if evoData == [""]:
      return False
    cost = int(evoData[2])
    th_req = int(evoData[1])
    return (self.max_level() and player.d_elixir >= cost
            and player.th >= th_req)

  def evolve(self, player):
    evoData = get_troop_info(self.internal_name)[9].split(",")
    player.d_elixir -= int(evoData[2])
    evo = Troop(evoData[0], self.level+1, self.owner)
    evoUnlocked = [x.internal_name for x in evo.unlocked_attacks]
    for attack in self.unlocked_attacks:
      if attack.internal_name not in evoUnlocked:
        evo.unlocked_attacks.append(attack)    
    evo.max_attacks = self.max_attacks
    evo.weapons = self.weapons
    evo.calc_stats()
    self = evo
    return self

  def has_attack(self, attack):
    return attack in [x.internal_name for x in self.unlocked_attacks]

  def has_active_attack(self, attack):
    return attack in [x.internal_name for x in self.active_attacks]

  def has_unlocked_attack(self, attack):
    if not self.has_attack(attack):
      return None
    unlocked_attacks = [x.internal_name for x in self.unlocked_attacks]
    if attack in unlocked_attacks:
      return self.unlocked_attacks[unlocked_attacks.index(attack)]
    return None

  def get_active_attack(self, attack):
    active_attacks = [x.internal_name for x in self.active_attacks]
    if attack in active_attacks:
      return self.active_attacks[active_attacks.index(attack)]
    return None

  def unlock_attack(self, attack):
    if type(attack) != Attack:
      attack = Attack(attack)
    if attack.internal_name not in [x.internal_name for x in self.unlocked_attacks]:
      self.unlocked_attacks.append(attack)

  def learn_attack(self, attack, forced=False):
    if not forced:
      if type(attack) == Attack:
        attack = self.has_unlocked_attack(attack.internal_name)
      elif type(attack) == str:
        attack = self.has_unlocked_attack(attack)
      else:
        raise TypeError("Invalid Attack.")
      if attack is None:
        return
    elif forced:
      attack = Attack(attack)
    self.active_attacks.append(attack)

  def forget_attack(self, attack):
    if type(attack) != Attack:
      attack = self.get_active_attack(attack)
    if attack is None:
      raise TypeError("Not a valid attack.")
    else:
      self.active_attacks.remove(attack)

  def can_learn_attack(self):
    return len(self.active_attacks) < self.max_attacks

  def has_ability(self,ability):
    if self.ability is None:
      return None
    if self.ability.internal_name == ability and self.stats["ability_level"] > 0:
      return self
    return None

  def change_ability(self, ability):
    self.ability = Ability(ability)

  def can_upgrade(self, player):
    if self.can_evolve(player):
      return 5
    if self.max_level():
      return 4
    stats = self.get_upgrade_costs(self.level+1)
    th_req = (self.level)//10+1
    costs = [player.elixir >= stats[1], player.gold >= stats[2]]
    if player.th < th_req:
      return 2
    if False in costs:
      return 3
    return 1

  def owned_by_player(self):
    return self.owner == "Player"
    