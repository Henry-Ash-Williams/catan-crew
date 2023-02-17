from Bank import Bank
from Player import Player, HumanPlayer
from Trade import Trade
from Board import Intersection, Path, Tile, Settlement, City, Road, Board
from Resources import Resources
from clear import clear
from pickle import Pickler, Unpickler

from typing import Union
import random, sys, fileinput
from rich.console import Console
from rich.rule import Rule
from rich.table import Table
from dataclasses import dataclass


ROAD_LENGTH_THRESHOLD = 5
ARMY_SIZE_THRESHOLD = 3


class GameException(Exception):
    pass


class Game:
    def __init__(self, getter, players=[], has_human_players=False, seed=None):
    
        clear()
        self.getter = getter
        self.bank = Bank()
        self.board = Board(seed=seed)
        self.board.game = self
        
        self.players = players
        self.player_colors = [player.color for player in players]

        if has_human_players:
            player_number = self.prompt_player_number()
            for number in range(player_number):
                self.prompt_human_player()

        if len(self.players)<1:
            raise GameException("You can't have a game with no players")
        
        self.current_player_number = 0
        self.current_player = self.players[self.current_player_number]

        self.is_just_starting = True
        self.is_on = True

        self.turn_count = 0

        # self.start()
    
    def prompt_player_number(self):
        return int(self.getter("How many players would like to play? "))
    
    def prompt_human_player(self):
        player_number = len(self.players) + 1
        color = self.getter("Player #%i's color: " % player_number)
        while color in self.player_colors:
            color = self.getter('Sorry, that color is already taken. Please choose a different color: ')
        new_player = HumanPlayer(color, self.getter)
        new_player.number = player_number
        new_player.game = self
        self.players.append(new_player)

    def check_longest_road(self) -> Player:
        player = max(self.players, key=lambda player: player.road_length)
        return player if player.road_length > ROAD_LENGTH_THRESHOLD else None

    def check_largest_army(self) -> Player:
        player = max(self.players, key=lambda player: player.knights_played)
        return player if player.knights_played > ARMY_SIZE_THRESHOLD else None

    def distribute_resources(self):
        tiles = self.board.tiles_with_token[self.dice]
        for tile in tiles:
            neighboring_settlements = self.board.settlements_neighboring(tile)
            for settlement in neighboring_settlements:
                new_resource = self.bank.distribute(
                    settlement.distribution_rate, tile.resource
                )
                settlement.owner.resources += new_resource

    def handle_trade(self, trade: Trade):
        pass

    def dice_roll(self):
        self.dice = random.randint(1, 6) + random.randint(1, 6)
        print("Dice rolled. Result: %i" % self.dice)

    def print_current_player(self):
        player_color = self.current_player.color
        c = Console()
        r = Rule(
            f"[b {player_color}]{player_color.capitalize()}'s[/b {player_color}] turn"
        )
        c.print(r)

    def display_game_state(self):
        clear()
        player_data = [
            (
                player.color,
                player.visible_victory_points,
                player.road_length,
                player.knights_played,
                player.resources.card_count()[0],
                player.resources.card_count()[1],
            )
            for player in self.players
        ]

        t = Table(title="Player worth")
        t.add_column("Player")
        t.add_column("Victory Points")
        t.add_column("Road Length")
        t.add_column("Army Size")
        t.add_column("Resource Cards")
        t.add_column("Development Cards")

        for player in player_data:
            t.add_row(
                player[0],
                str(player[1]),
                str(player[2]),
                str(player[3]),
                str(player[4]),
                str(player[5]),
                style=player[0],
            )
        return t

    def set_turn(self, player):
        self.current_player = player
        self.current_player_number = player.number
        self.print_current_player()

    def start(self):
        self.set_up_board()
        self.game_loop()

    def set_up_board(self):
        for player in self.players:
            self.set_turn(player)
            self.build_settlement(for_free=True)
            self.build_road(for_free=True)

        self.build_settlement(for_free=True)
        self.build_road(for_free=True)
        for player in self.players[-2::-1]:
            self.set_turn(player)
            self.build_settlement(for_free=True)
            self.build_road(for_free=True)

        self.getter("Press any key to continue")
        clear()

    def game_loop(self):
        c = Console()
        while self.is_on:
            self.do_turn()
            table = self.display_game_state()
            clear()
            c.print(table, justify="center")
            self.getter("Press any key to continue")
            clear()

    def do_turn(self):
        self.print_current_player()
        self.dice_roll()

        player = self.current_player

        resources_before = player.resources
        self.distribute_resources()
        resources_after = player.resources
        resources_gained = resources_after - resources_before
        print("\nYou got:", str(resources_gained), "\n")

        self.turn_ongoing = True

        while self.turn_ongoing:
            print()

            player.get_player_state()

            available_actions = []

            if player.has_resources():
                available_actions.append(("Propose a trade", self.start_trade))

            if player.can_build_road():
                available_actions.append(("Build a road", self.build_road))

            if player.can_build_settlement():
                available_actions.append(("Build a settlement", self.build_settlement))

            if player.can_upgrade_settlement():
                available_actions.append(
                    ("Upgrade a settlement", self.upgrade_settlement)
                )

            if player.can_buy_dev_card():
                available_actions.append(
                    ("Buy a development card", self.sell_development_card)
                )

            if player.has_knight_card():
                available_actions.append(("Play Knight card", self.play_knight))

            if player.has_road_building_card():
                available_actions.append(
                    ("Play Road Building card", self.play_road_building)
                )

            if player.has_year_of_plenty_card():
                available_actions.append(
                    ("Play Year of Plenty card", self.play_year_of_plenty)
                )

            if player.has_monopoly_card():
                available_actions.append(("Play Monopoly card", self.play_monopoly))

            available_actions.append(("End turn", self.end_turn))

            print("\nYou can:")
            for index, (action_name, action_method) in enumerate(available_actions, 1):
                print("%i. %s" % (index, action_name))

            choice = int(self.getter("What would you like to do? ")) - 1

            available_actions[choice][1]()

    def start_trade(self):
        trade = self.current_player.prompt_trade_details()
        willing_traders = [
            trader
            for trader in trade.proposees + [self.bank]
            if trader.accepts_trade(trade)
        ]

        if len(willing_traders) == 0:
            self.current_player.message("No trader accepted this trade.")
            return

        else:
            trade.accepters = willing_traders
            self.current_player.prompt_trade_partner(trade)

    def build_settlement(self, for_free=False):
        choice = self.current_player.prompt_settlement_location()
        self.current_player.builds_settlement(choice, for_free)

    def build_road(self, for_free=False):
        choice = self.current_player.prompt_road_location()
        self.current_player.builds_road(choice, for_free)

    def sell_development_card(self):
        self.current_player.buy_development_card()

    def upgrade_settlement(self):
        settlement = self.current_player.prompt_settlement_for_upgrade()
        self.board.cells[settlement.location].settlement = None
        self.board.cells[settlement.location].has_settlement = False
        # TODO: finish this

    def play_knight(self):
        """play knight by interacting board"""
        pass

    def play_monopoly(self):
        resource_name = self.current_player.prompt_monopoly_resource().name
        total_gained = 0
        for player in self.players:
            if player is self.current_player:
                continue
            total_gained += player.resources[resource_name]
            player.resources[resource_name] = 0
        self.current_player.resources[resource_name] += total_gained
        self.current_player.message(
            "Congrats, you got %i %ss!" % (resource_name, total_gained)
        )

    def play_year_of_plenty(self):
        for _ in range(2):
            choice = self.current_player.prompt_YoP_resource()
            while not self.bank.available_resources[choice.name]:
                self.current_player.message(
                    "Sorry, the bank doesn't have any %s." % choice.name
                )
                choice = self.current_player.prompt_YoP_resource()
            self.current_player.resources += self.bank.distribute_resources(1, choice)

    def play_road_building(self):
        for _ in range(2):
            self.build_road(for_free=True)

    def verify_current_player_is(self, player):
        if player != self.current_player:
            raise Exception(
                f"Player {player.color} can't play as it's {self.current_player.color}'s turn."
            )

    def check_win_condition(self) -> bool:
        victory_points = [
            player.victory_points + player.hidden_victory_points
            for player in self.players
        ]
        win_status = [vp >= 10 for vp in victory_points]
        return any(win_status)

    def end_turn(self):
        self.turn_ongoing = False
        self.current_player_number = (self.current_player_number + 1) % len(self.players)
        self.current_player = self.players[self.current_player_number]
        self.turn_count += 1

    def add_road(self, location, road):
        self.verify_current_player_is(road.owner)
        self.board.add_road(location, road)

    def add_settlement(self, location, settlement):
        self.verify_current_player_is(settlement.owner)
        self.board.add_settlement(
            location, settlement, allow_disconnected_settlement=self.is_just_starting
        )

    def move_robber(self):
        tile_choice = self.current_player.prompt_robber_location()
        self.board.robber_location = tile_choice
        neighboring_settlements = self.board.settlements_neighboring(tile_choice)
        neighboring_players = set(
            [settlement.owner for settlement in neighboring_settlements]
        )
        robbee = self.current_player.prompt_robbing_victim(neighboring_players)
        if not robbee.has_resources:
            self.current_player.message(
                "%s has no resources to rob." % robbee.color.capitalize()
            )
        else:
            available_to_steal = filter(
                lambda r: robbee.resources[r] > 0,
                ["brick", "lumber", "ore", "grain", "wool"],
            )
            resource_to_steal = random.choice(available_to_steal)
            robbee.resources[resource_to_steal] -= 1
            self.current_player.resources[resource_to_steal] += 1
            self.current_player.message("You got a %s." % resource_to_steal)


    def save_state(self, filename: str):
        with open(filename, "wb") as file:
            pickled = Pickler(file)
            pickled.dump(self)

    def load_state(filename: str):
        with open(filename, "rb") as file:
            pickle = Unpickler(file)
            return pickle.load()

if __name__ == "__main__":
    inp = fileinput.input()
    def get(s):
        sys.stdout.write(s)
        sys.stdout.flush()
        k=inp.__next__().strip()
        if inp.fileno()>0: print(k)
        return k
    #get = input
    game = Game(getter=get, has_human_players=True)
    game.start()

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
