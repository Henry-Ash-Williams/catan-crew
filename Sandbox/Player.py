from Board import *
from Resources import Resources, RESOURCE_REQUIREMENTS
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from copy import copy

class Player:
    def __init__(player, color, game, getter = None):
        player.color = color
        player.game = game
        player.get = input if getter==None else getter

        player.available_settlements = [Settlement(player) for i in range(5)]
        player.available_cities = [City(player) for i in range(4)]
        player.available_roads = [Road(0, player) for i in range(15)]

        player.built_settlements = []
        player.built_cities = []
        player.built_roads = []

        # Victory point related
        player.road_length = 0
        player.knights_played = 0
        player.visible_victory_points = 0
        player.hidden_victory_points = 0

        player.resources = Resources()
        player.development_cards = {
            "knight": 0,
            "road building": 0,
            "year of plenty": 0,
            "monopoly": 0,
        }  # TODO: either dict or dataclass

        player.exchange_rate = {
            # player side to bank: identical resource to 1 target resource
            "brick": {"lumber": 4, "ore": 4, "grain": 4, "wool": 4},
            "lumber": {"brick": 4, "ore": 4, "grain": 4, "wool": 4},
            "ore": {"brick": 4, "lumber": 4, "grain": 4, "wool": 4},
            "grain": {"brick": 4, "ore": 4, "lumber": 4, "wool": 4},
            "wool": {"brick": 4, "ore": 4, "grain": 4, "lumber": 4}
            # how to handle the harbour
            # 1. 3:1 harbour: update all 3
            # 2. 2:1 harbour: update like ore in each to 2
        }

        player.proposed_trades = []

    # def builds_settlement(player, location):
    #  player.game.board.add_settlement(location, player)

    # def builds_road(player, location):
    #  player.game.board.add_road(location, player)

    def roll_dice(player):
        player.game.dice_roll()

    def view_possible_devcard(self):
        t = Table(title="Available Development Card")
        t.add_column("Dev Card")
        t.add_column("Count")
        t.add_row("Knight", str(self.development_cards["knight"]), style="#cb4154")
        t.add_row(
            "Road Building",
            str(self.development_cards["road building"]),
            style="green4",
        )
        t.add_row(
            "Year of Plenty",
            str(self.development_cards["year of plenty"]),
            style="grey30",
        )
        t.add_row("Monopoly", str(self.development_cards["monopoly"]), style="gold1")
        return t

    def view_available_resources(self) -> Table:
        # Display resources owned by the player directly to stdout
        t = Table(
            title=f"Player [bold {self.color}]{self.color.upper()}[/bold {self.color}]"
        )
        t.add_column("Resource")
        t.add_column("Count")
        t.add_row("Brick", str(self.resources.brick), style="#cb4154")
        t.add_row("Lumber", str(self.resources.lumber), style="green4")
        t.add_row("Ore", str(self.resources.ore), style="grey30")
        t.add_row("Grain", str(self.resources.grain), style="gold1")
        t.add_row("Wool", str(self.resources.wool), style="grey70")
        return t

    def view_available_builds(self) -> list[str]:
        return [
            building
            for building, cost in RESOURCE_REQUIREMENTS.items()
            if self.resources.can_build(cost)
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
            )
        )

    def builds_settlement(player, location, for_free=False):
        player.resources -= Resources() if for_free else RESOURCE_REQUIREMENTS["settlement"]
        settlement = player.available_settlements.pop()
        player.game.add_settlement(location, settlement)
        player.built_settlements.append((settlement, location))

    def upgrade_settlement(player, location):
        player.resources -= RESOURCE_REQUIREMENTS["city"]
        city = player.available_cities.pop()
        player.game.upgrade_settlement(location, city)
        player.built_cities.append((city, location))   
        player.available_settlements.append(Settlement(player))        

    def builds_road(player, location, for_free=False):
        # TODO: make this method subtract from player's resources

        # shall these handel by gamemaster to look over to it
        # when gamemaster give options for player to choose
        
        player.resources -= Resources() if for_free else RESOURCE_REQUIREMENTS["road"]

        if player.available_roads:
            road = player.available_roads.pop()
        else:
            raise Exception("Player has no available roads to build")
            
        player.game.add_road(location, road)
        player.built_roads.append((road, location))

    def play_knight(player, location):
        player.development_cards["knight"] -= 1
        player.game.play_knight(location)

    def play_monopoly(player, resource_type: ResourceKind):
        player.development_cards["monopoly"] -= 1
        player.game.play_monopoly(resource_type)

    def play_year_of_plenty(player, resource1: str, resource2: str):
        # check dev card
        if player.development_cards["year of plenty"] <= 0:
            raise Exception("Player has no available year of plenty card to play")
        else:
            player.development_cards["year of plenty"] -= 1
            player.game.play_monopoly(player, resource1, resource2)

    def play_road_building(player, location1, location2):
        # can place 2 roads immediately
        player.development_cards["road building"] -= 1
        player.game.add_road(location1)
        player.game.add_road(location2)

    def ends_turn(player):
        player.game.end_turn()

    def handle_trade(self, trade):
        pass

    def propose_trade(
        self,
        offered_to,
        resources_offered: Resources,
        resources_requested: Resources,
    ):
        # check resource
        for offering_resources, player_resources in zip(
            resources_offered, self.resources
        ):
            if offering_resources > player_resources:
                raise Exception(
                    "player doesn't have enough resources to for this trade"
                )

        t = Trade(
            sender=self,
            resources_offered=resources_offered,
            resources_requested=resources_requested,
        )

        for player in offered_to + [self.game.bank]:
            new_trade = copy(t)
            new_trade.recipient = player
            player.proposed_trades.append(new_trade)

    def update_exchange_rate(player, special_harbour: bool, resource_type: str = None):
        if special_harbour:
            for inner_dict in player.exchange_rate.values():
                inner_dict[resource_type] = 2
        else:
            for inner_dict in player.exchange_rate.values():
                keys = inner_dict.keys()
                for key in keys:
                    inner_dict[key] = 3

    ####### avavilable actions validation #######
    
    def can_build_road(player):
        """ Returns whether a player can build a road or not."""
        return True if len(player.available_roads) > 0 and player.resources.can_build(RESOURCE_REQUIREMENTS["road"]) else False
    
    def can_build_settlement(player):
        """Returns whether a player can build a settlement or not."""
        return True if len(player.available_settlements) > 0 and player.resources.can_build(RESOURCE_REQUIREMENTS["settlement"]) else False
    
    def has_resources(player):
        """Returns True if player has any resource to trade."""
        for amount in player.resources:
            if amount > 0:
                return True
        return False
    
    def can_upgrade_settlement(player):
        """Returns True if player has an un-upgraded settlement and
        enough resources to upgrade it."""

        # no sure if we upgrade a city, do we pop settlement out of built-settlement
        return True if player.resources.can_build(RESOURCE_REQUIREMENTS["city"]) and player.available_cities > 0 and player.built_settlements > 0 else False
    
    def can_buy_dev_card(player):
        """Returns True if player can afford a development card."""
        return True if player.resources.can_build(RESOURCE_REQUIREMENTS["development_card"]) else False
    
    def has_knight_card(player):
        """Returns True if player has a Knight card."""
        return True if player.development_cards["knight"] > 0 else False
    
    def has_road_building_card(player):
        """Returns True if player has a Road Building card."""
        return True if player.development_cards["road building"] > 0 else False
    
    def has_year_of_plenty_card(player):
        """Returns True if player has a Year of Plenty card."""
        return True if player.development_cards["year of plenty"] > 0 else False
    
    def has_monopoly_card(player):
        """Returns True if player has a Monopoly card."""
        return True if player.development_cards["monopoly"] > 0 else False
        
    def calculate_visable_victory_point(player):
        """ for each action, the game can update this, so that every players can view other players' VP in real time"""
        player.visible_victory_points = len(player.built_cities) * 2 + len(player.built_settlements) + 2 if player.game.check_longest_road() is player else 0 + 2 if player.game.check_largest_army is player else 0
        return player.visible_victory_points

    def calculate_total_victory_point(player):
        """ for each action, the game can update this, so that by the time player do an action to win, the game just ends"""
        return player.calculate_visable_victory_point + player.hidden_victory_points
        
class HumanPlayer(Player):

    def prompt_settlement_location(player, for_free=False):
        choice = None
        while not (choice in player.game.board.available_intersection_locations):
            choice = int(player.get("Pick a location to place a settlement: "))
        return choice

    def prompt_road_location(player, for_free=False):
        choice = None
        while not (choice in player.game.board.available_path_locations):
            choice = int(player.get("Pick a location to place a road: "))
        return choice

    def prompt_trade_details(player):
        """Called when user chooses to propose a trade.
        Prompts user for proposed trade details, verifies
        the trade is valid, then initiates proposed trade."""
        details = player.get('Enter trade details: ')
        
    def prompt_settlement_for_upgrade(player):
        """Called when user plays Road Building card.
        Prompts user for settlement they want to upgrade,
        then initiates upgrade"""
        choice = None
        choice = player.get('Choose a settlement: ')
        
    def prompt_knight(player):
        """Called when user plays Road Building card.
        Prompts user for tile they want to place the robber on,
        then initiates robbery."""
        choice = player.get('Pick a tile to place the robber on: ')
        
    def prompt_road_building(player):
        """Called when user plays Road Building card.
        Prompts user for the location of a path to build a road on,
        initiates the building of that road, then repeats this again for
        second road."""
        choice = player.get('Pick a location to place a road: ')
        
    def prompt_year_of_plenty(player):
        """Called when user plays Year of Plenty card.
        Prompts user for a resource type to get from bank,
        passes it to them, then repeats this again for second
        resource type."""
        choice1 = player.get('Pick a resource type: ')
        choice2 = player.get('Pick the second resource type: ')
        
    def prompt_monopoly(player):
        """Called when user plays Monopoly card.
        Prompts user for a resource type to steal from all players,
        then steals it for them."""
        choice = player.get('Pick a resource type: ')
        
    def sell_development_card(player):
        """Called when user chooses to buy a development card.
        Passes development card to them and prints out which card
        they got."""
        print('Congratulations, you got XXXXXXX')