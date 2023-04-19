import random
import fileinput
from random import randint
from dill import Pickler, Unpickler
from rich.console import Console
from rich.rule import Rule
from rich.table import Table
from rich.panel import Panel
from rich import print

from bank import Bank
from player import Player
from human_player import HumanPlayer
from autonomous_player import AutonomousPlayer
from board import Board
from resources import (
    Resources,
    RESOURCE_REQUIREMENTS,
    DevelopmentCards,
    ResourceKind,
    knight,
    road_building,
    year_of_plenty,
    monopoly,
)
from clear import clear
from trade import Trade


ROAD_LENGTH_THRESHOLD = 5
ARMY_SIZE_THRESHOLD = 3
ROBBING_THRESHOLD = 7
STARTING_RESOURCES = Resources(10, 10, 10, 10, 10)
VP_TO_WIN = 10

inp = fileinput.input()


def get(prompt, inp):
    print(prompt, end="")
    k = next(inp).strip()
    if inp.fileno() > 0:
        print(k)
    return k


class GameException(Exception):
    pass


class Game:
    def __init__(self, board_size: int = 3, seed=None):
        self.bank = Bank()
        random.seed(seed)
        self.board = Board(board_size, None, seed)
        self.board.game = self

        self.players = []
        self.player_colors = ["red", "green", "blue", "purple"]

        self.current_player_number = 0
        self.current_player = None

        self.dice = randint(1, 6) + randint(1, 6)
        self.is_just_starting = True
        self.is_won = False

        self.turn_count = 0
        self.dev_card_played = False



    def add_player(self, colour: str):
        temp_player = HumanPlayer(colour)
        temp_player.number = len(self.players) + 1
        temp_player.game = self
        temp_player.resources = STARTING_RESOURCES.copy()
        self.players.append(temp_player)

        if self.current_player is None:
            self.current_player = self.players[-1]
            
    def add_autonomous_player(self, colour: str):
        temp_player = AutonomousPlayer(colour)
        temp_player.number = len(self.players) + 1
        temp_player.game = self
        temp_player.resources = STARTING_RESOURCES.copy()
        self.players.append(temp_player)

        if self.current_player is None:
            self.current_player = self.players[-1]

    def check_longest_road(self) -> Player:
        player = max(self.players, key=lambda player: player.road_length)
        return player if player.road_length > ROAD_LENGTH_THRESHOLD else None

    def check_largest_army(self) -> Player:
        player = max(self.players, key=lambda player: player.knights_played)
        return player if player.knights_played > ARMY_SIZE_THRESHOLD else None

    def distribute_resources(self):
        tiles = self.board.tiles_by_token[self.dice]
        for tile in tiles:
            neighboring_settlements = tile.neighboring_settlements()
            for settlement in neighboring_settlements:
                new_resource = self.bank.distribute(
                    settlement.distribution_rate, tile.resource
                )
                settlement.owner.resources += new_resource

    def dice_roll(self):
        self.dice = random.randint(1, 6) + random.randint(1, 6)
        #print(f"Dice rolled. Result: {self.dice}")
        return self.dice

    def print_current_player(self):
        player_color = self.current_player.color
        c = Console()
        r = Rule(
            f"[b {player_color}]{player_color.capitalize()}'s[/b {player_color}] turn ({self.turn_count})"
        )
        c.print(r)

    def display_game_state(self):
        # clear()
        player_data = [
            (
                player.color,
                player.calculate_visible_victory_points(),
                player.calculate_total_victory_points(),
                player.road_length,
                player.knights_played,
                player.resources.total(),
                player.development_cards.total(),
            )
            for player in self.players
        ]
        # player_data.append(player_data)
        # t = Table(title="Player worth")
        # t.add_column("Player")
        # t.add_column("Victory Points")
        # t.add_column("Road Length")
        # t.add_column("Army Size")
        # t.add_column("Resource Cards")
        # t.add_column("Development Cards")

        # for player in player_data:
            # t.add_row(
                # str(player[0]),
                # str(player[1]),
                # str(player[2]),
                # str(player[3]),
                # str(player[4]),
                # str(player[5]),
                # style=player[0],
            # )
        return player_data

    def set_turn(self, player):
        self.current_player = player
        self.current_player_number = player.number
        self.print_current_player()

    def start(self):
        if len(self.players) > 0:
            self.current_player = self.players[0]
        else:
            raise GameException("Cannot have a game with no players")
        #self.set_up_board()
        self.debugging_set_up_board()
        self.game_loop()
        
    def debugging_set_up_board(self):
    
        """Temporary method for setting up the board automatically, for debugging"""
    
        # Iterate over all players twice
        for player in self.players*2:
        
            # Make it this player's turn
            self.set_turn(player)
        
            # Build a settlement at a random valid location for that player
            valid_settlement_locations = self.board.valid_settlement_locations(player, needs_to_be_reachable=False)
            choice = random.choice(valid_settlement_locations)
            player.builds_settlement(choice, for_free = True)
            
            # Build a road at a random valid location for that player
            valid_road_locations = player.reachable_paths()
            choice = random.choice(valid_road_locations)
            player.builds_road(choice, for_free = True)
            
        # Set the next player to be red
        self.set_turn(self.players[0])

    def set_up_board(self):
        for player in self.players:
            self.set_turn(player)
            self.build_settlement(for_free=True)
            self.build_road(for_free=True)

        new_settlement = self.build_settlement(for_free=True)
        self.distribute_bonus(new_settlement)
        self.build_road(for_free=True)
        for player in self.players[-2::-1]:
            self.set_turn(player)
            new_settlement = self.build_settlement(for_free=True)
            self.distribute_bonus(new_settlement)
            self.build_road(for_free=True)

        # self.getter("Press any key to continue")
        clear()

    def distribute_bonus(self, settlement):
        bonus_resources = Resources()
        for tile in settlement.neighboring_resource_tiles():
            bonus_resources += self.bank.distribute(
                settlement.distribution_rate, tile.resource
            )
        settlement.owner.resources += bonus_resources
        settlement.owner.message(f"You got {bonus_resources}")

    def game_loop(self):
        self.turn_count = 1
        c = Console()
        while not self.is_won:
            self.do_turn()
            table = self.display_game_state()
            c.print(table, justify="center")
            c.print(
                Panel(f"Longest Road:\n{self.check_longest_road()}"), justify="center"
            )
            c.print(
                Panel(f"Largest Army:\n{self.check_largest_army()}"), justify="center"
            )  # self.getter("Press any key to continue")
            clear()

        print(f"\n\n{str(self.current_player).upper()} WINS!!")

    def handle_robber(self):
            # self.current_player.message(
                # f"You rolled a 7. Any player with more than {ROBBING_THRESHOLD} resource cards now has to give up half of them!\n"
            # )
            for other_player in self.players:
                player_wealth = other_player.resources.total()
                if player_wealth > ROBBING_THRESHOLD:
                    # other_player.message(
                        # f"[b {other_player.color}]{other_player}[/b {other_player.color}]: a 7 has been rolled. "
                        # + f"You have {player_wealth} resource cards. You have to give up {amount_robbed} of them."
                    # )
                    resources_robbed = other_player.get_valid_resources_to_give_up()
                    other_player.resources -= resources_robbed
                    self.bank.return_resources(resources_robbed)
    def get_available_actions(self, player):
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

        if (not self.dev_card_played) and player.has_knight_card():
            available_actions.append(("Play Knight card", self.play_knight))

        if (not self.dev_card_played) and player.can_play_road_building():
            available_actions.append(
                ("Play Road Building card", self.play_road_building)
            )

        if (not self.dev_card_played) and player.has_year_of_plenty_card():
            available_actions.append(
                ("Play Year of Plenty card", self.play_year_of_plenty)
            )

        if (not self.dev_card_played) and player.has_monopoly_card():
            available_actions.append(("Play Monopoly card", self.play_monopoly))

        available_actions.append(("End turn", self.end_turn))
        return available_actions

    def do_turn(self):
        self.dev_card_played = False
        self.print_current_player()
        self.dice_roll()

        player = self.current_player

        if self.dice == 7:
            self.handle_robber()
        else:
            resources_before = player.resources.copy()
            self.distribute_resources()
            resources_after = player.resources.copy()
            resources_gained = resources_after - resources_before
            print("\nYou got:", str(resources_gained), "\n")

        self.turn_ongoing = True

        while self.turn_ongoing:
            print()
            available_actions = self.get_available_actions(player)

            action_labels = [label for label, method in available_actions]

            choice = self.current_player.prompt_action(action_labels)

            available_actions[choice][1]()

    def add_trade(self, trade: Trade):
        # use this method when interacting via API
        self.trades.append(trade)

    def start_trade(self):
        # use this method when interacting via terminal
        trade = self.current_player.prompt_trade_details()

        while True:
            if self.current_player in trade.proposees:
                self.current_player.message("You can't propose a trade to yourself")
                trade = self.current_player.prompt_trade_details()
            elif not (self.current_player.resources >= trade.resources_offered):
                self.current_player.message(
                    "You don't have enough resources for this trade"
                )
                trade = self.current_player.prompt_trade_details()
            else:
                break

        willing_traders = [
            trader
            for trader in trade.proposees + [self.bank]
            if trader.accepts_trade(trade)
        ]

        if len(willing_traders) == 0:
            self.current_player.message("No trader accepted this trade.")
            return

        trade.accepters = willing_traders
        trade_partner = self.current_player.prompt_trade_partner(trade)

        outgoing = self.current_player.distribute_resources(trade.resources_offered)
        incoming = trade_partner.distribute_resources(trade.resources_requested)

        trade_partner.resources += outgoing
        self.current_player.resources += incoming

    def build_settlement(self, for_free=False):
        valid_settlement_locations = self.board.valid_settlement_locations(
            self.current_player, needs_to_be_reachable=not for_free
        )
        choice = self.current_player.prompt_settlement_location(
            valid_settlement_locations
        )
        return self.current_player.builds_settlement(choice, for_free)

    def build_road(self, for_free=False):
        valid_road_locations = self.current_player.reachable_paths()
        choice = self.current_player.prompt_road_location(valid_road_locations)
        self.current_player.builds_road(choice, for_free)

    def sell_development_card(self):
        cost = self.current_player.distribute_resources(
            RESOURCE_REQUIREMENTS["development_card"]
        )
        self.bank.return_resources(cost)
        dev_card = self.bank.distribute_dev_card()
        self.current_player.gets_development_cards(dev_card)
        self.current_player.message(f"Congrats, you got [b]{str(dev_card)}[/b]")
        return dev_card

    def upgrade_settlement(self):
        settlement = self.current_player.prompt_settlement_for_upgrade()
        self.current_player.upgrade_settlement(settlement)

    def play_monopoly(self):
        self.dev_card_played = True
        self.current_player.development_cards[monopoly] -= 1
        self.bank.development_cards[monopoly] += 1
        resource = self.current_player.prompt_monopoly_resource()
        total_gained = 0
        for player in self.players:
            if player is self.current_player:
                continue
            total_gained += player.resources[resource]
            player.resources[resource] = 0
        self.current_player.resources[resource] += total_gained
        self.current_player.message(f"Congrats, you got {total_gained} {resource}s!")

    def play_year_of_plenty(self):
        self.dev_card_played = True
        self.current_player.development_cards[year_of_plenty] -= 1
        self.bank.development_cards[year_of_plenty] += 1
        for _ in range(2):
            choice = self.current_player.prompt_YoP_resource()
            remaining_tries = 4
            while (not self.bank.resources[choice]) and remaining_tries > 0:
                self.current_player.message(
                    f"Sorry, the bank doesn't have any {choice}. You have {remaining_tries} tries left."
                )
                choice = self.current_player.prompt_YoP_resource()
                remaining_tries -= 1
            self.current_player.resources += self.bank.distribute(1, choice)

    def play_road_building(self):
        self.dev_card_played = True
        self.current_player.development_cards[road_building] -= 1
        self.bank.development_cards[road_building] += 1
        for _ in range(2):
            if self.current_player.can_build_road():
                self.build_road(for_free=True)

    def play_knight(self):
        self.dev_card_played = True
        self.current_player.development_cards[knight] -= 1
        self.bank.development_cards[knight] += 1
        tile_choice = self.current_player.prompt_robber_location()
        self.board.robber_location = tile_choice.location
        self.current_player.knights_played += 1
        neighboring_settlements = tile_choice.neighboring_settlements()
        if not neighboring_settlements:
            self.current_player.message(
                "The tile where the robber has been placed has no neighboring settlements"
            )
            return
        neighboring_players = list(
            set([settlement.owner for settlement in neighboring_settlements])
        )
        neighboring_players = [
            player
            for player in neighboring_players
            if not (player is self.current_player)
        ]
        if not neighboring_players:
            self.current_player.message(
                "You are the only player adjacent to the chosen tile."
            )
            return
        potential_robbees = [
            player for player in neighboring_players if player.has_resources()
        ]
        if not potential_robbees:
            self.current_player.message(
                "None of the players adjacent to this tile have any resource cards."
            )
            return
        robbee = self.current_player.prompt_robbing_victim(potential_robbees)
        available_to_steal = [
            resource for resource in ResourceKind if robbee.resources[resource] > 0
        ]
        resource_to_steal = random.choice(available_to_steal)
        robbee.resources[resource_to_steal] -= 1
        self.current_player.resources[resource_to_steal] += 1
        self.current_player.message(f"You got a {resource_to_steal}.")

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

        self.current_player.development_cards += self.current_player.new_dev_cards
        self.current_player.new_dev_cards = DevelopmentCards()

        # print('VP:',self.current_player.calculate_total_victory_points())
        if self.current_player.calculate_total_victory_points() >= VP_TO_WIN:
            self.is_won = True
        else:
            self.current_player_number = (self.current_player_number + 1) % len(
                self.players
            )
            self.current_player = self.players[self.current_player_number]
            self.turn_count += 1

    def add_road(self, location, road):
        self.verify_current_player_is(road.owner)
        self.board.add_road(road, location)

    def add_settlement(self, location, settlement):
        self.verify_current_player_is(settlement.owner)
        self.board.add_settlement(
            settlement, location, allow_disconnected_settlement=self.is_just_starting
        )

    def save_state(self, filename: str):
        """
        Save game instance to a file
        """
        with open(filename, "wb") as file:
            pickled = Pickler(file)
            pickled.dump(self)

    def load_state(filename: str):
        """
        Load a Game instance from file
        """
        with open(filename, "rb") as file:
            pickle = Unpickler(file)
            return pickle.load()

    def get_game_id(self) -> str:
        """
        Randomly generate a game ID,
        """
        import uuid
        return str(uuid.uuid4())
