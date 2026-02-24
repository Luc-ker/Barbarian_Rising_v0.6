from Player import Player
from Player_data import test_data, load_player_data
from Game import game
import db_builder

def main():
    test_data()
    details = load_player_data("jlee4889@gmail.com", "sdfds")
    player = Player(details[3]).load(details)
    game(player)

if __name__ == "__main__":
    db_builder.main()
    main()
