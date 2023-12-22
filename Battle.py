from BattleTroop import BattleTroop
from Player import Player
from Turn_Order import PriorityQueue
from Game import display_message, display
from BattleLoader import create_enemies
import BattleScene

def digit_range_check(vari,min=0,max=9):
  if len(vari) != 1 or vari.isdigit() is False or (int(vari) < min or int(vari) > max):
    return False
  return True

class Battle():
  def __init__(self, player, battle, mechanic=None, bg="grass.jpg"):
    if type(player) != Player:
      return
    self.player = player
    self.barb = BattleTroop(player.barb)
    self.player_troops = [self.barb]
    self.waves = []
    enemy_troops = create_enemies(battle)
    for waves in enemy_troops:
      self.waves.append([BattleTroop(x) for x in waves])
    self.mechanic = mechanic
    self.wave = 1
    self.max_waves = len(self.waves)
    self.display = display
    self.result = None
    self.bg = bg
    self.start()

  def wave_enemies_beaten(self):
    if self.enemy_troops == []:
      return True
    return False

  def all_enemies_beaten(self):
    if self.waves == [[]]:
      return True
    return False

  def get_queue(self):
    return self.queue.queue

  def get_action_order_icons(self):
    return BattleScene.get_action_order_icons(self.get_queue())

  def display_message(self, message):
    return display_message(self.player, message)

  def update_enemies(self):
    self.graphics = BattleScene.load_images(self.barb, self.enemy_troops,
                                            self.bg, update=False)

  def update_scene(self):
    return BattleScene.update_scene(self.graphics + self.AV_Icons)

  def spawn_enemy(self, enemy, level):
    troop = BattleTroop(enemy, level)
    self.enemy_troops.append(troop)
    self.queue.enqueue(troop)
    self.AV_Icons = self.get_action_order_icons()
    self.update_enemies()
    self.update_scene()

  def start(self):
    if self.mechanic == "Endless":
      self.waves.append([BattleTroop(x.internal_name, x.level) for x in self.waves[0]])
    self.enemy_troops = self.waves[0]
    enemies = self.enemy_troops
    if len(enemies) == 1:
      print(f"Battle occured between {self.barb.display_name} vs {enemies[0].display_name}")
    else:
      print(f"Battle occured between {self.barb.display_name} vs {', '.join([i.display_name for i in enemies[:-1]])} and {enemies[-1].display_name}")
    self.queue = PriorityQueue()
    self.troops = self.player_troops + self.enemy_troops
    for troop in self.troops:
      troop.reset_AV()
      self.queue.enqueue(troop)
    self.graphics = BattleScene.load_images(self.barb, self.enemy_troops,
                                            self.bg, update=False)
    self.AV_Icons = self.get_action_order_icons()
    self.update_scene()
    self.main_loop()

  def main_loop(self):
    self.display_message(f"Wave {self.wave}/{self.max_waves}")
    for troop in self.troops:
      troop.trigger_ability(self, "BattleStart")
    while self.barb.stats["hp"] >= 0 and not self.wave_enemies_beaten():
      self.queue.to_zero()
      self.AV_Icons = self.get_action_order_icons()
      BattleScene.update_scene(self.graphics+self.AV_Icons)
      troop = self.get_queue()[0]
      troop.turns_taken += 1
      troop.trigger_ability(self, "TurnStart")
      if troop.owner == "Player":
        can_attack = troop.can_act()
        targets = None
        attack = None
        while can_attack:
          choice = BattleScene.choose_action(self)
          if choice == 1:
            attack = BattleScene.select_attack(self)
            if attack is not None:
              targets = BattleScene.select_target(self, attack)
            if targets is not None:
              BattleScene.remove_targets(self)
              self.update_scene()
              can_attack = troop.attack(self, attack, troop, targets)
          elif choice == 2:
            power = BattleScene.select_power(self)
            if power is None:
              pass
            elif power.type not in ["buff", "heal"]:
              targets = BattleScene.select_target(self, power)
            elif power.type in ["buff", "heal"]:
              can_attack = troop.use_power(self, power, [troop])
            if targets is not None:
              BattleScene.remove_targets(self)
              can_attack = troop.use_power(self, power, targets)
        if attack is not None:
          attack.effect(self, troop, targets)
        for power in self.player.active_powers:
          if power.cooldown > 0:
            power.cooldown -= 1
      else:
        troop.ai(self, self.player_troops)
      troop.trigger_ability(self, "AttackEnd")
      if self.barb.stats["hp"] <= 0:
        self.display_message("You lost and are forced to retreat...")
        self.result = 0
        self.barb.stats["hp"] = self.barb.stats["maxHp"]
        return
      elif self.wave_enemies_beaten():
        if self.all_enemies_beaten():
          self.display_message("You won!")
          self.result = 1
          self.barb.stats["hp"] = self.barb.stats["maxHp"]
          return
        else:
          self.waves.pop(0)
          self.enemy_troops = self.waves[0]
          self.wave += 1
          self.start()
          return
      if troop.stats["hp"] > 0:
        self.queue.dequeue()
        troop.reset_AV()
        self.queue.enqueue(troop)
        if troop.broke_enemy:
          troop.advance_forward(self.queue, 90)
          troop.broke_enemy = False
        for buff in troop.buffs:
          buff.turns -= 1
          if buff.turns <= 0:
            troop.buffs.remove(buff)
        for debuff in troop.debuffs:
          debuff.turns -= 1
          if debuff.turns <= 0:
            troop.debuffs.remove(debuff)
        old_speed = troop.stats["speed"]
        troop.calc_stats()
        troop.update_action(self.queue, old_speed)
        troop.damage_dealt = 0
        troop.trigger_ability(self, "TurnEnd")
