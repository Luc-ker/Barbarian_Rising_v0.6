lv = 1
hp = 360
atk = 260
defe = 260
spd = 35
abil_lv = 19
stop = 50

while lv <= stop:
  with open("./Stats/generated stats.txt","a") as f1:
    f1.write(f"{lv},{hp},{atk},{defe},{spd},{abil_lv}\n")
  lv += 1
  hp += 7
  atk += 5
  defe += 5
  if lv % 5 == 0:
    spd += 1
  if lv % 5 == 1:
    abil_lv += 1
