#!/usr/bin/env python3

from Game import Game
from Player import Player
from Bank import Bank
from Trade import Trade
from Board import *
import random, sys
from rich.console import Console
from rich.rule import Rule

ROAD_LENGTH_THRESHOLD = 5
ARMY_SIZE_THRESHOLD = 3


class Input_getter:
    def __init__(self, filename):
        self.index = 0
        self.inputs = open(filename, "r+").readlines()

    def get(self, s):
        if self.index < len(self.inputs):
            inp = self.inputs[self.index].rstrip("\r\n")
            sys.stdout.write(s)
            print(inp)
            self.index += 1
            return inp
        else:
            return input(s)


class GameMaster:
    def __init__(self):
        board = Board()
        players = []

        player_number = int(get("How many players would like to play? "))

        for i in range(1, player_number + 1):
            color = get("Player #%i's color: " % i)
            players.append(Player(color))

        self.game = Game(board, players)
        self.bank = self.game.bank
        self.start()

    def check_longest_road(self) -> Player:
        player = max(self.game.players, key=lambda player: player.road_length)
        return player if player.road_length > ROAD_LENGTH_THRESHOLD else None

    def check_largest_army(self) -> Player:
        player = max(self.game.players, key=lambda player: player.knights_played)
        return player if player.knights_played > ARMY_SIZE_THRESHOLD else None

    def distribute_resources(self, roll: int):
        tiles = self.game.board.tiles_with_token[roll]
        for tile in tiles:
            neighboring_settlements = self.game.board.settlements_neighboring(tile)
            for settlement in neighboring_settlements:
                new_resource = self.bank.distribute(
                    settlement.distribution_rate, tile.resource
                )
                settlement.owner.resources += new_resource

    def handle_trade(self, trade: Trade):
        pass

    def dice_roll(self):
        self.game.dice = random.randint(1, 6) + random.randint(1, 6)
        print("Dice rolled. Result: %i" % self.game.dice)

    def print_current_player(self):
        player_color = self.game.current_player.color
        c = Console()
        r = Rule(f"player [b {player_color}]{player_color}s[/b {player_color}] turn")
        c.print(r)

    def set_turn(self, player):
        self.game.current_player = player
        self.game.current_player_number = player.number
        self.print_current_player()

    def prompt_settlement_location(self):
        choice = None
        while not (choice in self.game.board.available_intersection_locations):
            choice = int(get("Please pick a location to place a settlement: "))
        self.game.current_player.builds_settlement(choice)

    def prompt_road_location(self):
        choice = None
        while not (choice in self.game.board.available_path_locations):
            choice = int(get("Please pick a location to place a road: "))
        self.game.current_player.builds_road(choice)

    def start(self):
        self.set_up_board()
        self.game_loop()

    def set_up_board(self):
        for player in self.game.players:
            self.set_turn(player)
            self.prompt_settlement_location()
            self.prompt_road_location()
        self.prompt_settlement_location()
        self.prompt_road_location()
        for player in self.game.players[-2::-1]:
            self.set_turn(player)
            self.prompt_settlement_location()
            self.prompt_road_location()

    def game_loop(self):
        while self.game.is_on:
            self.do_turn()

    def do_turn(self):
        self.print_current_player()
        self.dice_roll()
        self.game.is_on = False


if __name__ == "__main__":
    get = Input_getter("settlers.in").get
    # get = input
    gamemaster = GameMaster()


# iterate over players
#  - roll dice
#  - give player list of options among
#    - propose a trade
#    - build a road
#    - build a settlement
#    - upgrade settlement to a city
#    - buy a development card
#    - play a development card (multiple kinds)
#    - end turn
#   after each action, check to see if player has won
