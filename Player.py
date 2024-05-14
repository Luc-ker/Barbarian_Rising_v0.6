from Power import Power, get_power_from_id
from Troop import Troop, make_attacks
from Weapon import Weapon, get_weapon_from_id
from Storage import get_max_storages
from Player_data import now, should_refresh_stamina

class Player():
  name = ""
  id = None

  def __init__(self, name):
    self.name = name
    self.id = 0
    self.th = 0
    self.gold = 500
    self.elixir = 500
    self.weapon_ore = 0
    self.d_elixir = 0
    self.max_gold = 5000
    self.max_elixir = 5000
    self.max_weapon_ore = 0
    self.max_d_elixir = 0
    self.gold_full = (self.gold == self.max_gold)
    self.elixir_full = (self.elixir == self.max_elixir)
    self.weapon_ore_full = (self.weapon_ore == self.max_weapon_ore)
    self.d_elixir_full = (self.d_elixir == self.max_d_elixir)
    self.barb = Troop("BARBARIAN",1,"Player")
    self.unlocked_powers = []
    self.active_powers = []
    self.power_limit = 1
    self.swords = []
    self.shields = []
    self.stamina = 240
    self.difficulties_unlocked = {
      "GOLD": 1,
      "ELIXIR": 1,
      "ORE": 0,
      "DARKELIXIR": 0,
      "TH2": 1,
      "TH3": 1,
      "TH4": 1,
      "TH5": 1,
      "TH6": 1,
      "TH7": 1,
      "TH8": 1,
      "TH9": 1,
      "TH10": 1,
      "TH11": 1,
      "TH12": 1,
      "TH13": 1,
      "TH14": 1,
      "TH15": 1
    }
    self.settings = {
      "txt_speed": "Normal",
      "txt_box_col": "Blue"
    }
    self.controls = {
      "Back": ["x"],
      "Use": ["c"]
    }
    self.last_login = now()

  def load(self,save_values):
    self.__init__(save_values[3])
    self.id = save_values[0]
    self.th = save_values[4]
    self.gold = int(save_values[5])
    self.elixir = int(save_values[6])
    self.weapon_ore = int(save_values[7])
    self.d_elixir = int(save_values[8])
    self.update_max_storage()
    self.gold_full = (self.gold == self.max_gold)
    self.elixir_full = (self.elixir == self.max_elixir)
    self.weapon_ore_full = (self.weapon_ore == self.max_weapon_ore)
    self.d_elixir_full = (self.d_elixir == self.max_d_elixir)
    if save_values[9] != "[]":
      self.unlocked_powers = self.convert_power_save_value(save_values[9])
    if save_values[10] != "[]":
      self.active_powers = self.convert_power_save_value(save_values[10])
    self.power_limit = save_values[11]
    if save_values[12] != "[]":
      self.swords = self.convert_weapon_save_value(save_values[12])
    if save_values[13] != "[]":
      self.shields = self.convert_weapon_save_value(save_values[13])
    difficulties = [
      int(x) for x in save_values[14].split(",")
    ]
    for i, diff in enumerate(list(self.difficulties_unlocked.keys())):
      self.difficulties_unlocked[diff] = difficulties[i]
    settings = save_values[15].split(",")
    self.settings = {
      "txt_speed": settings[0],
      "txt_box_col": settings[1]
    }
    self.stamina = save_values[16]
    self.barb = Troop(save_values[17],save_values[18],"Player")
    self.barb.active_attacks = make_attacks(save_values[19])
    self.barb.unlocked_attacks = make_attacks(save_values[20])
    self.barb.max_attacks = save_values[21]
    if save_values[22] != "None":
      self.get_barb_weapon(save_values[22])
    if save_values[23] != "None":
      self.get_barb_weapon(save_values[23])
    self.barb.calc_stats()
    self.last_login = save_values[24]
    return self

  def should_refresh_stamina(self):
    if should_refresh_stamina(self.last_login):
      self.stamina = 240
      self.last_login = now()
      return True
    return False

  def update_max_storage(self):
    stats = get_max_storages(self.th)
    self.max_gold = int(stats[1])
    self.max_elixir = int(stats[2])
    self.max_weapon_ore = int(stats[3])
    self.max_d_elixir = int(stats[4])

  def get_barb_weapon(self, save_value):
    weapon = save_value[1:-1].replace("'","").split(":")
    weapon = Weapon(get_weapon_from_id(weapon[0]),int(weapon[1]))
    if weapon.type == "sword":
      self.barb.weapons["sword"] = self.get_sword(weapon.internal_name)
    if weapon.type == "shield":
      self.barb.weapons["shield"] = self.get_shield(weapon.internal_name)

  def convert_weapon_save_value(self, save_value):
    data = save_value[1:-1].replace("'","").split(",")
    return [Weapon(get_weapon_from_id(x.split(":")[0]),int(x.split(":")[1])) for x in data]

  def convert_power_save_value(self, save_value):
    data = save_value[1:-1].replace("'","").split(",")
    return [Power(get_power_from_id(x.split(":")[0]), int(x.split(":")[1]), int(x.split(":")[2])) for x in data]

  def unlocked_power(self, power):
    return power in [x.internal_name for x in self.unlocked_powers]

  def has_active_power(self, power):
    return power in [x.internal_name for x in self.active_powers]

  def get_unlocked_power(self, power):
    if not self.unlocked_power(power):
      return None
    unlocked_powers = [
      x.internal_name for x in self.unlocked_powers
    ]
    if power in unlocked_powers:
      return self.unlocked_powers[unlocked_powers.index(power)]
    return None

  def get_unlocked_power_index(self, power):
    if not self.unlocked_power(power):
      return None
    unlocked_powers = [
      x.internal_name for x in self.unlocked_powers
    ]
    if power in unlocked_powers:
      return unlocked_powers.index(power)
    return None

  def get_active_power(self, power):
    active_powers = [x.internal_name for x in self.active_powers]
    if power in active_powers:
      return self.active_powers[active_powers.index(power)]
    return None

  def get_active_power_index(self, power):
    active_powers = [x.internal_name for x in self.active_powers]
    if power in active_powers:
      return active_powers.index(power)
    return None

  def unlock_power(self, power):
    if type(power) != Power:
      power = Power(power)
    if power.internal_name in [x.internal_name for x in self.unlocked_powers]:
      return
    else:
      self.unlocked_powers.append(power)
      return power.display_name

  def equip_power(self, power):
    if type(power) == Power:
      power = self.get_unlocked_power(power.internal_name)
    elif type(power) == str:
      power = self.get_unlocked_power(power)
    else:
      raise TypeError("Invalid Power.")
    if power is None:
      return
    self.active_powers.append(power)
  
  def unequip_power(self, power):
    if type(power) != Power:
      power = self.get_active_power(power)
    if power is None:
      raise TypeError("Not a valid power.")
    self.active_powers.remove(power)

  def can_equip_power(self):
    return len(self.active_powers) < self.power_limit

  def has_sword(self, weapon):
    if type(weapon) == Weapon:
      return weapon.internal_name in [x.internal_name for x in self.swords]
    elif type(weapon) == str:
      return weapon in [x.internal_name for x in self.swords]
    else:
      raise TypeError("Invalid weapon type.")

  def get_sword(self, weapon):
    swords = [x.internal_name for x in self.swords]
    if weapon in swords:
      return self.swords[swords.index(weapon)]
    return None

  def has_shield(self, weapon):
    if type(weapon) == Weapon:
      return weapon.internal_name in [x.internal_name for x in self.shields]
    elif type(weapon) == str:
      return weapon in [x.internal_name for x in self.shields]
    else:
      raise TypeError("Invalid weapon type.")

  def get_shield(self, weapon):
    shields = [x.internal_name for x in self.shields]
    if weapon in shields:
      return self.shields[shields.index(weapon)]
    return None

  def obtain_weapon(self, weapon, level):
    if type(weapon) != Weapon:
      weapon = Weapon(weapon, level)
    if weapon.type == "sword":
      if not self.has_sword(weapon):
        self.swords.append(weapon)
    elif weapon.type == "shield":
      if not self.has_shield(weapon):
        self.shields.append(weapon)

  def add_gold(self, amount):
    available = self.max_gold - self.gold
    if self.gold_full:
      pass
    elif amount > available:
      self.gold += available
    else:
      self.gold += amount
    self.gold_full = (self.gold == self.max_gold)

  def add_elixir(self, amount):
    available = self.max_elixir - self.elixir
    if self.elixir_full:
      pass
    elif amount > available:
      self.elixir += available
    else:
      self.elixir += amount
    self.elixir_full = (self.elixir == self.max_elixir)

  def add_weapon_ore(self, amount):
    available = self.max_weapon_ore - self.weapon_ore
    if self.weapon_ore_full:
      pass
    elif amount > available:
      self.weapon_ore += available
    else:
      self.weapon_ore += amount
    self.weapon_ore_full = (self.weapon_ore == self.max_weapon_ore)

  def add_d_elixir(self, amount):
    available = self.max_d_elixir - self.d_elixir
    if self.d_elixir_full:
      pass
    elif amount > available:
      self.d_elixir += available
    else:
      self.d_elixir += amount
    self.d_elixir_full = (self.d_elixir == self.max_d_elixir)

  def set_TH(self,th):
    self.th = th
    self.update_max_storage()


