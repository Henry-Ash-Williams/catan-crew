from Board import *
from Player import *
from Game import *
from rich import print
from random import choice

def main():
    newBoard = Board(size=3)

    alice = Player('blue')
    bob = Player('red')
    charlie = Player('green')
    david = Player('purple')

    player_order = [alice, bob, charlie, david]
    colors = [player.color for player in player_order]
    print(f"player order: {[f'[bold {color}]{color}[/bold {color}]' for color in colors]}")

    game = Game(board=newBoard, players=player_order)

    game.begin_setup_phase()

    for player in player_order + reversed(player_order):
        # Randomly place settlements and roads on the game board
        player.builds_settlement(location=choice(game.board.intersections))
        player.builds_road(location=choice(game.board.paths))
        player.ends_turn()

    game.distribute_resources()
    game.end_setup_phase()

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
