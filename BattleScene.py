from Screen_Objects import HPBar, HPShieldBar, Image, EnemyImage, BattlePowerImage, AVImage, BattleChoiceButton, font
from sys import exit
from Game import pygame, display, QUIT, blit_message, blue, green

back_butt = BattleChoiceButton(448, 262, 102, 32, "Back",
                              blue, blue, green, -1)

def remove_targets(battle):
  for enemy in battle.enemy_troops:
    enemy.graphic.remove_target(battle)

def set_troop_image(troop, pos, back):
  ability = troop.stats['ability_level']
  if ability == 0:
    ability = 1
  opened = False
  while not opened:
    try:
      name = troop.internal_name
      if back == "p":
        troop.graphic = Image(
          f"Troops/{name}/{name}-{ability}_p.png", pos, True
        )
      elif back == "e":
        troop.graphic = EnemyImage(
          f"Troops/{name}/{name}-{ability}_e.png",
          pos, True
        )
      opened = True
    except FileNotFoundError:
      ability -= 1

def load_images(barb, enemies, bg, update=True):
  bg = Image(f"Backgrounds/{bg}", (0,0))
  set_troop_image(barb, (50,70), "p")
  barb.graphic.pos.bottom = 230
  barb.hp_bar = HPBar(barb, (20, 68))
  left = 205
  top = 10
  for enemy in enemies:
    set_troop_image(enemy, (left,220), "e")
    enemy.graphic.pos.bottom = 260
    enemy.hp_shield_bar = HPShieldBar(enemy, (262,top))
    left += enemy.graphic.rect.width
    top += 53
  images = [bg, barb.hp_bar, barb.graphic] + [x.hp_shield_bar for x in enemies] + [x.graphic for x in enemies]
  if update: update_scene(images)
  return images

def update_scene(events):
  for event in events:
    event.draw(display)
  pygame.display.update()

def choose_action(battle):
  attack = BattleChoiceButton(0, 262, 102, 32, "ATTACK",
                              blue, blue, green, 1)
  power = BattleChoiceButton(410, 262, 102, 32, "POWER",
                             blue, blue, green, 2)
  events = battle.graphics + battle.AV_Icons + [attack, power]
  update_scene(events)
  blit_message(battle.player, "What will you do?",
               speed="Fast", removeBox=False)
  choice = None
  
  while True:
    for event in pygame.event.get():
      pygame.display.update()
      if event.type == QUIT:
        pygame.quit()
        exit()
      elif (event.type == pygame.MOUSEBUTTONDOWN or
            event.type == pygame.KEYDOWN):
        for i in events:
          if type(i) != EnemyImage:
            choice = i.handle_event(event, display)
          if choice != -1 and choice is not None:
            i.draw(display)
            pygame.display.update()
            return choice

def select_attack(battle):
  troop = battle.barb
  attacks = []
  left = 0
  for i,attack in enumerate(troop.active_attacks):
    width = font.render(attack.display_name, True,
                        blue).get_width() + 10
    attacks.append(
      BattleChoiceButton(left, 262, width, 32,
                         attack.display_name, blue,
                         blue, green, i)
    )
    width += 10
    left += width
  events = battle.graphics + battle.AV_Icons + attacks + [back_butt]
  update_scene(events)    
  blit_message(battle.player, "Select an attack to use.",
               speed="Fast", removeBox=False)
  choice = None
  
  while True:
    for event in pygame.event.get():
      pygame.display.update()
      if event.type == QUIT:
        pygame.quit()
        exit()
      elif (event.type == pygame.MOUSEBUTTONDOWN or
            event.type == pygame.KEYDOWN):
        for i in reversed(events):
          if type(i) != EnemyImage:
            choice = i.handle_event(event, display)
          if choice == -1:
            return None
          elif choice is not None and (choice >= 0 and choice < len(troop.active_attacks)):
            i.draw(display)
            pygame.display.update()
            return troop.active_attacks[choice]

def select_power(battle):
  player = battle.player
  powers = []
  for i,power in enumerate(player.active_powers):
    powers.append(
      BattlePowerImage(f"Troops/Icons/{power.internal_name}.png",
                       (70*i,234), power.cooldown, i)
    )  
  events = battle.graphics + battle.AV_Icons + powers + [back_butt]
  update_scene(events)    
  blit_message(battle.player, "Select an power to use.",
               speed="Fast", removeBox=False)
  choice = None
  
  while True:
    for event in pygame.event.get():
      pygame.display.update()
      if event.type == QUIT:
        pygame.quit()
        exit()
      elif (event.type == pygame.MOUSEBUTTONDOWN or
            event.type == pygame.KEYDOWN):
        for i in reversed(events):
          if type(i) != EnemyImage:
            choice = i.handle_event(event, display)
          if choice == -1:
            return None
          elif (choice is not None and choice >= 0 and 
                choice < len(player.active_powers)):
            i.draw(display)
            pygame.display.update()
            return player.active_powers[choice]
            
def select_target(battle,attack):
  enemies = battle.enemy_troops
  enemy_graphics = [x.graphic for x in enemies]
  events = battle.graphics + battle.AV_Icons + [back_butt]
  remove_targets(battle)
  update_scene(events)

  if attack.target == "SingleTarget":
    target = enemy_graphics[len(enemies)//2]
    target.add_target(display)
  elif attack.target == "Blast":
    if len(enemy_graphics) == 1:
      enemy_graphics[0].add_target(display)
      enemy_graphics[0].main_target = True
    else:
      target = enemy_graphics[len(enemies)//2]
      target.main_target = True
      for i,x in enumerate(enemy_graphics):
        if target is x:
          target.add_target(display)
          if i == 0:
            enemy_graphics[1].add_target(display)
          elif i == len(enemies)-1:
            enemy_graphics[-2].add_target(display)
          else:
            enemy_graphics[i+1].add_target(display)
            enemy_graphics[i-1].add_target(display)
  elif attack.target == "AoE":
    for enemy in enemy_graphics:
      enemy.add_target(display) 
  blit_message(battle.player, "Select target(s).",
               speed="Fast", removeBox=False)
  
  while True:
    retarget = True
    for event in pygame.event.get():
      pygame.display.update()
      if event.type == QUIT:
        pygame.quit()
        exit()
      elif (event.type == pygame.MOUSEBUTTONDOWN or
            event.type == pygame.KEYDOWN):
        for i in reversed(events):
          if type(i) == EnemyImage:
            choice = i.handle_event(event, battle, retarget,
                                    attack.target, enemy_graphics)
          else:
            choice = i.handle_event(event, battle.display)
          if choice == -1:
            return None
          elif choice == 0:
            retarget = False
          elif choice == 1:
            i.draw(display)
            pygame.display.update()
            targets = [x for x in enemies if x.graphic.targeted]
            if attack.target != "Blast":
              return targets
            else:
              main = [x for x in enemies if x.graphic.main_target]
              targets.remove(main[0])
              return main + targets

def get_action_order_icons(queue):
  left = 2
  troops = []
  for troop in queue:
    troops.append(
      AVImage(f"/Troops/Icons/{troop.internal_name}.png",
              (left,2), round(troop.action), True)
    )
    left += 62
  return troops
  
def main():
  pass

if __name__ == '__main__':
  main()
