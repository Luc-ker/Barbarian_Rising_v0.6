from BattleEvents import goblinBattle1
from Game import title, intro1, intro2, game

def main():
  deleted = True
  while True:
    if deleted:
      player = title()
    if player.th < 1:
      intro1(player)
      goblinBattle1(player)
      intro2(player)
      player.th = 1
    deleted, player = game(player)

main()

# db_builder.create_player_table()
# db_builder.main()
# test_data()
# details = load_player_data("jlee4889@gmail.com", "sdfds")
# player = Player(details[3]).load(details)
# game(player)