import sys
import random
import pygame
from pygame.locals import *

from Player_data import *
from Screen_Objects import AttackText, Image, ScreenChangeImage, UpgradeTroopImage, ScreenChangeButton, InputButton, InputBox, Screen, UpgradeWeaponImage, WeaponImage, ShopWeaponImage, font, Text, UpgradeButtonImage, LootFarmImage, DiffImage, PowerImage, SettingsArrow, ActionText, ShopAttackText, DescText, red, green
from Weapon import get_weapon_stats, get_weapon_info
from Player import Player
from BattleLoader import get_battle_info, get_enemy_names
import Validator
import BattleEvents

pygame.init()

WINDOW_WIDTH = 512
WINDOW_HEIGHT = 384
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
home = ScreenChangeImage("Pictures/home icon.png", (478,350), -1, True)
back = ScreenChangeImage("Pictures/back icon.png", (442,350), -1, True)

#colours
darkGreen = (30, 125, 20)
blue = (0, 0, 128)
orange = pygame.Color("Orange")
black = pygame.Color("Black")
yellow = pygame.Color("Yellow")
pink = (255, 51, 153)
gold = (255, 215, 0)
white = pygame.Color("White")
purple = pygame.Color("Purple")

def blit_message(player,message="", color=black, speed="Normal",removeBox=True):
  if player is not None:
    col = player.settings['txt_box_col']
  else:
    col = "Blue"
  textBox = Image(f"Text Boxes/{col}.png", (0,WINDOW_HEIGHT-90), True)
  speeds = {
    "Slow"   : 90,
    "Normal" : 45,
    "Fast"   : 15,
    "Instant": 0
  }
  waitTime = speeds[speed]
  message = [word.split(' ') for word in message.splitlines()]
  space = font.size(' ')[0]
  boxWidth, boxHeight = textBox.get_size()
  boxWidth -= 40
  textBox.draw(display)
  pygame.display.update()
  pygame.time.delay(30)
  pos = (25, (WINDOW_HEIGHT - boxHeight + 15))
  x, y = pos
  row = 1
  for line in message:
    for word in line:
      text = ""
      wordSurface = font.render(word, 0, color)
      wordWidth, wordHeight = wordSurface.get_size()
      if x + wordWidth >= boxWidth:
        x, y, row = updateTextVariables(player,y,row,pos,wordHeight,textBox,removeBox)
      for letter in word:
        text += letter
        text_surface = font.render(text, True, blue)
        display.blit(text_surface, (x, y))
        pygame.display.update()
        pygame.time.delay(waitTime)
      x += wordWidth + space
    end = (word is message[-1][-1])
    if end and removeBox:
      waitForReturn(player)
      return
    x, y, row = updateTextVariables(player,y,row,pos,wordHeight,textBox,removeBox)

def display_message(player,message="", color=black,speed="Normal",removeBox=True):
  if player is not None:
    col = player.settings['txt_box_col']
  else:
    col = "Blue"
  textBox = Image(f"Text Boxes/{col}.png", (0,WINDOW_HEIGHT-90), True)
  speeds = {
    "Slow"   : 90,
    "Normal" : 45,
    "Fast"   : 15,
    "Instant": 0
  }
  waitTime = speeds[speed]
  message = [word.split(' ') for word in message.splitlines()]
  space = font.size(' ')[0]
  boxWidth, boxHeight = textBox.get_size()
  boxWidth -= 40
  textBox.draw(display)
  pygame.display.update()
  pygame.time.delay(30)
  pos = (25, (WINDOW_HEIGHT - boxHeight + 15))
  x, y = pos
  row = 1
  for line in message:
    for word in line:
      text = ""
      wordSurface = font.render(word, 0, color)
      wordWidth, wordHeight = wordSurface.get_size()
      if x + wordWidth >= boxWidth:
        x, y, row = updateTextVariables(player,y,row,pos,wordHeight,textBox,removeBox,False)
      for letter in word:
        text += letter
        text_surface = font.render(text, True, blue)
        display.blit(text_surface, (x, y))
        pygame.display.update()
        pygame.time.delay(waitTime)
      x += wordWidth + space
    end = (word is message[-1][-1])
    if end and removeBox:
      pygame.time.delay(waitTime+500)
      return
    x, y, row = updateTextVariables(player,y,row,pos,wordHeight,textBox,removeBox,False)

def refreshScreen(display,events=[]):
    for event in events:
      event.draw(display)
    pygame.display.update()

def updateTextVariables(player, y, row, pos,wordHeight,textBox,removeBox,wait=True):
  x = pos[0]
  y += wordHeight + 3
  row += 1
  if row > 2 and removeBox:
    if wait:
      waitForReturn(player)
    textBox.draw(display)
    y = pos[1]
    row -= 2
  return x, y, row

def close(player):
  if player is not None:
    update_player_table(player)
  pygame.quit()
  sys.exit()

def waitForReturn(player):
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      if (event.type == KEYDOWN and event.key == K_RETURN) or event.type == MOUSEBUTTONDOWN:
        return

def updateMode(mode,screens):
    return mode, screens[mode-1]

def title():
    loggedIn = False
    pygame.display.set_caption('Barbarian Rising')
    pygame.display.set_icon(pygame.image.load("./Graphics/icon.png"))
    titleScreen = Image("title.png", (0,0))
  
    toLoginButt = ScreenChangeButton(WINDOW_WIDTH-75,WINDOW_HEIGHT-32,75,32,1,blue,darkGreen,green,"Login")
    newAccBox = ScreenChangeButton(WINDOW_WIDTH-245,WINDOW_HEIGHT-32,245,32,2,blue,darkGreen,green,"Create New Account")
    resetPwordBox = ScreenChangeButton(0,WINDOW_HEIGHT-32,192,32,4,blue,darkGreen,green,"Reset Password")
    back_butt = ScreenChangeButton(0,WINDOW_HEIGHT-32,70,32,0,blue,darkGreen,green,"Back")
    yesButt = ScreenChangeButton((WINDOW_WIDTH-110),(WINDOW_HEIGHT-122),50,30,3,blue,darkGreen,green,"Yes")
    noButt = ScreenChangeButton((WINDOW_WIDTH-50),(WINDOW_HEIGHT-122),50,30,1,blue,darkGreen,green,"No")

    emailBox = InputBox(170,(WINDOW_HEIGHT/2)-50,200,32,blue,darkGreen,green,"Email: ",7,30,"EmailBox")
    pwordBox = InputBox(170,(WINDOW_HEIGHT/2)+20,200,32,blue,darkGreen,green,"Password: ",10,40,"PwordBox")
    codeBox = InputBox(170,(WINDOW_HEIGHT/2)-50,200,32,blue,darkGreen,green,"Code: ",6,12,"CodeBox")
  
    loginButt = InputButton(210,(WINDOW_HEIGHT-96),90,30,blue,darkGreen,green,"LOGIN")
    signUpButt = InputButton(200,(WINDOW_HEIGHT-96),110,30,blue,darkGreen,green,"SIGN UP")
    enterButt = InputButton(180,(WINDOW_HEIGHT-96),175,30,blue,darkGreen,green,"ENTER CODE")
    getCodeButt = InputButton(190,(WINDOW_HEIGHT-96),150,30,blue,darkGreen,green,"GET CODE")
    changePwordButt = InputButton(150,(WINDOW_HEIGHT-96),260,30,blue,darkGreen,green,"CHANGE PASSWORD")
  
    screen1 = Screen(1,[emailBox,pwordBox,loginButt,newAccBox,resetPwordBox])
    screen2 = Screen(2,[emailBox,pwordBox,signUpButt,toLoginButt])
    screen3 = Screen(3,[codeBox,enterButt,back_butt])
    screen4 = Screen(4,[emailBox,getCodeButt,back_butt])
    screen5 = Screen(5,[codeBox,pwordBox,changePwordButt,back_butt])
    screen6 = Screen(6,[yesButt,noButt])
    screens = [screen1,screen2,screen3,screen4,screen5,screen6]
    active_screen = screen1
    previousScreens = []
    mode = active_screen.number
  
    while not loggedIn:
      if mode != 6:
          refreshScreen(display,[titleScreen] + active_screen.events)
      for event in pygame.event.get():
          if event.type == QUIT:
            pygame.quit()
            sys.exit()
          elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
            outputs = active_screen.handle_events(event,display,mode)
            if mode == 1:
              if outputs[2][1] is True and Validator.valid_email(emailBox.txtOutput()) and len(pwordBox.txtOutput()) > 0:
                details = load_player_data(emailBox.txtOutput(),pwordBox.txtOutput())
                try:
                  player = Player(details[3]).load(details) # old player
                  return player
                except IndexError:
                  mode, active_screen = updateMode(6,screens)
                  refreshScreen(display,[titleScreen] + active_screen.events)
                  display_message(None,"No account found. Create a new account?",speed="Fast",removeBox=False)
                  loginButt.active = False
              elif outputs[2][1] and not Validator.valid_email(emailBox.txtOutput()):
                display_message(None,"Invalid email.",speed="Fast")
              elif outputs[-1] != mode:
                mode, active_screen = updateMode(outputs[-1],screens)
              elif outputs[-2] != mode:
                mode, active_screen = updateMode(outputs[-2],screens)
            elif mode == 2:
              if outputs[2][1]:
                if get_acc_with_email(emailBox.txtOutput()) is not None:
                  display_message(None,"Email already in use.",speed="Fast")
                else:
                  previousScreens.append(mode)
                  code,mode,active_screen = sendVerificationCode(emailBox.txtOutput(),screens,mode)
              elif outputs[-1] != mode:
                mode, active_screen = updateMode(outputs[-1],screens)
            elif mode == 3:
              if enterButt.active and codeBox.txtOutput().isdigit() and int(codeBox.txtOutput()) == code:
                player = Player("")
                player.id = get_new_id()
                update_player_table(player,emailBox.txtOutput(),pwordBox.txtOutput())
                return player
              elif outputs[-1] != mode:
                mode, active_screen = updateMode(previousScreens.pop(),screens)
            elif mode == 4:
              if getCodeButt.active:
                if get_acc_with_email(emailBox.txtOutput()) is None:
                  display_message(None,"No account found with that email.",speed="Fast")
                else:
                  code,mode,active_screen = sendVerificationCode(emailBox.txtOutput(),screens,mode,5)
              elif back_butt.active:
                mode, active_screen = updateMode(1,screens)
            elif mode == 5:
              if changePwordButt.active and codeBox.txtOutput().isdigit() and int(codeBox.txtOutput()) == code and len(pwordBox.txtOutput()) > 0:
                update_player_password(emailBox.txtOutput(),pwordBox.txtOutput())
                display_message(None,"Password successfully changed.",speed="Fast")
                mode, active_screen = updateMode(1,screens)
              if back_butt.active:
                mode, active_screen = updateMode(1,screens)
            elif mode == 6:
              if yesButt.active:
                mode, active_screen = updateMode(2,screens)
              elif noButt.active:
                mode, active_screen = updateMode(1,screens)
      clock.tick(60)

def intro1(player):
    display.fill(black)
    display_message(player,"You survived?")
    display_message(player,"You really are stubborn, huh?")
    display_message(player,"Guess I'll let you off for now, no point in killing you when you're so weak...")
    display.fill(black)
    pygame.display.update()
    pygame.time.delay(1200)
    display_message(player,"Hey, wake up! Goblins are about to attack us!")
    display.fill(green)

def intro2(player):
    villager = Image("villager.png", (0,50), True)
    nameBox = InputBox(170,(WINDOW_HEIGHT/2)-50,192,32,blue,darkGreen,green,"Name: ",6,30,"EmailBox")
    enterButt = InputButton(210,(WINDOW_HEIGHT-96),90,30,blue,darkGreen,green,"Enter")
    nameSet = False
  
    bg = Image("Backgrounds/barb screen.png", (0,0))
    bg.draw(display)
    villager.draw(display)
    pygame.display.update()
    display_message(player,"Oooh... you're strong.")
    display_message(player,"What's your name?")
    nameBox.draw(display)
  
    screen1 = Screen(1,[bg, nameBox, enterButt])
    active_screen = screen1
    pygame.display.update()

    while not nameSet:        
      for event in pygame.event.get():
          if event.type == QUIT:
            pygame.quit()
            sys.exit()
          elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
            active_screen.handle_events(event, display, 1)
            if active_screen == screen1:
              if event.type == KEYDOWN and event.key == K_RETURN or enterButt.active:
                player.name = nameBox.txtOutput()
                bg.draw(display)
                active_screen.draw_events(display)
                pygame.display.update()
                nameSet = True
            active_screen.draw_events(display)
            pygame.display.update()
                
    bg.draw(display)
    display_message(player, f"Nice to meet you, {player.name}! I'll be helping you out from now on.")
    return player
  
def mainScreen(player):
  grass = Image("Backgrounds/Classic Scenery v3.png", (0,0))
  town_hall = Image(f"Town Halls/{player.th}.png", (WINDOW_WIDTH/3,WINDOW_HEIGHT/3), True)
  town_hall.pos.center = (256,212)

  refreshed = player.should_refresh_stamina()
  name = Text(f"{player.name}, Town Hall {player.th}", (2,2), orange, blue)
  stamina_text = Text(f"Stamina: {player.stamina}/240", (0,0), black, red)
  stamina_text.rect.topleft = (WINDOW_WIDTH-(stamina_text.get_width() + 2),4)
  gold_text = Text(f"Gold: {player.gold}/{player.max_gold}", (0,0), black, gold)
  gold_text.rect.topleft = (WINDOW_WIDTH-(gold_text.get_width() + 2),34)
  elixir_text = Text(f"Elixir: {player.elixir}/{player.max_elixir}", (0,0), black, pink)
  elixir_text.rect.topleft = (WINDOW_WIDTH-(elixir_text.get_width() + 2),64)

  weapon_text = None
  de_text = None
  if player.th >= 2:
    weapon_text = Text(f"Weapon Ore: {player.weapon_ore}/{player.max_weapon_ore}", (0,0), white, orange) 
    weapon_text.rect.topleft = (WINDOW_WIDTH-(weapon_text.get_width() + 2),94)
  if player.th >= 4:
    de_text = Text(f"Dark Elixir: {player.d_elixir}/{player.max_d_elixir}", (0,0), white, black) 
    de_text.rect.topleft = (WINDOW_WIDTH-(de_text.get_width() + 2),124)

  settings = ScreenChangeImage("Pictures/settings icon.png", (5,35), 1, True)
  loot = ScreenChangeButton(2,350,font.render("Loot",True,black).get_width()+10,32,1,black,darkGreen,green,"Loot")
  font_width = font.render("Village Upgrade",True,black).get_width()+10
  barbSettings  = ScreenChangeImage(f"Troops/Icons/{player.barb.internal_name}.png", (5,90), 1, True)
  upgrade = ScreenChangeImage("Pictures/Buttons/upgrade menu button.png", (5,155), 1, True)
  weapUpgrade = ScreenChangeImage("Pictures/Buttons/weapons button.png", (5,205), 1, True)
  font_width = font.render("Shop",True,black).get_width()+10
  shop = ScreenChangeButton(510-font_width,350,font_width,32,1,black,darkGreen,green,"Shop")
  boss = ScreenChangeImage("Pictures/Buttons/boss screen arrow.png", (392,190), 1, True)
  
  main_screen = Screen(0, [
    grass, town_hall, settings, barbSettings,
    upgrade, weapUpgrade, loot, shop, boss, 
    name, stamina_text, gold_text, elixir_text
  ])
  if weapon_text is not None:
    main_screen.events.append(weapon_text)
  if de_text is not None:
    main_screen.events.append(de_text)
  refreshScreen(display,main_screen.events)
  if refreshed:
    display_message(player, "You have recieved your stamina for today.")
    refreshScreen(display,main_screen.events)

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN:
        mode = main_screen.handle_events(event,display,0)
        if mode[2] != 0:
          return 1
        elif mode[3] != 0:
          return 2
        elif mode[4] != 0:
          return 3
        elif mode[5] != 0:
          return 4
        elif mode[6] != 0:
          return 5
        elif mode[7] != 0:
          return 6
        elif mode[8] != 0:
          return 7
    pygame.display.update()
    clock.tick(60)

def settingsScreen(player):
  bg = Image("Backgrounds/settings board.png", (0,0))
  speedTxt = Text(" Text Speed ", (100,85), bgcol=green)
  leftArrow1 = SettingsArrow("Pictures/left arrow.png", (271,85), -1)
  rightArrow1 = SettingsArrow("Pictures/right arrow.png", (418,85), 1)
  leftArrow2 = SettingsArrow("Pictures/left arrow.png", (271,128), -1)
  rightArrow2 = SettingsArrow("Pictures/right arrow.png", (418,128), 1)
  
  speedOptions = ["Slow","Normal","Fast","Instant"]
  currentSpeedTxt = Text(f" {player.settings['txt_speed']} ", (280,85), bgcol=green)
  currentSpeedTxt.update_pos((359-(currentSpeedTxt.get_width()//2), 85))
  currentSpeed = speedOptions.index(player.settings['txt_speed'])
  
  textColTxt = Text("Text Box Colour", (73,128), bgcol=green)
  colOptions = ["Blue","Green","Orange","Purple","Red", "Gold","Silver","Steel","Brick"]
  currentColTxt = Text(f" {player.settings['txt_box_col']} ", (280,125), bgcol=green)
  currentColTxt.update_pos((359-(currentColTxt.get_width()//2), 128))
  currentCol = colOptions.index(player.settings['txt_box_col'])
  
  textBox = Image(f"Text Boxes/{player.settings['txt_box_col']}.png",(0,WINDOW_HEIGHT-90), True)
  reset = ActionText("Reset Save", (295,207), "Reset")
  delete = ActionText("Delete Account", (265,247), "Delete")
  back = ScreenChangeImage("Pictures/back icon.png", (448,265), -1, True)
  screen = Screen(0, [bg, speedTxt, leftArrow1, currentSpeedTxt, 
                      rightArrow1, textColTxt, leftArrow2, 
                      currentColTxt, rightArrow2, textBox, 
                      reset, delete, back])
  screen.draw_events(display)
  pygame.display.update()
  
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
        mode = screen.handle_events(event,display,0)
        if mode[-1] == -1:
          player.settings['txt_speed'] = screen.events[3].text[1:-1]
          player.settings['txt_box_col'] = screen.events[7].text[1:-1]
          return 0
        elif "Reset" in mode:
          return 8
        elif "Delete" in mode:
          return 9
        elif mode[2] == -1:
          currentSpeed -= 1
          if currentSpeed < 0: currentSpeed = len(speedOptions)-1
        elif mode[4] == 1:
          currentSpeed += 1
          if currentSpeed >= len(speedOptions): currentSpeed = 0
        elif mode[6] == -1:
          currentCol -= 1
          if currentCol < 0: currentCol = len(colOptions)-1
        elif mode[8] == 1:
          currentCol += 1
          if currentCol >= len(colOptions): currentCol = 0
            
        currentSpeedTxt.update_text(f" {speedOptions[currentSpeed]} ")
        currentSpeedTxt.update_pos((359-(currentSpeedTxt.get_width()//2),85))
        currentColTxt.update_text(f" {colOptions[currentCol]} ")
        currentColTxt.update_pos((359-(currentColTxt.get_width()//2), 128))
        screen.events[9] = Image(f"Text Boxes/{colOptions[currentCol]}.png", (0,WINDOW_HEIGHT-90), True)
        screen.draw_events(display)
        pygame.display.update()

def lootFarmSelectionScreen(player):
  gold = LootFarmImage("Pictures/Loot Icons/Gold icon.png", (96,32), "GOLD", True)
  elixir = LootFarmImage("Pictures/Loot Icons/Elixir icon.png", (266,32), "ELIXIR", True)
  d_elixir = LootFarmImage("Pictures/Loot Icons/Dark Elixir icon.png", (266,192), "DARKELIXIR", True)
  weapon = LootFarmImage("Pictures/Loot Icons/Weapon Ore.png", (96,192), "ORE", True)
  lootTxt = Text(" Resources ", (2,2), bgcol=green)
  difftxt = Text(" Difficulty ", (2,2), bgcol=green)
  text = f"Stamina: {player.stamina}/240"
  stamina_text = Text(text, (WINDOW_WIDTH-(font.render(text,True,red).get_width() + 2),4), bgcol=red)
  starttxt = Text("Start!", (225,350), bgcol=green)
  starttxt = ScreenChangeButton(220,345,starttxt.get_width()+10,starttxt.get_height()+10,4,red,darkGreen,green,"Start!")
  mult = 1
  multtxt = Text(f"Multiplier: X{mult}", (8,300))
  mult1 = DiffImage("Pictures/Buttons/x1 mult.png",(4, 328),1,3)
  mult2 = DiffImage("Pictures/Buttons/x2 mult.png",(53, 328),2,3)
  mult3 = DiffImage("Pictures/Buttons/x3 mult.png",(102, 328),3,3)
  mult4 = DiffImage("Pictures/Buttons/x4 mult.png",(151, 328),4,3)
  stamtxt = Text("", (8,250))
  reward_txt = Text("", (8,70))
  stamina = 0
  reward = 0
  enemy_images = []
  
  lootScreen = Screen(0, [gold, elixir, d_elixir, weapon, lootTxt, reward_txt, stamina_text, home])
  active_screen = lootScreen

  loot_type = None
  diff = 0
  display.fill(purple)
  active_screen.draw_events(display)
  pygame.display.update()
  
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
        mode = active_screen.handle_events(event,display,0)
        if mode[-1] == -1:
          return 0
        elif mode[-2] == -1:
          text = f"Stamina: {player.stamina}/240"
          lootScreen.events[5] = Text(text, (WINDOW_WIDTH-(font.render(text,True,red).get_width() + 2),4), bgcol=red)
          stamtxt.update_text("")
          if enemy_images != []:
            removeEventsFromScreen(active_screen, enemy_images)
          active_screen = lootScreen
        elif 1 in mode:
          events = []
          loot_index = mode.index(1)
          loot_type = active_screen.events[loot_index].type
          if loot_type == "ORE" and player.th < 2:
            display_message(player, "You can start farming Weapon Ore at Town Hall 2.")
          elif loot_type == "DARKELIXIR" and player.th < 4:
            display_message(player, "You can start farming Dark Elixir at Town Hall 4.")
          else:
            left = 16
            diffs = player.difficulties_unlocked[loot_type]
            if diffs > 6:
              diffs = 6
            for i in range(diffs):
              events.append(DiffImage(f"Pictures/Buttons/diff circle {i+1}.png", (left,154), i+1, 2))
              left += 80
            diffScreen = Screen(1, events + [difftxt, starttxt, stamtxt, stamina_text, back, home])
            active_screen = diffScreen
        elif 2 in mode:
          if multtxt is not None:
            multtxt.update_text("Multiplier: X1")
          diff_event = active_screen.events[mode.index(2)]
          diff = diff_event.diff
          info = get_battle_info(f"{loot_type}BATTLE{diff}")
          stamina = int(info[0])
          stamtxt.update_text(f'Required Stamina: {stamina}')
          if stamtxt not in active_screen.events:
            active_screen.events.insert(-3, stamtxt)
          reward = int(info[1])
          reward_txt.update_text(f'Base Reward: {reward}')
          reward_type = Image(f"Pictures/Loot Icons/{loot_type}.png", (170, 92), True)
          if reward_txt not in active_screen.events:
            active_screen.events.insert(-3, reward_txt)
          active_screen.events.insert(-3, reward_type)
          if player.difficulties_unlocked[loot_type] > diff:
            if multtxt not in active_screen.events:
              active_screen.events.insert(1, multtxt)
              addEventsToScreen(active_screen,-3,[mult1,mult2,mult3,mult4])
          elif player.difficulties_unlocked[loot_type] <= diff:
            if multtxt in active_screen.events:
              removeEventsFromScreen(active_screen,[multtxt,mult1,mult2,mult3,mult4])
              mult = 1
          update_diffs(active_screen, diff_event)
          battle_id = f"{loot_type}BATTLE{diff}"
          enemy_images = add_enemies(active_screen, enemy_images, battle_id)
        elif 3 in mode:
          mult_event = active_screen.events[mode.index(3)]
          mult = mult_event.diff
          active_screen.events.remove(multtxt)
          multtxt = Text(f"Multiplier: X{mult}", (8,300))
          active_screen.events.insert(1, multtxt)
          stamtxt.update_text(f"Required Stamina: {stamina*mult}")
          reward_txt.update_text(f'Base Reward: {reward*mult}')
        elif 4 in mode:
          if loot_type is not None and diff > 0:
            BattleEvents.loot_battle(player,loot_type,diff,mult)
            events = []
            left = 16
            for i in range(player.difficulties_unlocked[loot_type]):
              events.append(DiffImage(f"Pictures/Buttons/diff circle {i+1}.png", (left,154), i+1, 2))
              left += 80
            text = f"Stamina: {player.stamina}/240"
            lootScreen.events.remove(stamina_text)
            stamina_text = Text(text, (WINDOW_WIDTH-(font.render(text,True,red).get_width() + 2),4), bgcol=red)
            diffScreen = Screen(1, events + [difftxt, starttxt, stamina_text, back, home])
            lootScreen.events.insert(-1, stamina_text)
            active_screen = diffScreen
        display.fill(purple)
        active_screen.draw_events(display)
        pygame.display.update()

def troopUpgScreen(player):
  display.fill(purple)
  bg = Image("Pictures/troop upgrade.png", (0,0))
  barb = UpgradeTroopImage(f"Troops/Icons/Upgrade {player.barb.internal_name}.png", (25,228), player.barb, player, barb=True)
  th_warn = Text("Town Hall level too low!", (20,182), bgcol=red)
  loot_warn = Text("Not enough loot!", (20,182), bgcol=red)
  max_warn = Text("Already at max level!", (20,182), bgcol=green)
  upgradeButton = None
  events = [bg, home, barb]
  left = 160
  tops = [224,289]
  powers = get_powers()
  if player.unlocked_power("ARCHERQUEEN"):
    powers[0] = "ARCHERQUEEN"
  elif player.unlocked_power("SUPERARCHER"):
    powers[0] = "SUPERARCHER"
  if player.unlocked_power("SUPERWALLBREAKER"):
    powers[1] = "SUPERWALLBREAKER"
  if player.unlocked_power("SUPERWIZARD"):
    powers[2] = "SUPERWIZARD"
  if player.unlocked_power("SUPERMINER"):
    powers[5] = "SUPERMINER"
  for i,power in enumerate(powers):
    events.append(UpgradeTroopImage(f"Troops/Icons/{power}.png", (left,tops[i%2]), player.get_unlocked_power(power), player))
    if i%2 == 1:
      left += 64
  
  screen = Screen(0, events)
  screen.draw_events(display)
  pygame.display.update()
  
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
        mode = screen.handle_events(event,display,0)
        if mode[1] != 0:
          return 0
        if upgradeButton is not None and upgradeButton.active and upgradeButton.mode == "evolve":
          oldName = upgradeButton.troop.display_name
          oldIntName = upgradeButton.troop.internal_name
          newTroop = upgradeButton.troop.evolve(player)
          newName = newTroop.display_name
          if "BARBARIAN" in upgradeButton.troop.internal_name:
            player.barb = newTroop
          else:
            unlocked = player.get_unlocked_power_index(oldIntName)
            if unlocked is not None:
              player.unlocked_powers[unlocked] = newTroop
            active = player.get_active_power_index(oldIntName)
            if active is not None:
              player.active_powers[active] = newTroop
          display_message(player,f"{oldName} evolved into {newName}!")
          return 0
        if 1 in mode:
          eventidx = mode.index(1)
          if eventidx != len(events)-1:
            troop = events[eventidx]
          removeEventsFromScreen(screen,[max_warn,th_warn,loot_warn])
          if upgradeButton in events:
            events.remove(upgradeButton)
          upgradeButton = UpgradeButtonImage("Pictures/Buttons/upgrade button.png", (356,182), player, troop.troop)
          events.append(upgradeButton)
        elif 2 in mode:
          eventidx = mode.index(2)
          if eventidx != len(events)-1:
            troop = events[eventidx]
          removeEventsFromScreen(screen,[upgradeButton,loot_warn,max_warn])
          if th_warn not in events: events.append(th_warn)
        elif 3 in mode:
          eventidx = mode.index(3)
          if eventidx != len(events)-1:
            troop = events[eventidx]
          elif eventidx == len(events)-1:
            events.pop()
          removeEventsFromScreen(screen,[upgradeButton,th_warn,max_warn])
          if loot_warn not in events: events.append(loot_warn)
        elif 4 in mode:
          eventidx = mode.index(4)
          if eventidx != len(events)-1:
            troop = events[eventidx]
          elif eventidx == len(events)-1 and type(eventidx) == UpgradeButtonImage:
            events.pop()
          removeEventsFromScreen(screen,[upgradeButton,th_warn,loot_warn])
          if max_warn not in events: events.append(max_warn)
        elif 5 in mode:
          eventidx = mode.index(5)
          if eventidx != len(events)-1:
            troop = events[eventidx]
          removeEventsFromScreen(screen,[max_warn,th_warn,loot_warn])
          if upgradeButton in events:
            events.remove(upgradeButton)
          upgradeButton = UpgradeButtonImage("Pictures/Buttons/evolve button.png", (356,182), player, troop.troop, mode="evolve")
          events.append(upgradeButton)
        if 1 in mode or 2 in mode or 3 in mode or 4 in mode or 5 in mode:
          screen.draw_events(display)
          Image("Pictures/stat box bg.png", (20, 20), True).draw(display)
          if 4 in mode or 5 in mode:
            pass
          elif troop.troop is player.barb:
            troop.drawBarbStats(display)
          else:
            troop.drawPowerStats(display)
        pygame.display.update()

def addEventsToScreen(screen, position, events):
  for event in events:
    screen.events.insert(position, event)

def removeEventsFromScreen(screen,events):
  for event in events:
    if event in screen.events:
      screen.events.remove(event)

def removeEventTypeFromScreen(screen, event_type):
  for event in screen.events:
    screen.events = [x for x in screen.events if type(x) != event_type]

def weaponUpgScreen(player):
  display.fill(purple)
  swords = ScreenChangeImage("Weapons/Swords2.png",(0,87),1)
  shields = ScreenChangeImage("Weapons/Shields1.png",(0,116),2)  
  sword_screen = Screen(1,[swords,shields,home])
  swords = ScreenChangeImage("Weapons/Swords1.png",(0,87),1)
  shields = ScreenChangeImage("Weapons/Shields2.png",(0,116),2)
  th_warn = Text("Town Hall level too low!", (15,340), bgcol=red)
  loot_warn = Text("Not enough loot!", (15,340), bgcol=red)
  max_warn = Text("Already at max level!", (15,340), bgcol=green)
  shield_screen = Screen(2,[swords,shields,home])
  addWeaponsToScreen(player, "Swords", sword_screen)
  addWeaponsToScreen(player, "Shields", shield_screen)
  
  weapon_screen = None
  previous_screen = None
  upgradeImage = None
  active_screen = sword_screen
  active_screen.draw_events(display)
  pygame.display.update()
  
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
        mode = active_screen.handle_events(event,display,0)
        if mode[-1] != 0:
          return 0
        elif mode[-2] == -1:
          active_screen = previous_screen
        elif 1 in mode:
          active_screen = sword_screen
        elif 2 in mode:
          active_screen = shield_screen
        elif 4 in mode:
          if upgradeImage in active_screen.events:
            active_screen.events.remove(upgradeImage)
          active_screen.events.insert(-2,th_warn)
        elif 5 in mode:
          if upgradeImage in active_screen.events:
            active_screen.events.remove(upgradeImage)
          active_screen.events.insert(-2,loot_warn)
        elif 6 in mode:
          previous_screen = active_screen
          weapon = active_screen.events[mode.index(6)]
          currentWeapon = Image(weapon.name,(20,140),True)
          upgradeable = weapon.weapon.can_upgrade(player)
          if upgradeable == 3:
            upgradeImage = UpgradeButtonImage("Pictures/Buttons/upgrade button.png", (370,300), player, weapon.weapon)
            events = [currentWeapon,upgradeImage,back,home]
          elif upgradeable == 4:
            events = [currentWeapon,th_warn,back,home]
          elif upgradeable == 5:
            events = [currentWeapon,loot_warn,back,home]
          elif upgradeable == 6:
            events = [currentWeapon,max_warn,back,home]
          boxes = len(weapon.weapon.stats.keys())+1
          top = 20
          for i in range(boxes):
            stat_box = Image("Weapons/Weapon Stat Box.png", (120,top),True)
            events.insert(-2,stat_box)
            if not weapon.weapon.max_level():
              stat_box = Image("Weapons/Weapon Stat Box.png", (120,top+160),True)
              events.insert(-2,stat_box)
            top += 28
          weapon_screen = Screen(3,events)
          active_screen = weapon_screen
          
        display.fill(purple)
        active_screen.draw_events(display)
        if active_screen == weapon_screen and weapon_screen is not None:
          drawWeaponScreenStats(weapon.weapon.level, weapon, display, 124, 24)
          if not weapon.weapon.max_level():
            drawWeaponScreenStats(weapon.weapon.level+1, weapon, display, 124, 184)
        pygame.display.update()

def addWeaponsToScreen(player, weapon_type, screen, left=160,top=40):
  if weapon_type == "Shields":
    weapons = player.shields
  else:
    weapons = player.swords
  for i,weapon in enumerate(weapons):
    screen.events.insert(-1,UpgradeWeaponImage(weapon, (left,top)))
    if (i+1)%4 == 3:
      left = 160
      top += 80
    else:
      left += 80

def drawWeaponScreenStats(level, weapon, display, left, top):
  stat_convert = {
    "attack": "Attack",
    "defence": "Defence",
    "damage_mult": "Damage Mult",
    "damage_reduction": "Damage Reduction",
    "crit_rate": "Crit Rate"
  }
  Text(f"Lv. {level} {weapon.weapon.display_name}", (left, top)).draw(display)
  statNames = list(weapon.weapon.stats.keys())
  stats = get_weapon_stats(weapon.weaponName, level)[2].split(":")
  for i,stat in enumerate(stats):
    top += 28
    Text(f"{stat_convert[statNames[i]]}: {stat}%", (left, top)).draw(display)
  if weapon.weapon.max_level():
    return
  costs = get_weapon_stats(weapon.weaponName, weapon.weapon.level+1)[1].split(":")
  gold = Image("Pictures/Loot Icons/GOLD.png", (122, 141), True)
  ore = Image("Pictures/Loot Icons/ORE.png", (255, 141), True)
  gold.draw(display)
  ore.draw(display)
  Text(str(costs[0]), (160, 144)).draw(display)
  Text(str(costs[1]), (290, 144)).draw(display)

def make_shop_weapon_screen(num, events, weapon_type, player, left=180, top=40):
  weapons = get_weapons(weapon_type)
  for i, weapon in enumerate(weapons):
    image = ShopWeaponImage(weapon, (left, top))
    image.cost = int(get_weapon_stats(weapon, 1)[1].split(":")[1])
    if weapon_type == "sword":
      image.return_value = 5
    else:
      image.return_value = 6
    obtained = False
    if "SWORD" in weapon:
      obtained = player.has_sword(weapon)
    elif "SHIELD" in weapon:
      obtained = player.has_shield(weapon)
    if obtained:
      image.obtained = True
    if player.th < get_weapon_info(weapon)[5]:
      image.obtainable = False
    elif player.weapon_ore < image.cost:
      image.buyable = False
    events.insert(-1, image)
    if i % 3 == 2:
      left = 180
      top += 120
    else:
      left += 90
  return Screen(2, events)

def make_shop_attack_screen(num, events, player, left=180, top=40):
  pass

def shopScreen(player):
  bg = Image("Backgrounds/barb screen.png", (0,0))
  gold_text = Text(f"Gold: {player.gold}/{player.max_gold}", (0,0), black, yellow)
  gold_text.rect.left = WINDOW_WIDTH-(gold_text.get_width() + 5)
  weapon_text = Text(f"Weapon Ore: {player.weapon_ore}/{player.max_weapon_ore}", (0,0), white, orange)
  weapon_text.rect.left = WINDOW_WIDTH-(weapon_text.get_width() + 2)
  attacks = {
    "QUICKSLASH": ["Quick Slash", 4, 1000],
    "UPPERSLASH": ["Upper Slash", 7, 5000],
    "BURNSLASH": ["Burn Slash", 9, 10000],
    "DARKSLASH": ["Dark Slash", 9, 10000],
    "FROSTSLASH": ["Frost Slash", 12, 12500],
    "THUNDERSLASH": ["Thunder Slash", 12, 12500],
    "SACREDSLASH": ["Sacred Slash", 12, 12500],
    "WINDSLASH": ["Wind Slash", 12, 12500]
  }
  attacks1 = ScreenChangeImage("Pictures/Equip Screen/Attacks1.png",(0,60),1)
  attacks2 = ScreenChangeImage("Pictures/Equip Screen/Attacks2.png",(0,60),1)
  sword1 = ScreenChangeImage("Weapons/Swords1.png",(0,90),2)
  sword2 = ScreenChangeImage("Weapons/Swords2.png",(0,90),2)
  shield1 = ScreenChangeImage("Weapons/Shields1.png",(0,120),3)
  shield2 = ScreenChangeImage("Weapons/Shields2.png",(0,120),3)
  attack_screen = Screen(1, [bg, gold_text, attacks2, sword1, shield1, home])
  top = 40
  for key, attack in attacks.items():
    text = ShopAttackText(attack[0], (180, top), attack[2], player.barb)
    if player.barb.has_attack(key):
      text.obtained = True
    elif player.th < attack[1]:
      text.obtainable = False
    elif player.gold < attack[2]:
      text.buyable = False
    attack_screen.events.insert(-1, text)
    top += 30
  active_screen = attack_screen
  active_screen.draw_events(display)
  pygame.display.update()
  
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
        mode = active_screen.handle_events(event,display,0)
        if mode[-1] != 0:
          return 0
        elif 1 in mode:
          active_screen = attack_screen
        elif 2 in mode:
          sword_screen = make_shop_weapon_screen(2, [bg, attacks1, weapon_text, sword2, shield1, home], "sword", player)
          active_screen = sword_screen
        elif 3 in mode:
          shield_screen = make_shop_weapon_screen(3, [bg, attacks1, weapon_text, sword1, shield2, home], "shield", player)
          active_screen = shield_screen
        elif 4 in mode:
          attack_index = mode.index(4)
          attack = active_screen.events[attack_index]
          attack_int = attack.text.replace(" ", "").upper()
          player.gold -= attack.cost
          gold_text.update_text(f"Gold: {player.gold}/{player.max_gold}")
          player.barb.unlock_attack(attack_int)
          gold_text.rect.left = WINDOW_WIDTH-(gold_text.get_width() + 5)
          display_message(player, f"{player.barb.display_name} can now use {attack.text}!")
          attack.obtained = True
        elif 5 in mode:
          weapon_index = mode.index(5)
          event = active_screen.events[weapon_index]
          player.obtain_weapon(event.weapon, 1)
        elif 6 in mode:
          weapon_index = mode.index(6)
          event = active_screen.events[weapon_index]
          player.obtain_weapon(event.weapon, 1)
        if 5 in mode or 6 in mode:
          player.weapon_ore -= event.cost
          weapon_text.update_text(f"Weapon Ore: {player.weapon_ore}/{player.max_weapon_ore}")
          weapon_text.update_pos((WINDOW_WIDTH-(weapon_text.get_width() + 2),0))
          active_screen.events[2] = weapon_text
          event.obtained = True
          event.buyable = False
        active_screen.draw_events(display)
        pygame.display.update()

def bossScreen(player):
  display.fill(purple)
  starttxt = Text("Start!", (225,350), bgcol=green)
  starttxt = ScreenChangeButton(220,345,starttxt.get_width()+10,starttxt.get_height()+10,3,red,darkGreen,green,"Start!")
  th_image = None
  enemy_images = []
  th_events = [home]
  diff_events = [starttxt, back, home]
  diff = 0

  row = 1
  left = 2
  gap = 2
  for i in range(2,16):
    image = ScreenChangeImage(f"Town Halls/{i}.png",(left,0),1,True)
    size = image.get_size()
    image.pos.bottom = 128*row-2
    th_events.insert(0, image)
    if i == 6:
      row += 1
      left = 1
      gap = 0
    elif i == 11:
      row += 1
      left = 5
      gap = 5
    else:
      left += size[0]+gap

  for i in range(3):
    diff_events.insert(0, DiffImage(f"Pictures/Buttons/diff circle {i+1}.png", (20, 80*i+20), i+1, 2))
      
  th_screen = Screen(1, th_events)
  diff_screen = Screen(2, diff_events)
  active_screen = th_screen
  active_screen.draw_events(display)
  pygame.display.update()
  
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
        mode = active_screen.handle_events(event,display,0)
        if mode[-1] != 0:
          return 0
        elif mode[-2] == -1:
          active_screen = th_screen
        elif 1 in mode:
          th_event = th_screen.events[mode.index(1)]
          if enemy_images != []:
            removeEventsFromScreen(diff_screen, enemy_images)
          if th_image in diff_screen.events:
            diff_screen.events.remove(th_image)
          th_image = Image(th_event.name, (0, 200), True)
          th_image.pos.centerx = 256
          diff_screen.events.insert(-3, th_image)
          th = th_event.name[11:-4]
          for event in diff_screen.events:
            if type(event) == DiffImage:
              event.selected = False
          active_screen = diff_screen
        elif 2 in mode:
          diff_event = active_screen.events[mode.index(2)]
          diff = diff_event.diff
          if player.difficulties_unlocked[f"TH{th}"] < diff:
            display_message(player, "Clear the previous difficulty to unlock this one.")
            diff_event.selected = False
          else:
            if int(th) >= 12:
              diff_screen.events.remove(th_image)
              th_image = Image(f"{th_event.name[:-4]}.{diff*2-1}.png", (0, 200), True)
              th_image.pos.centerx = 256
              diff_screen.events.insert(-3, th_image)       
            update_diffs(active_screen, diff_event)
            battle_id = f"TH{th}BATTLE{diff}"
            enemy_images = add_enemies(active_screen, enemy_images, battle_id)
        elif 3 in mode and diff > 0:
          battle = getattr(BattleEvents,f"TH{th}_Battle")
          result = battle(player, diff)
          if result == 1 and player.difficulties_unlocked[f"TH{th}"] < 4:
            player.difficulties_unlocked[f"TH{th}"] = diff + 1
          return 0
        display.fill(purple)
        active_screen.draw_events(display)
        pygame.display.update()

def update_diffs(screen, diff_event):
  if diff_event.selected:
    for event in screen.events:
      if type(event) == DiffImage:
        event.selected = False
    diff_event.selected = True

def add_enemies(screen, enemy_images, battle_id, left=296, top=30):
  enemy_text = Text("Enemies:", (296, 30))
  enemy_text.rect.right = 290
  if enemy_images != []:
    removeEventsFromScreen(screen, enemy_images)
  waves, levels = get_enemy_names(battle_id)
  enemy_images = [enemy_text]
  og_left = left
  for i,names in enumerate(waves):
    for j,name in enumerate(names):
      enemy_images.append(Image(f"Troops/Icons/{name}.png", (left, top), True))
      enemy_images.append(Text(f"{levels[i][j]}", (left, top), True))
      left += 70
    left = og_left
    top += 70
  addEventsToScreen(screen, -3, enemy_images)
  return enemy_images

def barbScreen(player):
  bg = Image("Backgrounds/barb screen.png", (0,0))
  barb = Image(f"Pictures/equip {player.barb.internal_name}.png", (0,0), True)
  barb.pos.bottomleft = (150,336)
  upgrade = ScreenChangeImage("Pictures/Equip Screen/Upgrade.png",(0,0),6)
  overview = ScreenChangeImage("Pictures/Equip Screen/Overview2.png",(0,50),1)
  swords = ScreenChangeImage("Weapons/Swords1.png",(0,79),2)
  shields = ScreenChangeImage("Weapons/Shields1.png",(0,108),3)
  attacks = ScreenChangeImage("Pictures/Equip Screen/Attacks1.png",(0,137),4)
  powers = ScreenChangeImage("Pictures/Equip Screen/Powers1.png",(0,166),5)
  weapUpgrade = ScreenChangeImage("Pictures/Equip Screen/Upgrade.png",(0,0),7)
  statBox = Image("Pictures/Equip Screen/Stat Box.png", (308,10), True)
  barbStats = list(player.barb.stats.values())
  barbStats[0] = player.barb.level
  positions = [(389,13), (389,42), (389,70), (389,97), (389,124), (312,152), (312,182), (312,210)]
  equipped_text = Text("Equipped Weapon:", (160, 188))
  active_attack_text = Text(f"Active Attacks: {len(player.barb.active_attacks)}/{player.barb.max_attacks}", (200,5))  
  active_power_text = Text(f"Equipped Powers: {len(player.active_powers)}/{player.power_limit}",(200,5))
  sword_name, sword_text = get_weapon_descriptions(player, "sword")
  shield_name, shield_text = get_weapon_descriptions(player, "shield")
  overview_screen = Screen(1,[bg, barb, statBox, upgrade, home])
  swords_screen = Screen(2,[bg, weapUpgrade, equipped_text, sword_name, sword_text, home])
  shields_screen = Screen(3,[bg, weapUpgrade, equipped_text, shield_name, shield_text, home])
  attack_screen = Screen(4,[bg, active_attack_text, home])
  power_screen = Screen(5,[bg, upgrade, active_power_text, home])
  screens = [overview_screen, swords_screen, shields_screen, attack_screen, power_screen]
  options = [overview, swords, shields, attacks, powers]
  
  for i,x in enumerate(options):
    if x != options[0]:
      y = options[i-1]
      options[i-1] = ScreenChangeImage(y.name.replace("2","1"), y.top_left,y.mode)
    screens[i].events = screens[i].events[:-1] + options + [screens[i].events[-1]]
    if x != options[-1]:
      x = ScreenChangeImage(x.name.replace("2","1"), x.top_left,x.mode)
      y = options[i+1]
      options[i+1] = ScreenChangeImage(y.name.replace("1","2"), y.top_left,y.mode)
      
  active_screen = overview_screen
  active_screen.draw_events(display)
  drawBarbScreenStats(barbStats, positions, display)
  addWeaponsToBarbScreen(player, "sword", swords_screen)
  addWeaponsToBarbScreen(player, "shield", shields_screen)
  addAttacksToScreen(player.barb, attack_screen)
  get_attack_descriptions(player, attack_screen)
  addPowersToScreen(player, power_screen)
  get_power_descriptions(player, power_screen)
  pygame.display.update()
  
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        close(player)
      elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
        mode = active_screen.handle_events(event,display,0)
        if mode[-1] != 0:
          return 0
        elif 1 in mode:
          active_screen = overview_screen
        elif 2 in mode:
          active_screen = swords_screen
        elif 3 in mode:
          active_screen = shields_screen
        elif 4 in mode:
          active_screen = attack_screen
        elif 5 in mode:
          active_screen = power_screen
        elif 6 in mode:
          return 3
        elif 7 in mode:
          return 4
        elif 8 in mode:
          attack_screen.events.remove(active_attack_text)
          active_attack_text.update_text(f"Active Attacks: {len(player.barb.active_attacks)}/{player.barb.max_attacks}")
          attack_screen.events.insert(-1, active_attack_text)
          removeEventTypeFromScreen(attack_screen, DescText)
          get_attack_descriptions(player, attack_screen)
        elif 9 in mode:
          display_message(player,"Can't have less than one attack!")
        elif 10 in mode:
          display_message(player,"Can't learn any more attacks.")
        elif 11 in mode:
          display_message(player,"Can't equip any more powers.")
        elif 12 in mode:
          power_screen.events.remove(active_power_text)
          active_power_text.update_text(f"Equipped Powers: {len(player.active_powers)}/{player.power_limit}")
          power_screen.events.insert(-1, active_power_text)
          removeEventTypeFromScreen(power_screen, DescText)
          get_power_descriptions(player, power_screen)
        elif 13 in mode:
          weapon_index = mode.index(13)
          equipped_weapon = active_screen.events[weapon_index]
          if equipped_weapon.equipped:
            active_screen.handle_events(event,display,0)
            player.barb.equip_weapon(equipped_weapon.weapon)
            active_screen.events[weapon_index].equipped = True
            if equipped_weapon.weapon.type == "sword":
              removeEventsFromScreen(swords_screen, [sword_name, sword_text])
              sword_name, sword_text = get_weapon_descriptions(player, "sword")
              addEventsToScreen(swords_screen, -1, [sword_name, sword_text])
            elif equipped_weapon.weapon.type == "shield":
              removeEventsFromScreen(shields_screen, [shield_name, shield_text])
              shield_name, shield_text = get_weapon_descriptions(player, "shield")
              addEventsToScreen(shields_screen, -1, [shield_name, shield_text])
          elif not equipped_weapon.equipped:
            if equipped_weapon.weapon.type == "sword":
              removeEventsFromScreen(swords_screen, [sword_name, sword_text])
              sword_name.update_text("None")
              sword_text.update_text("")
              addEventsToScreen(swords_screen, -1, [sword_name, sword_text])
            elif equipped_weapon.weapon.type == "shield":
              removeEventsFromScreen(shields_screen, [shield_name, shield_text])
              shield_name.update_text("None")
              shield_text.update_text("")
              addEventsToScreen(shields_screen, -1, [shield_name, shield_text])
        active_screen.draw_events(display)
        if active_screen == overview_screen:
          barbStats = list(player.barb.stats.values())
          barbStats[0] = player.barb.level
          drawBarbScreenStats(barbStats, positions, display)
        pygame.display.update()

def drawBarbScreenStats(stats, positions, display):
  Text(f"Lv. {stats[0]}", positions[0], white).draw(display)
  Text(f"HP: {round(stats[1])}", positions[1], black).draw(display)
  Text(f"Atk: {round(stats[2])}", positions[2], black).draw(display)
  Text(f"Def: {round(stats[3])}", positions[3], black).draw(display)
  Text(f"Spd: {round(stats[4])}", positions[4], black).draw(display)
  Text(f"Ability Lv: {stats[5]}", positions[5], blue).draw(display)
  Text(f"Crit Rate: {stats[6]}%", positions[6], blue).draw(display)
  Text(f"Dmg Bonus: {stats[7]}%", positions[7], blue).draw(display)
  
def addPowersToScreen(player,power_screen, left=160,top=40):
  for i,power in enumerate(player.unlocked_powers):
    power_screen.events.insert(-1,PowerImage(f"Troops/Icons/{power.internal_name}.png", (left,top), player))
    if (i+1)%2 == 0:
      left = 160
      top += 70
    else:
      left += 70

def get_power_descriptions(player, screen):
  top = 40
  powers = player.active_powers
  for i in range(player.power_limit):
    if i < len(player.active_powers):
      power = powers[i]
      power_name = DescText(f"{power.display_name} Lv {power.level}", (295, top), WINDOW_WIDTH)
      top += power_name.get_height()
      power_text = DescText(power.description, (295, top), WINDOW_WIDTH)
      top += power_text.get_height() + 10
    else:
      power_name = DescText("None", (295, top), WINDOW_WIDTH)
      top += power_name.get_height()
      power_text = DescText("", (295, top), WINDOW_WIDTH)
      top += power_text.get_height() + 10
    screen.events.insert(-1, power_name)
    screen.events.insert(-1, power_text)

def addAttacksToScreen(barb,attack_screen, left=160,top=40):
  for i,attack in enumerate(barb.unlocked_attacks):
    attack_to_add = AttackText(attack, (left,top), barb)
    if left + attack_to_add.get_width()+10 > 512:
      left = 160
      top += 35
      attack_to_add = AttackText(attack, (left,top), barb)
    attack_screen.events.insert(-1,attack_to_add)
    left += attack_to_add.get_width()+10

def get_attack_descriptions(player, screen):
  barb = player.barb
  max_width = WINDOW_WIDTH/barb.max_attacks-2
  for i in range(barb.max_attacks):
    top = 205
    if i < len(barb.active_attacks):
      attack = barb.active_attacks[i]
      attack_name = DescText(attack.display_name, (max_width*i+2, top), max_width*(i+1))
      top += attack_name.get_height()
      details = DescText(f"{attack.element.capitalize()}, {attack.power}, {attack.shield_damage}", (max_width*i+2, 230), WINDOW_WIDTH)
      top += details.get_height()
      screen.events.insert(-1, details)
      attack_text = DescText(attack.description, (max_width*i+2, 255), max_width*(i+1))
      top += attack_name.get_height()
    else:
      attack_name = DescText("None", (max_width*i+2, 205), max_width*(i+1))
      attack_text = DescText("", (max_width*i+2, 230), max_width*(i+1))
    screen.events.insert(-1, attack_name)
    screen.events.insert(-1, attack_text)

def addWeaponsToBarbScreen(player, weapon_type, screen, left=160,top=40):
  if weapon_type == "shield":
    weapons = player.shields
  else:
    weapons = player.swords
  for i,weapon in enumerate(weapons):
    screen.events.insert(-1, WeaponImage(f"Weapons/{weapon.internal_name}.png", (left,top), player.barb, weapon))
    if (i+1)%4 == 3:
      left = 160
      top += 70
    else:
      left += 80

def get_weapon_descriptions(player, weapon_type):
  name = "None"
  text = ""
  if player.barb.weapons[weapon_type] is not None:
    weapon = player.barb.weapons[weapon_type]
    name = f"{weapon.display_name} Lv {weapon.level}"
    text = weapon.description
  weapon_name = Text(name, (160, 215))
  weapon_text = DescText(text, (160, 240), WINDOW_WIDTH)
  return weapon_name, weapon_text

def game(player):
  mode = 0
  while True:
    if mode == 0:
      mode = mainScreen(player)
    elif mode == 1:
      mode = settingsScreen(player)
    elif mode == 2:
      mode = barbScreen(player)
    elif mode == 3:
      mode = troopUpgScreen(player)
    elif mode == 4:
      mode = weaponUpgScreen(player)
    elif mode == 5:
      mode = lootFarmSelectionScreen(player)
    elif mode == 6:
      mode = shopScreen(player)
    elif mode == 7:
      mode = bossScreen(player)
    elif mode == 8:
      old_id = player.id
      player = Player(player.name)
      player.id = old_id
      return False, player
    elif mode == 9:
      delete_player_data(player)
      return True, player

def sendVerificationCode(email,screens,currentMode,newMode=3):
  if Validator.valid_email(email):
    code = random.randint(100000,999999)
    Validator.main(email,code)
    display_message(None,"A code has been sent to your email for verification.",speed="Fast")
    active_screen = screens[newMode-1]
    return code, newMode, active_screen
  else:
    display_message(None,"Invalid email.",speed="Fast")
    active_screen = screens[currentMode-1]
    return 0, currentMode, active_screen

if __name__ == "main":
    title()
