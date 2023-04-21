#!/usr/bin/env python3

import json
from game import Game
from board import BoardEncoder

def main():
    """Creates a game between 4 autonomous players and starts it, for testing"""

    game = Game()

    game.add_autonomous_player("red")
    game.add_autonomous_player("green")
    game.add_autonomous_player("blue")
    game.add_autonomous_player("yellow")

    game.start()

    with open('end_board.json','w') as f:
        f.write(json.dumps(game.board, cls=BoardEncoder, indent=4))


if __name__ == "__main__":
    main()
