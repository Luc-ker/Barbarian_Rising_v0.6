with open("stat.txt", "r") as f1, open("stats.txt", "w") as f2:
  for line in f1:
    if line[:3] == "[TH":
      f2.write(line.replace("BATTLE","BATTLE1"))
    else:
      f2.write(line)