from Board import *
from Player import *
from Game import *
from GameMaster import GameMaster
from Bank import Bank
from rich import print
from random import choice
import pickle


def main():
    board = Board.read_state("board.pickle")

    alice = Player("blue")
    bob = Player("red")
    charlie = Player("green")
    david = Player("purple")
    player_order = [alice, bob, charlie, david]
    game = Game(board=board, players=player_order)
    bank = Bank()
    game.bank = bank
    game_master = GameMaster(game)

    alice.builds_settlement(location=128)
    alice.builds_road((128 + 23) % 507)


if __name__ == "__main__":
    main()

# alice.roll_dice()
# alice.get_resources(...)
# alice.view_resources()
# alice.view_actions
# alice.view_buildings > return coor
# alice.ends_turn()

# bob.roll_dice()
# bob.trade(alice, wood)
# alice.accept()
# bob.view_resources()
# bob.view_actions
# bob.build...
# bob.end_turns
