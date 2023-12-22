from Ability import Ability

class BattleAbility(Ability):
    def __init__(self, ability):
        super().__init__(ability)

    def can_trigger(self, user, battle):
      return not user.ability_triggered

    def convert(self):
        ability_class = globals()[f"BattleAbility_{self.internal_name}"]
        abil = ability_class(self.internal_name)
        return abil

    def effect(self, battle, user): pass
    def damage_mult(self, battle, user, target): return 1
      
class BattleAbility_BALLOONPARADE(BattleAbility):
    def damage_mult(self, battle, user, target):
      mult = 1
      for troop in battle.enemy_troops:
        if troop.internal_name == "BALLOON":
          mult += 0.5
      return mult
      
class BattleAbility_CRASHANDBURN(BattleAbility):
    def effect(self, battle, user):
      damage = user.stats["maxHp"]*0.5*user.stats["ability_level"]
      battle.display_message(f"{user.display_name} crashed, dealing {round(damage)} damage!")
      battle.barb.take_damage(battle, damage)
      
class BattleAbility_DOUBLESTRIKE(BattleAbility):  
    pass

class BattleAbility_FAREWELLGIFT(BattleAbility):
    def effect(self, battle, user):
      damage = user.stats["maxHp"]*0.05*user.stats["ability_level"]
      battle.display_message(f"{user.display_name} left a parting gift, dealing {round(damage)} damage!")
      battle.barb.take_damage(battle, damage)

class BattleAbility_FREEZEBLAST(BattleAbility):
    def effect(self, battle, user):
      turns = round(user.stats["ability_level"]/2)
      battle.display_message(f"{user.display_name} exploded, freezing {battle.barb.display_name} for {turns} turns!")
      battle.barb.debuff("Frozen", turns, self)

class BattleAbility_IRONFIST(BattleAbility):
    def can_trigger(self, user, battle):
     return super().can_trigger(user, battle) and user.stats["hp"] <= user.stats["maxHp"]/2
      
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name}'s rage kicked in!")
      user.advance_forward(battle.queue, 50)
      user.buff("Attack Buff", 2, self, "attack",
                "mult", 1+0.05*user.stats["ability_level"])
      user.recover_hp(battle, user.stats["ability_level"]*user.stats["maxHp"]/20)

class BattleAbility_LAVAREPUPDUCTION(BattleAbility):
    def can_trigger(self, user, battle):
      return len(battle.enemy_troops) < 3
      
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name} released a Lava Pup!")
      battle.spawn_enemy("LAVAPUP", user.level)
      
class BattleAbility_LIFEAURA(BattleAbility):
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name}'s Life Aura activated, giving all troops on its side a HP buff!")
      for troop in battle.enemy_troops:
        hp_buff = 0.1 * user.stats["maxHp"] * user.stats["ability_level"]
        troop.buff("Max HP Buff", float("inf"), self, "maxHp",
                "add", hp_buff)
        troop.recover_hp(battle, hp_buff)
      
class BattleAbility_LIGHTNINGBURST(BattleAbility):
    def can_trigger(self, user, battle): return True
      
    def effect(self, battle, user):
      heal = round(user.damage_dealt/5)
      battle.display_message(f"The lingering lightning healed {user.display_name} for {heal} HP!")
      user.recover_hp(battle, heal)
      
class BattleAbility_NECROMANCER(BattleAbility):
    def can_trigger(self, user, battle):
      return len(battle.enemy_troops) < 3 and user.turns_taken % 2 == 1

    def effect(self, battle, user):
      battle.display_message(f"{user.display_name} summoned skeletons to help her!")
      while len(battle.enemy_troops) < 3:
        battle.spawn_enemy("SKELETON", user.level)
      
class BattleAbility_PYROKINETIC(BattleAbility):
    def damage_mult(self, battle, user, target):
      if target.has_debuff("Burned"):
        return 1+0.1*user.stats["ability_level"]
      return 1

class BattleAbility_RAGE(BattleAbility):
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name}'s rage kicked in!")
      user.advance_forward(battle.queue, 50)
      user.buff("Attack Buff", 2, self, "attack",
                "mult", 0.05*user.stats["ability_level"])

class BattleAbility_RAGE2(BattleAbility):
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name}'s rage kicked in!")
      user.advance_forward(battle.queue, 50)
      user.buff("Attack Buff", 2, self, "attack",
                "mult", 0.5+0.05*user.stats["ability_level"])

class BattleAbility_RAMPUP(BattleAbility):
    def can_trigger(self, user, battle): return True
      
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name} is ramping up!")
      user.buff("Attack Buff", 1, self, "attack",
                "mult", 1 + 0.01*user.stats["ability_level"] + 0.05*user.turns_taken)

class BattleAbility_REPULSIONFIELD(BattleAbility):
    def can_trigger(self, user, battle): return True
      
    def effect(self, battle, user):
      damage = user.calc_true_damage(battle, 50, user, battle.barb)
      battle.display_message(f"{user.display_name}'s electric field dealt {battle.barb.display_name} {damage} damage!")
      battle.barb.take_damage(battle, damage)      

class BattleAbility_ROCKETTHRUSTERS(BattleAbility):
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name} got a flying start to the battle!")
      user.change_speed(battle, self, 2,
                        user.stats["speed"]*(0.5+0.1*user.stats["ability_level"]))

class BattleAbility_SPLITAPART(BattleAbility):
    def effect(self, battle, user):
      battle.display_message(f"{user.display_name} split apart!")
      while len(battle.enemy_troops) < 3:
        battle.spawn_enemy("GOLEMITE", user.level)
      
class BattleAbility_TANTRUM(BattleAbility):
    def damage_mult(self, battle, user, target):
      if len(battle.enemy_troops) == 1:
        return 2
      return 1
      