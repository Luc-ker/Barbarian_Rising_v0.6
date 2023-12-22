from Attack import Attack
import random

class BattleAttack(Attack):
    def __init__(self, attack):
        super().__init__(attack)

    def convert(self):
        attack_class = globals()[f"BattleAttack_{self.effect_code}"]
        atk = attack_class(self.internal_name)
        return atk

    def effect(self, battle, user, target): pass
    def get_power(self, battle, user, target): return self.power
    def recoil_damage(self, user, damage): return 0
    
    def attacks_flying(self): return "f" in self.flags
    def healing_attack(self): return "h" in self.flags
    def recoil_attack(self): return "r" in self.flags

class BattleAttack_000(BattleAttack):
    pass

class BattleAttack_BurnTarget(BattleAttack):
    def effect(self, battle, user, target):
      if target.has_debuff("Burn"):
        return
      if random.randint(1,100) < self.effect_chance:
        battle.display_message(f"{target.display_name} is burned for {self.effect_turns} turns!")
        target.debuff("Burn", self.effect_turns, self)

class BattleAttack_DelayTarget20(BattleAttack):
    def effect(self, battle, user, target):
      target.push_back(20)
      battle.display_message(f"{target.display_name} was pushed back!")

class BattleAttack_DoublePowerAgainstFrozen(BattleAttack):
    def get_power(self, battle, user, target):
      if target.has_debuff("Frozen"):
        return self.power*2
      return self.power

class BattleAttack_DoublePowerAgainstParalysed(BattleAttack):
    def get_power(self, battle, user, target):
      if target.has_debuff("Paralysed"):
        return self.power*2
      return self.power

class BattleAttack_FreezeTarget(BattleAttack):
    def effect(self, battle, user, target):
      if target.has_debuff("Frozen"):
        return
      if random.randint(1,100) < self.effect_chance:
        target.debuff("Frozen", self.effect_turns, self)
        battle.display_message(f"{target.display_name} is frozen for {self.effect_turns} turns!")

class BattleAttack_HealAlly(BattleAttack):
    def effect(self, battle, user, target):
        heal = round(user.stats["maxHp"]*self.power/100)
        target.recover_hp(battle, heal)
        battle.display_message(f"{user.display_name} healed {target.display_name} for {heal} HP!")

class BattleAttack_IncreaseUserDef50(BattleAttack):
    def effect(self, battle, user, target):
        user.buff("Defence Boost", self.effect_turns,
                      self, "defence", "mult", 0.5)
        battle.display_message(f"{user.display_name}'s defence increased by 50%!")

class BattleAttack_IncreaseUserDmgReduction20(BattleAttack):
    def effect(self, battle, user, target):
        user.buff("Defence Boost", self.effect_turns,
                      self, "damage_reduction", "add", 20)
        battle.display_message(f"{user.display_name} takes 20% less damage for {self.effect_turns} turns!")

class BattleAttack_IncreaseUserSpd10(BattleAttack):
    def effect(self, battle, user, target):
        user.change_speed(battle, self, self.effect_turns,
                          user.stats["speed"]*0.1)
        battle.display_message(f"{user.display_name}'s speed increased by 10%!")

class BattleAttack_IncreaseUserSpd20(BattleAttack):
    def effect(self, battle, user, target):
        user.change_speed(battle, self, self.effect_turns,
                          user.stats["speed"]*0.2)
        battle.display_message(f"{user.display_name}'s speed increased by 20%!")

class BattleAttack_LowerTargetAtk30(BattleAttack):
    def effect(self, battle, user, target):
        target.debuff("Attack Reduction", self.effect_turns,
                      self, "attack", "mult", 0.3)
        battle.display_message(f"{target.display_name}'s attack decreased by 30%!")

class BattleAttack_LowerTargetDef10(BattleAttack):
    def effect(self, battle, user, target):
        target.debuff("Defence Reduction", self.effect_turns,
                      self, "defence", "mult", 0.1)
        battle.display_message(f"{target.display_name}'s defence decreased by 10%!")

class BattleAttack_LowerTargetDef30(BattleAttack):
    def effect(self, battle, user, target):
        target.debuff("Defence Reduction", self.effect_turns,
                      self, "defence", "mult", 0.3)
        battle.display_message(f"{target.display_name}'s defence decreased by 30%!")

class BattleAttack_ParalyseTarget(BattleAttack):
    def effect(self, battle, user, target):
      if target.has_debuff("Paralysis"):
        return
      if random.randint(1,100) < self.effect_chance:
        battle.display_message(f"{target.display_name} is paralysed for {self.effect_turns} turns!")
        target.debuff("Paralysis", self.effect_turns, self)
        target.change_speed(battle, self, self.effect_turns,
                          -target.stats["speed"]*0.25)
      
class BattleAttack_RecoilAttack(BattleAttack):
    def recoil_damage(self, damage):
      return round(damage/4)
      
class BattleAttack_SkeletonPowerUp(BattleAttack):
    def get_power(self, battle, user, target):
      mult = 1
      for troop in battle.enemy_troops:
        if troop.internal_name == "SKELETON":
          mult += 0.5
      return self.power*mult
      
class BattleAttack_SelfKO(BattleAttack):
    def effect(self, battle, user, target):
      user.take_damage(battle, user.stats["hp"])
      user.faint(battle)
      