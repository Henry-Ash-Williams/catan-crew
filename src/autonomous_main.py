#!/usr/bin/env python3

from game import Game
from player import AutonomousPlayer

def main():
    """Creates a game between 4 autonomous players and starts it, for testing"""
    game = Game(getter=input,players=[AutonomousPlayer(color) for color in ['red','green','blue','purple']])

    game.start()


if __name__ == "__main__":
    main()
