from BattleEvents import goblinBattle1
from Game import title, intro1, intro2, game
import db_builder

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

if __name__ == "__main__":
    db_builder.main()
    main()
