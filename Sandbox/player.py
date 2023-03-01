from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel

from rich import print as rich_print

from board import Settlement, City, Road, Tile
from resources import (
    Resources,
    RESOURCE_REQUIREMENTS,
    ResourceKind,
    NO_RESOURCES,
    brick, lumber, ore, grain, wool,
    DevelopmentCardKind,
    DevelopmentCards,
    knight, hidden_victory_point, road_building, year_of_plenty, monopoly
)
from trade import Trade

import random



def join(ll): return [i for k in ll for i in k]


class PlayerException(Exception):
    pass


class Player:
    def __init__(player, color, getter=None):
        player.game = None
        player.color = color
        player.get = getter if getter else input

        player.available_settlements = [Settlement(player) for i in range(5)]
        player.available_cities = [City(player) for i in range(4)]
        player.available_roads = [Road(0, player) for i in range(15)]

        player.built_settlements = []
        player.built_cities = []
        player.built_roads = []

        player.road_length = 0
        player.knights_played = 0

        player.resources = Resources()
        player.new_dev_cards = DevelopmentCards()
        player.development_cards = DevelopmentCards()

        player.exchange_rate = {
            # player side to bank: identical resource to 1 target resource
            brick: {lumber: 4, ore: 4, grain: 4, wool: 4},
            lumber: {brick: 4, ore: 4, grain: 4, wool: 4},
            ore: {brick: 4, lumber: 4, grain: 4, wool: 4},
            grain: {brick: 4, ore: 4, lumber: 4, wool: 4},
            wool: {brick: 4, ore: 4, grain: 4, lumber: 4}
            # how to handle the harbour
            # 1. 3:1 harbour: update all 3
            # 2. 2:1 harbour: update like ore in each to 2
        }

        player.proposed_trades = []

    def __str__(player):
        return player.color.capitalize()

    def __repr__(player):
        return player.color.capitalize()

    def roll_dice(player):
        player.game.dice_roll()

    def view_possible_devcard(self):
        t = Table(title="Available Development Card")
        t.add_column("Dev Card")
        t.add_column("Count")
        t.add_row("Knight", str(self.development_cards[knight]), style="blue_violet")
        t.add_row(
            "Road Building",
            str(self.development_cards[road_building]),
            style="chartreuse4",
        )
        t.add_row(
            "Year of Plenty",
            str(self.development_cards[year_of_plenty]),
            style="red3",
        )
        t.add_row("Monopoly", str(self.development_cards[monopoly]), style="gold1")
        t.add_row(
            "Hidden Victory Point",
            str(self.development_cards[hidden_victory_point]),
            style="grey70",
        )
        return t

    def view_available_resources(self) -> Table:
        # Display resources owned by the player directly to stdout
        t = Table(
            title=f"Player [bold {self.color}]{self.color.upper()}[/bold {self.color}]"
        )
        t.add_column("Resource")
        t.add_column("Count")
        t.add_row("Brick", str(self.resources[brick]), style="#cb4154")
        t.add_row("Lumber", str(self.resources[lumber]), style="green4")
        t.add_row("Ore", str(self.resources[ore]), style="grey30")
        t.add_row("Grain", str(self.resources[grain]), style="gold1")
        t.add_row("Wool", str(self.resources[wool]), style="grey70")
        return t

    def view_available_builds(self) -> list[str]:
        return [
            building
            for building, cost in RESOURCE_REQUIREMENTS.items()
            if self.resources >= cost
        ]

    def get_player_state(self):
        console = Console()
        resource_table = self.view_available_resources()
        available_buildings = self.view_available_builds()
        devcard_table = self.view_possible_devcard()
        building_table = Table(title="Available buildings", width=25)
        building_table.add_column("[b blue]Building[/b blue]")
        [building_table.add_row(building) for building in available_buildings]
        console.print(
            Columns(
                [Panel(resource_table), Panel(building_table), Panel(devcard_table)]
            ),
            justify="center"
        )

    def builds_settlement(player, location, for_free=False):
        cost = (
            player.distribute_resources(RESOURCE_REQUIREMENTS["settlement"])
            if not for_free
            else Resources()
        )
        player.game.bank.return_resources(cost)
        settlement = player.available_settlements.pop()
        player.game.add_settlement(location, settlement)
        settlement.location = location
        player.built_settlements.append(settlement)
        return settlement

    def upgrade_settlement(player, settlement: Settlement):
        cost = player.distribute_resources(RESOURCE_REQUIREMENTS["city"])
        player.game.bank.return_resources(cost)

        city = player.available_cities.pop()
        city.location = settlement.location
        player.built_cities.append(city)

        player.built_settlements.remove(settlement)
        settlement.location = None
        player.available_settlements.append(settlement)

        player.game.board.cells[city.location].settlement = city

    def builds_road(player, location, for_free=False):
        cost = (
            player.distribute_resources(RESOURCE_REQUIREMENTS["road"])
            if not for_free
            else Resources()
        )
        player.game.bank.return_resources(cost)
        road = player.available_roads.pop()
        player.game.add_road(location, road)
        road.location = location
        player.built_roads.append(road)

    # def play_knight(player, location):
    #    player.development_cards["knight"] -= 1
    #    player.game.play_knight(location)

    def play_monopoly(player, resource_type: ResourceKind):
        player.development_cards[monopoly] -= 1
        player.game.play_monopoly(resource_type)

    def play_year_of_plenty(player, resource1: str, resource2: str):
        # check dev card
        if player.development_cards[year_of_plenty] <= 0:
            raise Exception("Player has no available year_of_plenty card to play")

        player.development_cards[year_of_plenty] -= 1
        player.game.play_monopoly(player, resource1, resource2)

    def play_road_building(player, location1, location2):
        # can place 2 roads immediately
        player.development_cards[road_building] -= 1
        player.game.add_road(location1)
        player.game.add_road(location2)

    def update_exchange_rate(
        player, special_harbour: bool = False, resource_type: ResourceKind = None
    ):
        if special_harbour:
            for inner_dict in player.exchange_rate.values():
                inner_dict[resource_type] = 2
        else:
            for inner_dict in player.exchange_rate.values():
                keys = inner_dict.keys()
                for key in keys:
                    inner_dict[key] = 3

    def reachable_paths(player):
        """Returns paths that player can reach based on their currently built settlements and roads"""
        board = player.game.board
        adjacent_to_settlement = join(
            board.select(around=settlement.location, distance=1)
            for settlement in player.built_settlements
        )
        adjacent_to_road = join(
            board.select(around=road.location, distance=1, dir_pattern=(1, 1))
            for road in player.built_roads
        )
        return list(
            (set(adjacent_to_settlement) | set(adjacent_to_road))
            & set(board.available_path_locations)
        )

    ####### avavilable actions validation #######

    def can_build_road(player):
        """Returns whether a player can build a road or not."""
        if len(player.reachable_paths()) < 1:
            return False
        return len(player.available_roads) > 0 and player.resources >= RESOURCE_REQUIREMENTS["road"]
        

    def can_build_settlement(player):
        """Returns whether a player can build a settlement or not."""
        if len(player.available_settlements) == 0:
            return False
        if not player.resources >= RESOURCE_REQUIREMENTS["settlement"]:
            return False
        if not player.game.board.valid_settlement_locations(player):
            return False

        return True

    def has_resources(player):
        """Returns True if player has any resource to trade."""
        return player.resources > NO_RESOURCES

    def can_upgrade_settlement(player):
        """Returns True if player has an un-upgraded settlement and
        enough resources to upgrade it."""

        # no sure if we upgrade a city, do we pop settlement out of built-settlement
        return (
            player.resources >= RESOURCE_REQUIREMENTS["city"]
            and len(player.available_cities) > 0
            and len(player.built_settlements) > 0
        )

    def can_buy_dev_card(player):
        """Returns True if player can afford a development card."""
        if player.game.bank.development_cards.total() <= 0:
            return False
        return player.resources >= RESOURCE_REQUIREMENTS["development_card"]

    def has_knight_card(player):
        """Returns True if player has a Knight card."""
        return player.development_cards[knight] > 0

    def can_play_road_building(player):
        """Returns True if player has a Road_Building card."""
        return player.can_build_road() and player.development_cards[road_building] > 0

    def has_year_of_plenty_card(player):
        """Returns True if player has a year_of_plenty card."""
        return player.development_cards[year_of_plenty] > 0

    def has_monopoly_card(player):
        """Returns True if player has a Monopoly card."""
        return player.development_cards[monopoly] > 0

    def calculate_visible_victory_points(player):
        """for each action, the game can update this, so that every players can view other players' VP in real time"""
        # please refactor this line
        player.visible_victory_points = (
            1 * len(player.built_settlements)
            + 2 * len(player.built_cities)
            + 2 * (player.game.check_longest_road() is player)
            + 2 * (player.game.check_largest_army() is player)
        )

        return player.visible_victory_points

    def calculate_total_victory_points(player):
        """for each action, the game can update this, so that by the time player do an action to win, the game just ends"""
        return (
            player.calculate_visible_victory_points()
            + player.development_cards[hidden_victory_point]
        )

    def gets_development_cards(player, dev_cards: DevelopmentCards):
        """Takes a development card parameter, adds it to this player's development cards."""
        player.new_dev_cards += dev_cards

    def message(player, msg: str):
        c = Console()
        c.print(msg)

    def distribute_resources(player, resources: Resources) -> Resources:
        player.resources -= resources
        return resources
        
    def get_valid_resources_to_give_up(player):
        resources = player.prompt_resources_to_give_up()
        while not(player.resources >= resources) \
              or resources.total() < player.resources.total()//2:
            if not(player.resources >= resources):
                player.message("That's more than you have. Try again.")
                resources = player.prompt_resources_to_give_up()
            else:
                player.message(f"You're giving up {resources.total()} " +
                               f"resource cards but the minimum is {player.resources.total()//2}. Try again")
                resources = player.prompt_resources_to_give_up()
        print()
        return resources


class HumanPlayer(Player):
    def prompt_settlement_location(player, valid_settlement_locations):
        choice = None
        print(f"Valid settlement locations: {valid_settlement_locations}")  # TODO
        while not (choice in valid_settlement_locations):
            choice = int(player.get("Pick a location to place a settlement: "))
        return choice

    def prompt_road_location(player, valid_road_locations):
        choice = None
        print(f"Valid road locations: {valid_road_locations}")
        while not (choice in valid_road_locations):
            choice = int(player.get("Pick a location to place a road: "))
        return choice
        
    def prompt_resources(player, prompt_string) -> Resources:
        resources_requested_input = player.get(
            f"{prompt_string} in format {', '.join(ResourceKind.__members__)}: ")
        
        while True:
            try:    return Resources(*eval(resources_requested_input))
            except:
                resources_requested_input = player.get(
                    "That doesn't look right. Try again: ")
        
    def prompt_resources_to_give_up(player):
        rich_print(f"[b {player.color}]{player}[/b {player.color}]: you have {player.resources}")
        resources = player.prompt_resources(f"[b {player.color}]{player}[/b {player.color}]: choose resources to give up")
        return resources

    def prompt_trade_proposees(player) -> list[Player]:
    
        print("You can propose this trade to:")
        other_players = [p for p in player.game.players if not(p is player)]
        
        for index, proposee in enumerate(other_players, 1):
            print("%i. %s" % (index, proposee))

        prompt1 = "Who would you like to propose this trade to? "
        choices = [p.strip() for p in player.get(prompt1).split(",")]
        choices_are_numbers = all(p.isnumeric() for p in choices)
        
        if choices_are_numbers:
            numeric_choices = [int(choice) for choice in choices]
            choices_in_range = min(numeric_choices) > 0 and \
                               max(numeric_choices) <= len(other_players)

        while not (choices_are_numbers and choices_in_range):
            prompt2 = "That is not a valid selection of players. Try again: "
            choices = [p.strip() for p in player.get(prompt2).split(",")]
            choices_are_numbers = all([p.isnumeric() for p in choices])
            if choices_are_numbers:
                numeric_choices = [int(choice) for choice in choices]
                choices_in_range = min(numeric_choices) > 0 and \
                                   max(numeric_choices) <= len(other_players)

        return [other_players[choice - 1] for choice in numeric_choices]

    def prompt_trade_details(player):
        """Called when user chooses to propose a trade.
        Prompts user for proposed trade details, verifies
        the trade is valid, then returns trade object."""
        
        resources_offered = player.prompt_resources("Enter resources you're offering")
        while not (player.resources >= resources_offered):
            resources_offered = player.prompt_resources("You don't have that many resources. Try again:")
            
        resources_requested = player.prompt_resources('Enter resources you want to get')
        while not (player.resources >= resources_offered):
            resources_offered = player.prompt_resources("You don't have that many resources. Try again:")

        proposees = player.prompt_trade_proposees()

        return Trade(
            sender=player,
            resources_offered=resources_offered,
            resources_requested=resources_requested,
            proposees=proposees,
        )

    def accepts_trade(player, trade):
        if player.resources >= trade.resources_requested:
            response = player.get(f"[b {player.color}]{player}[/b {player.color}]: would you like to accept this trade? (y/n) ")
            decision = True if response.lower()=='y' else False
        else:
            decision = False
        rich_print(
            f"[b {player.color}]{player}[/b {player.color}] {['rejects','accepts'][decision]} trade proposed by {trade.sender}"
        )
        return decision

    def prompt_trade_partner(player, trade):
        print("\nYou can trade with:")
        for index, accepter in enumerate(trade.accepters, 1):
            print(f"{index}. {accepter}")

        choice = int(player.get("Pick a trade partner: "))

        return trade.accepters[choice - 1]

    def prompt_settlement_for_upgrade(player) -> Settlement:
        """Called when the user chooses to upgrade a settlement.
        Prompts user for settlement they want to upgrade."""
        choice = None
        print(
            f"Your settlements: {[settlement.location for settlement in player.built_settlements]}"
        )
        while not (
            choice in [settlement.location for settlement in player.built_settlements]
        ):
            choice = int(player.get("Pick one of your settlement to upgrade: "))
        return player.game.board.cells[choice].settlement

    def prompt_knight(player):
        """Called when user plays knight card.
        Prompts user for tile they want to place the robber on,
        then initiates robbery."""
        choice = None
        while not (choice in player.game.board.tile_locations):
            choice = player.get("Pick a tile to place the robber on: ")
        return choice

    def prompt_road_building(player):
        """Called when user plays Road_Building card.
        Prompts user for the location of a path to build a road on,
        initiates the building of that road, then repeats this again for
        second road."""
        # the reason why we don't return 2 chocie at the same time
        # is because we can build 1 road and build the next road next to the first road
        choice = None
        while not (choice in player.reachable_paths()):
            choice = int(player.get("Pick a location to place a road: "))
        return choice

    def prompt_robbing_victim(player, robbee_options: list[Player]) -> Player:
        """Prompts the player for a choice of other player to rob."""
        available_robbees = [
            (potential_robbee.color, potential_robbee)
            for potential_robbee in robbee_options
        ]

        print("\nYou can rob:")
        for index, (color, robbee) in enumerate(available_robbees, 1):
            print(f"{index}. {color}")

        choice = int(player.get("Who would you like to rob? ")) - 1

        return robbee_options[choice]

    def prompt_robber_location(player) -> Tile:
        """Prompts player for a location at which to place the robber."""
        chosen_tile_location = int(
            player.get("Pick a location at which to place the robber: ")
        )
        valid_tile = player.game.board.has(Tile)(chosen_tile_location)
        robber_moved = chosen_tile_location != player.game.board.robber_location
        while not (valid_tile and robber_moved):
            if not robber_moved:
                chosen_tile_location = int(
                    player.get("The robber is already on that tile. Pick another: ")
                )
            elif not valid_tile:
                chosen_tile_location = int(
                    player.get(
                        "Sorry, that's not a valid tile location. Pick another: "
                    )
                )
            valid_tile = player.game.board.has(Tile)(chosen_tile_location)
            robber_moved = chosen_tile_location != player.game.board.robber_location
        chosen_tile = player.game.board.cells[chosen_tile_location]
        return chosen_tile

    def prompt_resource(player, prompt) -> ResourceKind:
        choice = player.get(prompt).lower()
        while not choice in ResourceKind.__members__:
            choice = player.get(
                "That is not a valid resource name. Try again: "
            ).lower()
        resource = ResourceKind(ResourceKind[choice])
        return resource

    def prompt_monopoly_resource(player) -> ResourceKind:
        return player.prompt_resource("Select a resource to monopolize: ")

    def prompt_YoP_resource(player) -> ResourceKind:
        return player.prompt_resource("Select a resource to get from bank: ")

    def prompt_action(player, action_labels):
        print("\nYou can:")
        for index, action_label in enumerate(action_labels, 1):
            print(f"{index}. {action_label}")
        return int(player.get("What would you like to do? ")) - 1


class AutonomousPlayer(Player):
    def prompt_settlement_location(player, valid_settlement_locations):
        location = random.choice(valid_settlement_locations)
        print(f"{player} builds a settlement at location {location}")
        return location

    def prompt_road_location(player, valid_road_locations):
        location = random.choice(valid_road_locations)
        print(f"{player} builds a road at location {location}")
        return location

    def prompt_trade_details(player):
        individual_resources = [Resources(kind) for kind in ResourceKind]
        resources_offered = random.choice(individual_resources)
        resources_requested = random.choice(individual_resources)
        other_players = [p for p in player.game.players if not(p is player)]
        proposees = random.sample(
            other_players, random.randint(1, len(other_players))
        )
        print(
            f"{player} proposes a trade of {resources_offered} for {resources_requested} to {proposees}"
        )
        return Trade(player, resources_offered, resources_requested, proposees)

    def accepts_trade(player, trade):
        if player.resources >= trade.resources_requested:
            decision = random.choice([True, False])
        else:
            decision = False
        print(
            f"{player} {['rejects','accepts'][decision]} trade proposed by {trade.sender}"
        )
        return decision

    def prompt_trade_partner(player, trade):
        chosen_trade_partner = random.choice(trade.accepters)
        print(f"{player} chooses to trade with {chosen_trade_partner}")
        return chosen_trade_partner

    def prompt_settlement_for_upgrade(player) -> Settlement:
        settlement = random.choice(player.built_settlements)
        print(f"{player} upgrades settlement at location {settlement.location}")
        return settlement

    def prompt_knight(player):
        options = player.game.board.tile_locations[:]
        options.remove(player.game.board.robber_location)
        chosen_location = random.choice(options)
        print(f"{player} places Knight at location {chosen_location}")
        return chosen_location

    def prompt_road_building(player):
        location = random.choice(player.game.board.valid_road_locations(player))
        print(f"{player} builds a road at location {location}")
        return location

    def prompt_robbing_victim(player, robbee_options: list[Player]) -> Player:
        robbing_victim = random.choice(robbee_options)
        print(f"{player} robs {robbing_victim}")
        return robbing_victim

    def prompt_robber_location(player) -> Tile:
        options = player.game.board.tile_locations[:]
        print("Options:", options)
        print("Current robber location:", player.game.board.robber_location)
        options.remove(player.game.board.robber_location)
        tile_location = random.choice(options)
        print(f"{player} moves robber to location {tile_location}")
        return player.game.board.cells[tile_location]

    def prompt_monopoly_resource(player) -> ResourceKind:
        choice = ResourceKind(random.randint(0, 4))
        print(f"{player} monopolizes {choice}")
        return choice

    def prompt_YoP_resource(player) -> ResourceKind:
        choice = ResourceKind(random.randint(0, 4))
        print(f"{player} uses Year of Plenty to get {choice} from the bank")
        return choice

    def prompt_action(player, action_labels):
        action_index = random.randint(0, len(action_labels) - 1)
        print(f"{player} chooses to ({action_labels[action_index]})")
        return action_index
        
    def prompt_resources_to_give_up(player):
        resources = player.resources.random_subset()
        while resources.total() > player.resources.total()//2:
            resources = player.resources.random_subset()
        return resources


class TesterPlayer(AutonomousPlayer):
    def upgrade_settlement(player, settlement: Settlement):
        settlement_location = settlement.location
        settlement_intersection = player.game.board.cells[settlement.location]

        assert settlement in player.built_settlements
        assert not (settlement in player.available_settlements)

        super().upgrade_settlement(settlement)

        assert not (settlement in player.built_settlements)
        assert settlement in player.available_settlements

        assert settlement_intersection.has_settlement
        assert type(settlement_intersection.settlement) is City

        new_city = settlement_intersection.settlement
        assert new_city.location == settlement_location
        assert new_city in player.built_cities
        assert not (new_city in player.available_cities)
