from Board import *
from Player import *
from Game import *
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

    bob.resources = Resources(brick=1, lumber=2, grain=1)
    bob.view_available_resources()
    # print(bob.view_possible_builds())


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
