from Bank import Bank
from Player import Player
from Player import Player
from Trade import Trade
from Board import Intersection, Path, Tile, Settlement, City, Road, Board
from Resources import Resources

from typing import Union
import random, sys
from rich.console import Console
from rich.rule import Rule
from dataclasses import dataclass


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


class Game:
    def __init__(self):
    
        self.bank = Bank()
        self.board = Board()
        self.board.game = self
        self.players = []

        self.player_number = int(get("How many players would like to play? "))

        for i in range(1, self.player_number + 1):
            color = get("Player #%i's color: " % i)
            self.players.append(Player(color, self)) 
            # I pass game inside player # Ryu #so player know which game are they in?

        requested_colors = set(p.color for p in self.players)
        if len(requested_colors) != len(self.players):
            raise Exception("More than one player have the same color")

        i = 0
        
        for player in self.players:
            player.game = self
            player.number = i
            i += 1

        self.current_player_number = 0
        self.current_player = self.players[self.current_player_number]

        self.is_just_starting = True
        self.is_on = True
        
        self.turn_count = 0

        self.start()

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
        r = Rule(f"[b {player_color}]{player_color.capitalize()}'s[/b {player_color}] turn")
        c.print(r)

    def set_turn(self, player):
        self.current_player = player
        self.current_player_number = player.number
        self.print_current_player()

    def prompt_settlement_location(self, for_free=False):
        choice = None
        while not (choice in self.board.available_intersection_locations):
            choice = int(get("Pick a location to place a settlement: "))
        self.current_player.builds_settlement(choice, for_free)

    def prompt_road_location(self, for_free=False):
        choice = None
        while not (choice in self.board.available_path_locations):
            choice = int(get("Pick a location to place a road: "))
        self.current_player.builds_road(choice, for_free)
        
    def prompt_trade_details(self):
        """Called when user chooses to propose a trade.
        Prompts user for proposed trade details, verifies
        the trade is valid, then initiates proposed trade."""
        details = get('Enter trade details: ')
        
    def prompt_settlement(self):
        """Called when user plays Road Building card.
        Prompts user for settlement they want to upgrade,
        then initiates upgrade"""
        choice = get('Choose a settlement: ')
        
    def prompt_knight(self):
        """Called when user plays Road Building card.
        Prompts user for tile they want to place the robber on,
        then initiates robbery."""
        choice = get('Pick a tile to place the robber on: ')
        
    def prompt_road_building(self):
        """Called when user plays Road Building card.
        Prompts user for the location of a path to build a road on,
        initiates the building of that road, then repeats this again for
        second road."""
        choice = get('Pick a location to place a road: ')
        
    def prompt_year_of_plenty(self):
        """Called when user plays Year of Plenty card.
        Prompts user for a resource type to get from bank,
        passes it to them, then repeats this again for second
        resource type."""
        choice1 = get('Pick a resource type: ')
        choice2 = get('Pick the second resource type: ')
        
    def prompt_monopoly(self):
        """Called when user plays Monopoly card.
        Prompts user for a resource type to steal from all players,
        then steals it for them."""
        choice = get('Pick a resource type: ')
        
    def sell_development_card(self):
        """Called when user chooses to buy a development card.
        Passes development card to them and prints out which card
        they got."""
        print('Congratulations, you got XXXXXXX')

    def start(self):
        self.set_up_board()
        self.game_loop()

    def set_up_board(self):
        for player in self.players:
            self.set_turn(player)
            self.prompt_settlement_location(for_free=True)
            self.prompt_road_location(for_free=True)

        self.prompt_settlement_location(for_free=True)
        self.prompt_road_location(for_free=True)
        for player in self.players[-2::-1]:
            self.set_turn(player)
            self.prompt_settlement_location(for_free=True)
            self.prompt_road_location(for_free=True)

    def game_loop(self):
        while self.is_on:
            self.do_turn()

    def do_turn(self):
        self.print_current_player()
        self.dice_roll()
        
        resources_before = self.current_player.resources
        self.distribute_resources()
        resources_after = self.current_player.resources
        resources_gained = resources_after - resources_before
        print('\nYou got:',resources_gained,'\n')
        
        self.turn_ongoing = True
        
        while self.turn_ongoing:
            print()
        
            self.current_player.get_player_state()
        
            available_actions = []
        
            if self.current_player.has_resources():
                available_actions.append(('Propose a trade', self.prompt_trade_details))
        
            if self.current_player.can_build_road():
                available_actions.append(('Build a road', self.prompt_road_location))
            
            if self.current_player.can_build_settlement():
                available_actions.append(('Build a settlement', self.prompt_settlement_location))
            
            if self.current_player.can_upgrade_settlement():
                available_actions.append(('Upgrade a settlement', self.prompt_settlement))
            
            if self.current_player.can_buy_dev_card():
                available_actions.append(('Buy a development card', self.sell_development_card))
            
            if self.current_player.has_knight_card():
                available_actions.append(('Play Knight card', self.prompt_knight))
            
            if self.current_player.has_road_building_card():
                available_actions.append(('Play Road Building card', self.prompt_road_building))
            
            if self.current_player.has_year_of_plenty_card():
                available_actions.append(('Play Year of Plenty card', self.prompt_year_of_plenty))
            
            if self.current_player.has_monopoly_card():
                available_actions.append(('Play Monopoly card', self.prompt_monopoly))
        
            available_actions.append(('End turn', self.end_turn))
        
            print('\nYou can:')
            for index,(action_name, action_method) in enumerate(available_actions,1):
              print('%i. %s'%(index, action_name))
        
            choice = int(get('What would you like to do? ')) - 1
        
            available_actions[choice][1]()
            
        
        #self.is_on = False
        
    # I guess it's redudiant @Ryu
    # def can_build_road(self, player): return True
    # def can_build_settlement(self, player): return True
        
        

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
        self.current_player_number = (self.current_player_number + 1) % self.player_number
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

    def upgrade_settlement(self, location, city):
        """ upgrade the settlement to city by interacting board"""
        # TODO: 
        self.verify_current_player_is(city.owner)
        self.board.upgrade_settlement(
            location, city, allow_disconnected_settlement=self.is_just_starting
        )

    def play_knight(self, location):
        """ play knight by interacting board"""

    def play_monopoly(self, resource1, resource2):
        """ play monopoly by interacting with other players"""

    def play_year_of_plenty():
        """ play year of plenty by interacting with banks"""

    def play_road_building(location1: int, location2: int):
        """ place two road on board"""

if __name__ == "__main__":
    get = Input_getter("settlers.in").get
    # get = input
    game = Game()


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
