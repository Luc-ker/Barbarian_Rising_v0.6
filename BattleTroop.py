from Troop import Troop, get_troop_info
from BattleAttack import BattleAttack
from BattleAbility import BattleAbility
from Status import Status
import random

def make_array(str):
  return str.split(",")

def digit_range_check(vari,min=1,max=4):
  if len(vari) != 1 or not vari.isdigit() or (int(vari) < min or int(vari) > max):
    return False
  return True

def all_flying(enemies):
  if type(enemies) != list:
    return enemies.flying
  for enemy in enemies:
    if enemy.flying is False:
      return False
  return True

class BattleTroop(Troop):
  weaknesses = []
  resistances = []
  shield = 0
  flying = None
  broken = False

  def __init__(self, troop, level=1):
    if type(troop) == str:
      super().__init__(troop, level)
    elif type(troop) == tuple:
      super().__init__(troop[0], troop[1])
    elif type(troop) == Troop:
      super().__init__(troop.internal_name, troop.level)
      self.weapons = troop.weapons
      self.owner = troop.owner
      self.stats = troop.stats
      self.ability = troop.ability
      self.active_attacks = troop.active_attacks
    else:
      raise TypeError("Not a valid troop.")
    info = get_troop_info(self.internal_name)
    self.weaknesses = make_array(info[4])
    self.resistances = make_array(info[5])
    self.shield = info[6]
    self.max_shield = info[6]
    self.flying = (info[7] == "true")
    self.buffs = []
    self.debuffs = []
    self.broken = False
    self.original_action = 1000 / self.stats["speed"]
    self.action = self.original_action # AV = Action Value
    self.active_attacks = [
      BattleAttack(x.internal_name).convert() for x in self.active_attacks
    ]
    if self.has_an_ability():
      self.ability = BattleAbility(self.ability.internal_name).convert()
    self.ability_triggered = False
    self.turns_taken = 0
    self.broke_enemy = False
    self.graphic = None
    self.hp_bar = None
    self.hp_shield_bar = None
    self.damage_dealt = 0
    self.calc_stats()

  def calc_stats(self):
    hp = self.stats["hp"]
    super().calc_stats()
    self.stats["hp"] = hp
    self.apply_statuses(self.buffs)
    self.apply_statuses(self.debuffs)

  def apply_statuses(self, statuses):
    for status in statuses:
      if status.stat is not None:
        if status.operand == "mult":
          self.stats.update(
            {status.stat: self.stats[status.stat] + self.base_stats[status.stat]*status.mult}
          )
        elif status.operand == "add":
          self.stats.update(
            {status.stat: self.stats[status.stat]+status.mult}
          )
        elif status.operand == "minus":
          self.stats.update(
            {status.stat: self.stats[status.stat]-status.mult}
          )

  def reduce_shield(self, battle, shieldDmg, breaker):
    self.shield -= shieldDmg
    self.hp_shield_bar.update(battle.display)
    if self.shield <= 0:
      self.shield = 0
      self.break_shield(battle, breaker)

  def faint(self, battle):
    if self.stats["hp"] <= 0:
      battle.display_message(f"{self.display_name} was defeated!")
      battle.queue.dequeue(battle.queue.get_pos(self))
      for enemy in battle.enemy_troops:
        if self is enemy:
          battle.enemy_troops.remove(enemy)
          battle.update_enemies()
          battle.update_scene()
          self.trigger_ability(battle, "OnFainting")
          return

  def reset_AV(self):
    self.action = self.original_action

  def has_an_ability(self):
    return self.ability is not None and self.stats["ability_level"] > 0

  def ability_is(self, ability):
    return self.ability is not None and self.ability.internal_name == ability

  def trigger_ability(self, battle, timing):
    if not self.has_an_ability() or timing != self.ability.trigger_timing:
      return
    if self.ability.can_trigger(self, battle):
      self.ability.effect(battle, self)
      self.ability_triggered = True

  def add_buff(self, buff):
    if type(buff) != Status:
      raise TypeError
    self.buffs.append(buff)

  def add_debuff(self, debuff):
    if type(debuff) != Status:
      raise TypeError
    self.debuffs.append(debuff)

  def has_buff(self, buff_name):
    for b in self.buffs:
      if buff_name == b.name:
        return True
    return False

  def has_debuff(self, debuff_name):
    for b in self.debuffs:
      if debuff_name == b.name:
        return True
    return False

  def has_same_buff(self, buff):
    for b in self.buffs:
      if buff.name == b.name and buff.caused_by == b.caused_by:
        return True
    return False

  def has_same_debuff(self, debuff):
    for d in self.debuffs:
      if debuff.name == d.name and debuff.caused_by == d.caused_by:
        return True
    return False

  def buff(self, name, turns, attack,
           stat=None, operand=None, mult=None):
    buff = Status(name, turns, attack, stat, operand, mult)
    if not self.has_same_buff(buff):
      self.add_buff(buff)
    elif buff.name not in ["Frozen"]:
      self.update_buff(name, attack, turns)
    self.calc_stats()

  def debuff(self, name, turns, attack,
             stat=None, operand=None, mult=None):
    debuff = Status(name, turns, attack, stat, operand, mult)
    if not self.has_same_debuff(debuff):
      self.add_debuff(debuff)
    elif debuff.name not in ["Frozen"]:
      self.update_debuff(name, attack, turns)
    self.calc_stats()

  def update_buff(self, name, cause, turns):
    for b in self.buffs:
      if name == b.name and cause == b.caused_by:
        b.turns = turns

  def update_debuff(self, name, cause, turns):
    for d in self.debuffs:
      if name == d.name and cause == d.caused_by:
        d.turns = turns

  def change_speed(self, battle, attack, turns, speed):
    old_speed = self.stats["speed"]
    if speed == 0:
      return
    elif speed > 0:
      self.buff("Speed Buff", turns, attack, "speed", "add", speed)
    elif speed < 0:
      self.debuff("Speed Debuff", turns, attack,
                  "speed", "minus", speed)
    self.calc_stats()
    self.update_action(battle.queue, old_speed)
    battle.update_scene()

  def advance_forward(self, queue, mult):
    self.action -= (self.original_action * mult/100)
    if self.action < 0:
      self.action = 0
    self.update_queue(queue)

  def break_shield(self, battle, breaker):
    self.broken = True
    self.push_back(25)
    self.update_queue(battle.queue)
    battle.display_message(f"{self.display_name} was broken by {breaker.display_name}!")
    breaker.broke_enemy = True

  def update_queue(self, queue):
    queue.dequeue(queue.get_pos(self))
    queue.enqueue(self)

  def push_back(self, mult):
    self.action += (self.original_action * mult/100)

  def update_action(self, queue, old_speed):
    self.original_action = 1000/self.stats["speed"]
    if self.action != 0:
      distance = old_speed * self.action
      self.action = distance/self.stats["speed"]
      self.update_queue(queue)

  def unbreak(self, display):
    self.broken = False
    self.shield = self.max_shield
    self.hp_shield_bar.update(display)

  def can_act(self):
    if self.has_debuff("Frozen"):
      return False
    if self.has_debuff("Paralysis") and random.randint(1, 100) < 30:
      return False
    return True

  def use_power(self, battle, power, enemies):
    battle.update_scene()
    if len(enemies) == 1:
      names = enemies[0].display_name
    else:
      names = f"{', '.join([i.display_name for i in enemies[:-1]])} and {enemies[-1].display_name}"
    if power.type == "dmg":
      self.use_power_effect(battle, power, enemies, "hp")
    elif power.type == "slow":
      self.use_power_effect(battle, power, enemies, "speed")
    elif power.type == "heal":
      heal = round(self.stats["maxHp"]*power.power/100)
      battle.barb.recover_hp(battle, heal)
      battle.display_message(f"{self.display_name} healed for {heal} HP!")
    elif power.type == "weaken":
      self.use_power_effect(battle, power, enemies, "damage_mult")
    elif power.type == "buff":
      if power.internal_name == "DRAGONRIDER":
        self.buff("Ignore flying immunity", float("inf"), power)
        battle.display_message(f"{self.display_name} gained the ability to ignore flying immunity!")
      elif power.internal_name == "APPRENTICEWARDEN":
        heal = round(self.stats["maxHp"]*power.power/100)
        self.buff("Max HP Buff", 5, power, "maxHp", "add", heal)
        self.recover_hp(battle, heal)
        battle.display_message(f"{self.display_name} healed for {heal} HP and its max HP increased by the same amount!")
    power.reset_cooldown()
    return False

  def use_power_effect(self, battle, power, enemies, stat):
    if power.target == "SingleTarget":
      enemy = enemies[0]
      if stat == "hp":
        dmg = self.calc_power_damage(battle, power,
                                     self, enemy)
        enemy.take_damage(battle,dmg)
        battle.display_message(f"{enemy.display_name} was dealt {dmg} damage!")
      elif stat == "speed":
        enemy.change_speed(power.power)
      elif stat == "attack":
        enemy.debuff("Weakened", power.cooldown, power,
                     stat, "mult", power.power)
        battle.display_message(f"{enemy} was weakened!")
      self.power_effect(enemy, battle, power)
    elif power.target == "Blast":
      if stat == "hp":
        for enemy in enemies:
          if enemy == enemies[0]:
            dmg = self.calc_power_damage(battle, power,
                                         self, enemy)
          else:
            dmg = self.calc_power_damage(battle, power,
                                         self, enemy, False)
          enemy.take_damage(battle,dmg)
          battle.display_message(f"{enemy.display_name} was dealt {dmg} damage!")
      elif stat == "speed":
        for enemy in enemies:
          enemy.change_speed(power.power)
      elif stat == "attack":
        for enemy in enemies:
          enemy.debuff(
            "Weakened", power.cooldown, power,
            stat, "mult", power.power)
        battle.display_message(f"{', '.join([i.display_name for i in enemies[:-1]])} and {enemies[-1].display_name} were weakened!")
      for enemy in enemies:
        self.power_effect(enemy,battle,power)
    elif power.target == "AoE":
      if stat == "hp":
        for enemy in enemies:
          dmg = self.calc_power_damage(battle, power,
                                       self, enemy)
          enemy.take_damage(battle,dmg)
          battle.display_message(f"{enemy.display_name} was dealt {dmg} damage!")
      elif stat == "speed":
        for enemy in enemies:
          enemy.change_speed(power.power)
      elif stat == "attack":
        for enemy in enemies:
          enemy.debuff("Weakened", power.cooldown, power,
                       stat, "mult", power.power)
        battle.display_message("All enemies were weakened!")
      for enemy in enemies:
        self.power_effect(enemy, battle, power)

  def attack(self, battle, attack, user, enemies):
    battle.display_message(f"{self.display_name} used {attack.display_name}!")
    if all_flying(enemies) and not attack.attacks_flying() and not self.has_buff("Ignore flying immunity"):
      battle.display_message("But the attack couldn't reach!")
    elif type(enemies) is list:
      for enemy in reversed(enemies):
        self.process_attack(battle, attack, user, enemy)
        battle.update_scene()
    else:
      self.process_attack(battle, attack, user, enemies)
    return False

  def should_crit(self, battle, attack, user, enemy):
    if battle.mechanic == "No Player Crits" and user.owned_by_player():
      return False
    elif battle.mechanic == "No Enemy Crits" and not user.owned_by_player():
      return False
    elif battle.mechanic == "No Crits":
      return False
    return (random.randint(1,100) <= user.stats["crit_rate"])    

  def process_attack(self, battle, attack, user, enemy):
    if self.ability_is("DOUBLESTRIKE"):
      times = 2
    else:
      times = 1
    for i in range(times):
      crit = self.should_crit(battle, attack, user, enemy)
      if crit:
        battle.display_message("It was a critical hit!")
      damage = self.calc_damage(battle, attack, user, enemy, crit)
      self.damage_dealt += damage
      enemy.take_damage(battle, damage)
      battle.display_message(f"{enemy.display_name} was dealt {damage} damage!")
      enemy.trigger_ability(battle, "TakeDamage")
      if enemy.shield > 0 and (attack.element in enemy.weaknesses or self.has_weapon("RAINBOWSWORD", "sword")):
        enemy.reduce_shield(battle,attack.shield_damage,self)
      if enemy.stats["hp"] <= 0:
        enemy.faint(battle)
        break
    if attack.recoil_attack():
      damage = user.take_damage(battle, attack.recoil_damage(self.damage_dealt))
      if damage < 1:
        damage = 1
      battle.display_message(f"{user.display_name} took {damage} recoil damage!")
      if user.stats["hp"] <= 0:
        user.faint(battle)

  def update_bar(self, display):
    if self.hp_bar is not None:
      self.hp_bar.update(display)
    if self.hp_shield_bar is not None:
      self.hp_shield_bar.update(display)

  def take_damage(self, battle, damage):
    self.stats["hp"] -= damage
    if self.stats["hp"] < 0:
      self.stats["hp"] = 0
    self.update_bar(battle.display)
    return damage

  def recover_hp(self, battle, damage):
    self.stats["hp"] += damage
    if self.stats["hp"] > self.stats["maxHp"]:
      self.stats["hp"] = self.stats["maxHp"]
    self.update_bar(battle.display)

  def calc_damage(self, battle, attack, user, enemy, crit):
    critdmg = 1
    if crit:
      critdmg = 1.5
    if enemy.immune(attack, self):
      return 0
    base = ((2*user.level/5+2) * attack.power *
        (user.stats["attack"]/enemy.stats["defence"]))/50 + 2
    dmg = base * critdmg * (
        1+user.stats["damage_mult"]/100) / (
        1+enemy.stats["damage_reduction"]/100
    )
    if self.has_an_ability():
      dmg *= self.ability.damage_mult(battle, user, enemy)
    if enemy.has_debuff("Burned"):
      dmg *= 1.2
    if attack.element in enemy.resistances:
      dmg *= 0.7
    if enemy.shield > 0:
      dmg *= 0.9
    if dmg < 1:
      dmg = 1
    return round(dmg)

  def calc_true_damage(self, battle, power, user, enemy):
    base = ((2*user.level/5+2) * power *
        (user.stats["attack"]/enemy.stats["defence"]))/50 + 2
    dmg = base * (
        1+user.stats["damage_mult"]/100) / (
        1+enemy.stats["damage_reduction"]/100
    )
    if enemy.shield > 0:
      dmg *= 0.9
    if dmg < 1:
      dmg = 1
    return round(dmg)

  def calc_power_damage(self, battle, power, user, enemy, main=True):
    base_power = power.power
    if not main:
      base_power *= 0.5
    dmg = ((2*user.level/5+2) * base_power *
        (user.stats["attack"]/enemy.stats["defence"]))/50 + 2 * (
        1+user.stats["damage_mult"]/100) / (
        1+enemy.stats["damage_reduction"]/100
    )
    if power.element in enemy.resistances:
      dmg *= 0.7
    if enemy.shield > 0:
      dmg *= 0.9
    if dmg < 1:
      dmg = 1
    return round(dmg)

  def power_effect(self, enemy, battle, power):
    if (enemy.shield > 0) and ("WALLBREAKER" in power.internal_name or 
        power.element in enemy.weaknesses):
      enemy.reduce_shield(battle,power.shield_damage,self)
    if enemy.stats["hp"] <= 0:
      enemy.faint(battle)

  def immune(self, attack, enemy):
    if self.flying and not attack.attacks_flying() and not enemy.has_buff("Ignore flying immunity"):
      return True
    return False

  def ai(self, battle, enemies):
    attack = None
    enemy = random.choice(enemies)
    if self.broken:
      self.unbreak(battle.display)
    if self.internal_name == "HEALER":
      hps = [x.stats["hp"]/x.stats["maxHp"] for x in battle.enemy_troops if x is not self]
      if len(hps) > 0:
        enemies = [x for x in battle.enemy_troops if x is not self]
        enemy = enemies[hps.index(min(hps))]
        attack = self.active_attacks[0]
      else:
        attack = self.active_attacks[1]
    elif self.internal_name == "WITCH":
      skeletons = 0
      for troop in battle.enemy_troops:
        if troop.internal_name == "SKELETON":
          skeletons += 1
      if skeletons > 0:
        attack = self.active_attacks[1]
      else:
        attack = self.active_attacks[0]
    elif self.internal_name in ["GIANT", "HOGRIDER", "ICEWIZARD"] and enemy.debuffs == []:
      attack = self.active_attacks[0]
    elif self.internal_name == "ICEWIZARD" and enemy.has_debuff("Frozen"):
      attack =  self.active_attacks[1]
    else:
      attack = random.choice(self.active_attacks)
    if not attack.healing_attack():
      self.attack(battle, attack, self, enemy)
    attack.effect(battle, self, enemy)

