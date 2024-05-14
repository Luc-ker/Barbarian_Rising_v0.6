import pygame
import Troop
import Power
import re

pygame.init()
font = pygame.font.SysFont('ariel', 36)
strike_font = pygame.font.SysFont('ariel', 36)
font_smaller = pygame.font.SysFont('ariel', 28)
strike_font.strikethrough = True
grey = (80,80,80,100)
black = pygame.Color("Black")
red = pygame.Color("Red")
green = pygame.Color("Green")
pattern = "^[a-zA-Z0-9!@#$&()\\-`.+,/\"]*$"

class Image():
  def __init__(self, image, pos, alpha=False):
    if alpha:
      self.graphic = pygame.image.load(f"./Graphics/{image}").convert_alpha()
    elif not alpha:
      self.graphic = pygame.image.load(f"./Graphics/{image}").convert()
    self.name = image
    self.rect = self.graphic.get_rect()
    self.pos = self.rect.move(pos)
    self.top_left = pos

  def draw(self, display):
    display.blit(self.graphic, self.pos)

  def get_size(self):
    return self.graphic.get_size()

  def handle_event(self, event, display):
    return None

class BattlePowerImage(Image):
  def __init__(self, image, pos, cooldown, choice):
    super().__init__(image, pos, True)    
    self.cdGraphic = Image("Pictures/cooldown image.png", self.top_left, True)
    self.cooldown = cooldown
    self.choice = choice

  def draw(self, display):
    super().draw(display)
    if self.cooldown > 0:
      self.cdGraphic.draw(display)
      cd_text = Text(str(self.cooldown), (0, 0))
      cd_text.rect.center = self.pos.center
      cd_text.draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos) and self.cooldown == 0:
        return self.choice

class EnemyImage(Image):
  def __init__(self, image, pos, alpha=False):
    super().__init__(image, pos, alpha)
    self.targeted = False
    self.main_target = False
    self.target_icon = None
      
  def add_target(self, display):
    self.targeted = True
    if self.main_target:
      self.target_icon = Image("Pictures/Battle/Target Icon large.png", (0, 0), True)
    else:
      self.target_icon = Image("Pictures/Battle/Target Icon small.png", (0, 0), True)
    self.target_icon.pos.center = self.pos.center
    self.target_icon.draw(display)
    pygame.display.update()

  def remove_target(self, battle):
    if self.target_icon is not None:
      self.targeted = False
      self.main_target = False
      battle.display.blit(battle.graphics[0].graphic, self.target_icon.pos, self.target_icon.pos)
      battle.display.blit(self.graphic, self.pos)
      pygame.display.update()

  def handle_event(self, event, battle, targeting=False, atkTarget=None, enemies=[]):
    display = battle.display
    if targeting:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if self.pos.collidepoint(event.pos):
          if self.targeted and not atkTarget == "Blast" or self.main_target:
            return 1 # return targeted opponents
          if self.name != "Target-icon small.png":
            for enemy in enemies:
              enemy.remove_target(battle)
            if atkTarget == "AoE":
              for enemy in enemies:
                enemy.add_target(display)
            elif atkTarget == "Blast":
              self.main_target = True
              if len(enemies) == 1:
                self.add_target(display)
              else:
                for i,x in enumerate(enemies):
                  if self is x:
                    if i == 0:
                      self.add_target(display)
                      enemies[1].add_target(display)
                    elif i == len(enemies)-1:
                      self.add_target(display)
                      enemies[-2].add_target(display)
                    else:
                      self.add_target(display)
                      enemies[i+1].add_target(display)
                      enemies[i-1].add_target(display)
            elif atkTarget == "SingleTarget":
              self.add_target(display)
            return 0
        pygame.display.update()
    return None

class ScreenChangeImage(Image):
  def __init__(self, image, pos, mode, alpha=False):
    super().__init__(image, pos, alpha)
    self.mode = mode

  def handle_event(self, event, display, mode):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        return self.mode
      else:
        self.active = False
    return mode

class AVImage(Image):
  def __init__(self, image, pos, AV, alpha=False):
    super().__init__(image, pos, alpha)
    self.AV = font.render(str(AV), True, black)

  def draw(self, display):
    super().draw(display)
    display.blit(self.AV, self.pos)

class UpgradeTroopImage(Image):
  def __init__(self, image, pos, troop, player, alpha=True, barb=False):
    super().__init__(image, pos, alpha)
    self.troop = troop
    self.player = player

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.troop is None: return
      if self.pos.collidepoint(event.pos):
        return self.troop.can_upgrade(self.player)

  def draw(self, display):
    super().draw(display)
    if self.troop is None:
      Image("Pictures/power greyed.png", self.pos.topleft, True).draw(display)

  def drawBarbStatsText(self, display, stats, positions):
    Text(f"Lv. {stats[0]}", positions[0]).draw(display)
    Text(f"HP: {stats[1]}", positions[1]).draw(display)
    Text(f"Atk: {stats[2]}", positions[2]).draw(display)
    Text(f"Def: {stats[3]}", positions[3]).draw(display)
    Text(f"Spd: {stats[4]}", positions[4]).draw(display)
    Text(f"Ability Lv: {stats[5]}", positions[5]).draw(display)

  def drawBarbStats(self, display):
    Image("Pictures/barb stat box.png", (20, 20), True).draw(display)
    stats = self.get_troop_stats(self.troop.level)
    positions = [(24,70), (24,98), (136,98), (24,126), (136,126), (24,154)]
    self.drawBarbStatsText(display, stats, positions)
    stats = self.get_troop_stats(self.troop.level+1)
    costs = self.troop.get_upgrade_costs(self.troop.level+1)
    Image("Pictures/Loot Icons/GOLD.png", (138,26), True).draw(display)
    Text(f"{costs[2]}", (172,28)).draw(display)
    Image("Pictures/Loot Icons/ELIXIR.png", (140,61), True).draw(display)
    Text(f"{costs[1]}", (172,63)).draw(display)
    positions = [(393,70), (269,98), (382,98), (269,126), (382,126), (269,154)]
    self.drawBarbStatsText(display, stats, positions)    

  def drawPowerStatsText(self, display, stats, positions):
    Text(f"Lv. {stats[0]}", positions[0]).draw(display)
    Text(f"Base Power: {stats[1]}", positions[1]).draw(display)

  def drawPowerStats(self, display):
    Image("Pictures/power stat box.png", (20, 20), True).draw(display)
    stats = self.get_power_stats(self.troop.level)
    positions = [(24,126), (24,154)]
    self.drawPowerStatsText(display,stats,positions)
    stats = self.get_power_stats(self.troop.level+1)
    Image("Pictures/Loot Icons/ELIXIR.png", (200,61), True).draw(display)
    Text(f"{stats[-1]}", (232,63)).draw(display)
    positions = [(392,126), (291,154)]
    self.drawPowerStatsText(display,stats,positions)

  def get_troop_stats(self, level):
    return Troop.get_base_stats(self.troop.internal_name, level)

  def get_power_stats(self, level):
    return Power.get_base_stats(self.troop.internal_name, level)

class UpgradeButtonImage(Image):
  def __init__(self, image, pos, player, troop, mode="upgrade", alpha=False):
    super().__init__(image, pos, alpha)
    self.troop = troop
    self.player = player
    self.mode = mode
    self.active = False

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.troop is None: return
      if self.pos.collidepoint(event.pos):
        if self.mode == "upgrade":
          self.troop.level_up(self.player, 1)
        self.active = True
        return self.troop.can_upgrade(self.player)

class PowerImage(Image):
  def __init__(self, image, pos, player, alpha=True):
    super().__init__(image, pos, alpha)
    self.player = player
    self.powerName = self.name[13:-4]
    self.active = self.powerName in [x.internal_name for x in player.active_powers]
    self.tick = Image("Pictures/Equip Screen/tick mark.png", (0,0), True)
    self.tick.pos.center = (pos[0]+55,pos[1])

  def draw(self, display):
    super().draw(display)
    if self.active: self.tick.draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        if self.player.has_active_power(self.powerName):
          self.player.unequip_power(self.powerName)
          self.active = False
          return 12
        elif self.player.can_equip_power():
          self.player.equip_power(self.powerName)
          self.active = True
          return 12
        else:
          return 11

class WeaponImage(Image):
  def __init__(self, image, pos, barb, weapon, alpha=True):
    super().__init__(image, pos, alpha)
    self.barb = barb
    self.weapon = weapon
    self.weaponIntName = weapon.internal_name
    self.weaponName = weapon.display_name
    self.equipped = (barb.weapons[weapon.type] is weapon)
    self.tick = Image("Pictures/Equip Screen/tick mark.png", (0,0), True)
    self.tick.pos.center = (pos[0]+55,pos[1])

  def draw(self, display):
    super().draw(display)
    if self.equipped:
      self.tick.draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        if self.barb.equipped(self.weapon):
          self.barb.unequip_weapon(self.weapon.type)
        else:
          self.barb.equip_weapon(self.weapon)
      self.equipped = self.barb.weapons[self.weapon.type] is self.weapon
      if self.pos.collidepoint(event.pos):
        return 13

class LootFarmImage(Image):
  def __init__(self, image, pos, type, alpha=False):
    super().__init__(image, pos, alpha)
    self.type = type

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        return 1

class DiffImage(Image):
  def __init__(self, image, pos, diff, output, alpha=True):
    super().__init__(image, pos, alpha)
    self.diff = diff
    self.selected = False
    self.output = output

  def draw(self, display):
    super().draw(display)
    if self.selected and "mult" not in self.name:
      pos = (self.top_left[0]-2, self.top_left[1]-2)
      Image("Pictures/Buttons/diff select.png", pos, True).draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        self.selected = True
        return self.output
        
class HPBar(Image):
  def __init__(self, troop, pos):
    super().__init__("Pictures/Battle/HP Bar.png", pos)
    self.troop = troop
    self.HPposX = pos[0] + 30
    self.HPposY = pos[1] + 27
    width = 140*(troop.stats["hp"]/troop.stats["maxHp"])
    self.HP = pygame.Rect(self.HPposX, self.HPposY,width,8)

  def draw(self, display):
    display.blit(self.graphic, self.pos)
    pygame.draw.rect(display, green, self.HP)
    name = Text(self.troop.display_name, (self.pos[0]+5, self.pos[1]+3), font=font_smaller)
    name.draw(display)

  def update(self, display):
    width = 140*(self.troop.stats["hp"]/self.troop.stats["maxHp"])
    self.HP = pygame.Rect(self.HPposX, self.HPposY,width,8)
    self.draw(display)
    
class HPShieldBar(Image):
  def __init__(self, troop, pos):
    super().__init__("Pictures/Battle/HP Shield Bar.png",pos)
    self.troop = troop
    self.shieldposX = pos[0] + 30
    self.shieldposY = pos[1] + 27
    self.HPposX = pos[0] + 30
    self.HPposY = pos[1] + 40
    hpWidth = 200*(troop.stats["hp"]/troop.stats["maxHp"])
    self.HP = pygame.Rect(self.HPposX, self.HPposY,hpWidth,8)
    shieldWidth = 200*(troop.shield/troop.max_shield)
    self.shield = pygame.Rect(self.shieldposX, self.shieldposY,shieldWidth,8)

  def draw(self, display):
    display.blit(self.graphic, self.pos)
    pygame.draw.rect(display, red, self.shield)
    pygame.draw.rect(display, green, self.HP)
    name = Text(self.troop.display_name, (self.pos[0]+5, self.pos[1]+3), font=font_smaller)
    name.draw(display)
    right = self.pos.right - 4
    weaknesses = reversed(self.troop.weaknesses)
    for weak in weaknesses:
      type_image = Image(f"Types/{weak}.png", (0, 0), True)
      type_image.pos.right = right
      type_image.pos.bottom = self.shieldposY - 5
      type_image.draw(display)
      right -= 20 

  def update(self, display):
    shieldWidth = 200*(self.troop.shield/self.troop.max_shield)
    self.shield = pygame.Rect(self.shieldposX, self.shieldposY,shieldWidth,8)
    width = 200*(self.troop.stats["hp"]/self.troop.stats["maxHp"])
    self.HP = pygame.Rect(self.HPposX, self.HPposY,width,8)
    self.draw(display)

class UpgradeWeaponImage(Image):
  def __init__(self, weapon, pos):
    self.weapon = weapon
    self.weaponName = weapon.internal_name
    super().__init__(f"Weapons/{weapon.internal_name}.png", pos, True)

  def draw(self, display):
    super().draw(display)
    Text(f"{self.weapon.level}",self.pos).draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        return 6

class ShopWeaponImage(Image):
  def __init__(self, weapon, pos):
    super().__init__(f"Weapons/{weapon}.png", pos, True)
    self.cost = 0
    self.return_value = 0
    self.obtainable = True
    self.obtained = False
    self.buyable = True
    self.weapon = weapon

  def draw(self, display):
    super().draw(display)
    cost_image = Image("Pictures/Shop cost.png", (0,0), True)
    cost_image.pos.top = self.pos.bottom + 12
    cost_image.pos.centerx = self.pos.centerx
    cost_image.draw(display)
    if self.obtained:
      sold = Image("Pictures/sold out.png", (0,0), True)
      sold.pos.center = self.pos.center
      sold.draw(display)
    if not self.obtainable:
      grey = Image("Pictures/cooldown image.png", (0,0), True)
      grey.pos.center = self.pos.center
      grey.draw(display)
      text = Text(f"{self.cost}",self.pos,red,font=strike_font)
    elif not self.buyable or self.obtained:
      text = Text(f"{self.cost}",self.pos,red)
    else:
      text = Text(f"{self.cost}",self.pos,(0,255,0))
    text.rect.center = cost_image.pos.center
    text.draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        if self.obtainable and self.buyable:
          return self.return_value

class SettingsArrow(Image):
  def __init__(self, image, pos, direction):
    super().__init__(image, pos, True)
    self.direction = direction

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.pos.collidepoint(event.pos):
        return self.direction
  
class Button():
  def __init__(self, x, y, w, h, txtColor, inactiveColor, activeColor, text, bgColor=None):
    self.rect = pygame.Rect(x, y, w, h)
    self.color = inactiveColor
    self.activeCol = activeColor
    self.inactiveCol = inactiveColor
    self.text = text
    self.txtCol = txtColor
    self.txt_surface = font.render(text, True, txtColor, bgColor)
    self.active = False

  def handle_event(self):
    pass

  def draw(self, display):
      pygame.draw.rect(display, self.color, self.rect, 2)
      display.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

class ScreenChangeButton(Button):
  def __init__(self, x, y, w, h, mode, txtColor, inactiveColor, activeColor, text=''):
    super().__init__(x, y, w, h, txtColor, inactiveColor, activeColor, text)
    self.mode = mode

  def handle_event(self, event, display, mode):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        self.active = True
        return self.mode
      else:
        self.active = False
      self.color = self.activeCol if self.active else self.inactiveCol
      pygame.display.update()
    return mode

class InputButton(Button):
  def __init__(self, x, y, w, h, txtColor, inactiveColor, activeColor, text=''):
    super().__init__(x, y, w, h, txtColor, inactiveColor, activeColor, text)

  def handle_event(self, event, display, events):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        self.active = True
      else:
        self.active = False
      self.color = self.activeCol if self.active else self.inactiveCol
      pygame.display.update()
    if self.active:
      return [event.txtOutput() for event in events],True
    else:
      return "","",False

class BattleChoiceButton(Button):
  def __init__(self, x, y, w, h, text, txtColor, inactiveColor, activeColor, choice):
    super().__init__(x, y, w, h, txtColor, inactiveColor, activeColor, text)
    self.choice = choice

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        self.active = True
        return self.choice
      else:
        self.active = False
    return None

class InputBox():
  def __init__(self, x, y, w, h, txtColor, inactiveColor, activeColor, text='', front=0, back=20, name=""):
    self.name = name
    self.rect = pygame.Rect(x, y, w, h)
    self.color = inactiveColor
    self.inactiveCol = inactiveColor
    self.activeCol = activeColor
    self.txtCol = txtColor
    self.text = text
    self.previous_text = []
    self.next_text = []
    self.txt_surface = font.render(text, True, txtColor)
    self.active = False
    self.front = front
    self.back = back

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        self.active = True
      else:
        self.active = False
      self.color = self.activeCol if self.active else self.inactiveCol
    if event.type == pygame.KEYDOWN and self.active:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
        self.previous_text.append(self.text)
        self.text = self.text[:self.front]
      elif keys[pygame.K_LCTRL] and keys[pygame.K_z] and self.previous_text != []:
        self.next_text.append(self.text)
        self.text = self.previous_text.pop(-1)
      elif keys[pygame.K_LCTRL] and keys[pygame.K_y] and self.next_text != []:
        self.previous_text.append(self.text)
        self.text = self.next_text.pop(-1)
      elif event.key == pygame.K_RETURN:
        print(self.text)
      elif event.key == pygame.K_BACKSPACE and len(self.text) > self.front:
        self.previous_text.append(self.text)
        self.text = self.text[:-1]
      elif event.key != pygame.K_BACKSPACE and len(self.text) < self.back and re.fullmatch(pattern, event.unicode):
        self.previous_text.append(self.text)
        self.text += event.unicode
      self.txt_surface = font.render(self.text, True, self.txtCol)
      self.update()
    self.draw(display)
    return self.text

  def update(self):
    if len(self.text) > self.front and self.name == "EmailBox":
      width = max(200, font.render(self.text[self.front:], True, self.txtCol).get_width()+10)
    elif len(self.text) > self.front and self.name == "PwordBox":
      width = max(200, font.render(f"{'*'*len(self.text[self.front:])}", True, self.txtCol).get_width()+10)
    else:
      width = max(200, self.txt_surface.get_width()+10)
    self.rect.w = width

  def draw(self, display):
    pygame.draw.rect(display, self.color, self.rect, 2)
    if len(self.text) > self.front and self.name == "EmailBox":
      display.blit(font.render(self.text[self.front:], True, self.txtCol), (self.rect.x+5, self.rect.y+5))
    elif len(self.text) > self.front and self.name == "PwordBox":
      display.blit(font.render(f"{'*'*len(self.text[self.front:])}", True, self.txtCol), (self.rect.x+5, self.rect.y+5))
    elif self.name == "CodeBox":
      display.blit(font.render(f"{self.text}{'-'*(12-len(self.text))}", True, self.txtCol), (self.rect.x+5, self.rect.y+5))          
    else:
      display.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

  def txtOutput(self):
    return self.text[self.front:]

class Text():
  def __init__(self, text, pos, txtcol=black, bgcol=None, font=font):
    self.text = text
    self.txtcol = txtcol
    self.bgcol = bgcol
    self.txt_surf = font.render(text, True, txtcol, bgcol)
    size = self.txt_surf.get_size()
    self.pos = pos
    self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

  def draw(self, display):
    display.blit(self.txt_surf, self.rect)

  def handle_event(self, event, display):
    pass

  def get_width(self):
    return self.txt_surf.get_width()

  def get_height(self):
    return self.txt_surf.get_height()

  def get_size(self):
    return self.txt_surf.get_size()

  def update_text(self, text):
    self.text = text
    self.txt_surf = font.render(text, True, self.txtcol, self.bgcol)
    size = self.txt_surf.get_size()
    self.rect = pygame.Rect(self.pos[0], self.pos[1], size[0], size[1])

  def update_pos(self, pos):
    size = self.txt_surf.get_size()
    self.pos = pos
    self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

class AttackText(Text):
  def __init__(self, attack, pos, barb):
    super().__init__(attack.display_name, pos, bgcol=green)
    self.barb = barb
    self.attackIntName = attack.internal_name
    self.attackName = attack.display_name
    self.active = attack.internal_name in [x.internal_name for x in barb.active_attacks]
    self.tick = Image("Pictures/Equip Screen/tick mark.png", (0,0), True)
    self.tick.pos.center = (pos[0]+self.get_width(),pos[1])

  def draw(self, display):
    super().draw(display)
    if self.active: self.tick.draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        if self.barb.has_active_attack(self.attackIntName):
          if len(self.barb.active_attacks) == 1:
            return 9
          self.barb.forget_attack(self.attackIntName)
          self.active = False
          return 8
        elif self.barb.can_learn_attack():
          self.barb.learn_attack(self.attackIntName)
          self.active = True
          return 8
        else:
          return 10

class ActionText(Text):
  def __init__(self, text, pos, action):
    super().__init__(text, pos, bgcol=red)
    self.action = action

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        return self.action

class ShopAttackText(Text):
  def __init__(self, attack, pos, cost, barb):
    super().__init__(attack, pos, bgcol=green)
    self.barb = barb
    self.cost = cost
    self.return_value = 4
    self.obtainable = True
    self.obtained = False
    self.buyable = True

  def draw(self, display):
    super().draw(display)
    if self.obtained:
      sold = Image("Pictures/sold out.png", (self.rect.left,self.rect.top), True)
      sold.rect.center = self.rect.center
      sold.draw(display)
    if not self.obtainable:
      grey = Image("Pictures/cooldown image.png", (0,0), True)
      grey.rect.center = self.rect.center
      grey.draw(display)
      text = Text(f"{self.cost}",self.rect,red,font=strike_font)
    elif not self.buyable or self.obtained:
      text = Text(f"{self.cost}",self.rect,red)
    else:
      text = Text(f"{self.cost}",self.rect,(0,255,0))
    text.rect.left = self.rect.right + 10
    text.draw(display)

  def handle_event(self, event, display):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos) and self.obtainable and not self.obtained and self.buyable:
        return self.return_value

class DescText(Text):
  def __init__(self, text, pos, max_width):
    self.max_width = max_width
    super().__init__(text, pos)

  def get_height(self):
    words = [word.split(' ') for word in self.text.splitlines()]
    space = font.size(' ')[0]
    x = self.rect.left
    height = 0
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, self.txtcol, self.bgcol)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= self.max_width:
                x = self.rect.left
                height += word_height
            x += word_width + space
        x = self.rect.left
        height += word_height
    return height
    
  def draw(self, display):
    words = [word.split(' ') for word in self.text.splitlines()]
    space = font.size(' ')[0]
    x, y = self.rect.left, self.rect.top
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, self.txtcol, self.bgcol)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= self.max_width:
                x = self.rect.left
                y += word_height
            display.blit(word_surface, (x, y))
            x += word_width + space
        x = self.rect.left
        y += word_height

class Screen():
  def __init__(self, number, events):
    self.events = events
    self.number = number

  def handle_events(self, pgEvent, display, mode):
    outputs = []
    for event in self.events:
      objType = type(event)
      if objType == InputButton:
        outputs.append(event.handle_event(pgEvent,display,[events for events in self.events if type(events) == InputBox]))
      elif objType == ScreenChangeButton or objType == ScreenChangeImage:
        outputs.append(event.handle_event(pgEvent,display,mode))
      else:
        outputs.append(event.handle_event(pgEvent,display))
    return outputs

  def draw_events(self,display):
    for event in self.events:
      event.draw(display)
