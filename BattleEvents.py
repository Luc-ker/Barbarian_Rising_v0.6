from Battle import Battle, display_message
from BattleLoader import get_battle_info

def loot_battle(player, type, diff, mult=1):    
  battle_id = f"{type}BATTLE{diff}"
  battle_info = get_battle_info(battle_id)
  battle_stamina = int(battle_info[0]) or 0
  total_stamina = battle_stamina*mult
  boost = sufficient_stamina(player, total_stamina)
  if boost != 2 and mult > 1:
    display_message(player, "Not enough stamina!")
    return
  amount = int(battle_info[1])*boost*mult
  
  battle = Battle(player, battle_id)
  if battle.result == 1:
    if type == "GOLD":
      player.add_gold(amount)
    elif type == "ELIXIR":
      player.add_elixir(amount)
    elif type == "ORE":
      player.add_weapon_ore(amount)
    elif type == "DARKELIXIR":
      player.add_d_elixir(amount)
    if total_stamina < player.stamina and boost == 2:
      player.stamina -= total_stamina
    if player.difficulties_unlocked[type] < diff+1:
      player.difficulties_unlocked[type] = diff+1

def sufficient_stamina(player, stamina):
  if player.stamina >= stamina:
    return 2
  return 1

def goblinBattle1(player):
    battle = Battle(player, "GOBLINBATTLE1", "No Enemy Crits")
    if battle.result == 1:
        player.add_gold(500)
        player.add_elixir(500)

def TH2_Battle(player, diff):
  battle = Battle(player, f"TH2BATTLE{diff}")
  if battle.result == 1:
    if not player.unlocked_power("SUPERARCHER") and not player.unlocked_power("ARCHERQUEEN"):
      power = player.unlock_power("ARCHER")
      if power is not None:
        display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 2:
      player.set_TH(2)
      player.add_gold(1000)
      player.add_elixir(1000)
  return battle.result

def TH3_Battle(player, diff):
  battle = Battle(player, f"TH3BATTLE{diff}")
  if battle.result == 1:
    player.obtain_weapon("WOODENSWORD",1)
    player.obtain_weapon("WOODENSHIELD",1)
    if player.th < 3:
      player.set_TH(3)
      player.add_gold(1500)
      player.add_elixir(1500)
  return battle.result

def TH4_Battle(player, diff):
  battle = Battle(player, f"TH4BATTLE{diff}")
  if battle.result == 1:
    if not player.unlocked_power("SUPERWALLBREAKER"):
      power = player.unlock_power("WALLBREAKER")
      if power is not None:
        display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 4:
      player.set_TH(4)
      player.add_gold(4000)
      player.add_elixir(4000)
  return battle.result

def TH5_Battle(player, diff):
  battle = Battle(player, f"TH5BATTLE{diff}")
  if battle.result == 1:
    # unlock stone sword in shop
    if not player.unlocked_power("SUPERWIZARD"):
      power = player.unlock_power("WIZARD")
      if power is not None:
        display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 5:
      player.set_TH(5)
      player.add_gold(5000)
      player.add_elixir(5000)
      player.add_d_elixir(2500)
    if player.barb.max_attacks < 2:
      player.barb.max_attacks = 2
      display_message(player, "Your barbarian can now have 2 active attacks!")
    if player.power_limit < 2:
      player.power_limit = 2
      display_message(player, "You can now have up to 2 powers in battle!")
  return battle.result

def TH6_Battle(player, diff):
  battle = Battle(player, f"TH6BATTLE{diff}")
  if battle.result == 1:
    # unlock meat shield in shop
    power = player.unlock_power("ICEWIZARD")
    if power is not None:
      display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 6:
      player.set_TH(6)
      player.add_gold(6000)
      player.add_elixir(6000)
  return battle.result

def TH7_Battle(player, diff):
  battle = Battle(player, f"TH7BATTLE{diff}")
  if battle.result == 1:
    power = player.unlock_power("HEALER")
    if power is not None:
      display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 7:
      player.set_TH(7)
      player.add_gold(7000)
      player.add_elixir(7000)
  return battle.result

def TH8_Battle(player, diff):
  battle = Battle(player, f"TH8BATTLE{diff}")
  if battle.result == 1:
    # unlock iron sword and shield in shop
    if player.th < 8:
      player.set_TH(8)
      player.add_gold(8000)
      player.add_elixir(8000)
  return battle.result

def TH9_Battle(player, diff):
  battle = Battle(player, f"TH9BATTLE{diff}")
  if battle.result == 1:
    if not player.unlocked_power("SUPERMINER"):
      power = player.unlock_power("MINER")
      if power is not None:
        display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 9:
      player.set_TH(9)
      player.add_gold(9000)
      player.add_elixir(9000)
  return battle.result

def TH10_Battle(player, diff):
  battle = Battle(player, f"TH10BATTLE{diff}")
  if battle.result == 1:
    # unlock gold sword and shield in shop
    if player.th < 10:
      player.set_TH(10)
      player.add_gold(10000)
      player.add_elixir(10000)
    if player.barb.max_attacks < 3:
      player.barb.max_attacks = 3
      display_message(player, "Your barbarian can now have 3 active attacks!")
    if player.power_limit < 3:
      player.power_limit = 3
      display_message(player, "You can now have up to 3 powers in battle!")
  return battle.result

def TH11_Battle(player, diff):
  battle = Battle(player, f"TH11BATTLE{diff}")
  if battle.result == 1:
    power = player.unlock_power("HEADHUNTER")
    if power is not None:
      display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 11:
      player.set_TH(11)
      player.add_gold(11000)
      player.add_elixir(11000)
  return battle.result

def TH12_Battle(player, diff):
  battle = Battle(player, f"TH12BATTLE{diff}")
  if battle.result == 1:
    power = player.unlock_power("ETITAN")
    if power is not None:
      display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 12:
      player.set_TH(12)
      player.add_gold(12000)
      player.add_elixir(12000)
  return battle.result

def TH13_Battle(player, diff):
  battle = Battle(player, f"TH13BATTLE{diff}")
  if battle.result == 1:
    # unlock diamond sword and emerald shield in shop
    power = player.unlock_power("APPRENTICEWARDEN")
    if power is not None:
      display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 13:
      player.set_TH(13)
      player.add_gold(13000)
      player.add_elixir(13000)
  return battle.result

def TH14_Battle(player, diff):
  battle = Battle(player, f"TH14BATTLE{diff}")
  if battle.result == 1:
    power = player.unlock_power("DRAGONRIDER")
    if power is not None:
      display_message(player, f"You unlocked the power of the {power}!")
    if player.th < 14:
      player.set_TH(14)
      player.add_gold(14000)
      player.add_elixir(14000)
  return battle.result

def TH15_Battle(player, diff):
  battle = Battle(player, f"TH15BATTLE{diff}")
  if battle.result == 1:
    # unlock rainbow sword and frozen shield in shop
    if player.th < 15:
      player.set_TH(15)
      player.add_gold(15000)
      player.add_elixir(15000)
  return battle.result
