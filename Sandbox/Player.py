from Board import *
from Resources import Resources, RESOURCE_REQUIREMENTS
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from copy import copy


class Player:
    def __init__(player, color):
        player.color = color

        player.available_settlements = [Settlement(player) for i in range(5)]
        player.available_cities = [City(player) for i in range(4)]
        # TODO: change this so the location of possible roads is accurate
        player.available_roads = [Road(0, player) for i in range(15)]

        player.built_settlements = []
        player.built_cities = []
        player.built_roads = []

        # Victory point related
        player.road_length = 0
        player.knights_played = 0
        player.victory_points = 0
        player.hidden_victory_points = 0

        player.resources = Resources()
        player.development_cards = {
            "knight" : 0,
            "road building": 0,
            "year of plenty": 0,
            "monopoly" : 0
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
        player.GameMaster.dice_roll()

    def view_possible_devcard(self):
        t = Table(
            title="Available Development Card"
        )
        t.add_column("Dev Card")
        t.add_column("Count")
        t.add_row("Knight", str(self.development_cards["knight"]), style="#cb4154")
        t.add_row("Road Building", str(self.development_cards["road building"]), style="green4")
        t.add_row("Year of Plenty", str(self.development_cards["year of plenty"]), style="grey30")
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
        console.print(Columns([Panel(resource_table), Panel(building_table), Panel(devcard_table)]))

    def builds_settlement(player, location):
        # TODO: make this method subtract from player's resources
        if player.available_settlements:
            settlement = player.available_settlements.pop()
        else:
            raise Exception("Player has no available settlements to build")

        try:
            player.game.add_settlement(location, settlement)
            player.built_settlements.append((settlement, location))
        except Exception as e:
            player.available_settlements.append(settlement)
            raise e

    def upgrade_settlement(player, location):
        # TODO: make this method subtract from player's resources
        if player.available_cities:
            city = player.available_cities.pop()
        else:
            raise Exception("Player has no available cities to build")

        try:
            player.game.upgrade_settlement(location, city)
            player.built_cities.append(city)
        except Exception as e:
            player.available_settlements.append(city)
            raise e

    def builds_road(player, location):
        # TODO: make this method subtract from player's resources
        
        # shall these handel by gamemaster to look over to it
        # when gamemaster give options for player to choose
        
        if player.available_roads:
            road = player.available_roads.pop()
        else:
            raise Exception("Player has no available roads to build")

        try:
            player.game.add_road(location, road)
            player.built_roads.append(road)
        except Exception as e:
            player.available_roads.append(road)
            raise e

    def play_knight(player, location):
        # check dev card
        if player.development_cards["knight"] <= 0:
            raise Exception("Player has no available knight card to play")
        else:
            player.development_cards["knight"] -= 1
            player.GameMaster.play_knight(player, location)
            # TODO: need to check if location is valid or not

    def play_monopoly(player, resource_type: str):
        # check dev card
        if player.development_cards["monopoly"] <= 0:
            raise Exception("Player has no available monopoly card to play")
        else:
            player.development_cards["monopoly"] -= 1
            player.GameMaster.play_monopoly(player, resource_type)

    def play_year_of_plenty(player, resource1: str, resource2: str):
        # check dev card
        # FIXME: supply stacks means bank?
        if player.development_cards["year of plenty"] <= 0:
            raise Exception("Player has no available year of plenty card to play")
        else:
            player.development_cards["year of plenty"] -= 1
            player.GameMaster.play_monopoly(player, resource1, resource2)
    
    def play_road_building(player):
        # can place 2 roads immediately
        # check dev card
        if player.development_cards["road building"] <= 0:
            raise Exception("Player has no available road building card to play")
        else:
            player.development_cards["road building"] -= 1
            # TODO: return a list of location
            locations = player.GameMaster.play_road_building(player)
            print("The availalbe locations: ", locations)
            player.GameMaster.add_road(location1)
            player.GameMaster.add_road(location2)

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
            resources_offered, player.resources
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

    def update_exchange_rate(player, speical_harbour: bool, resource_type: str = None):
        if speical_harbour:
            for inner_dict in player.exchange_rate.values():
                inner_dict[resource_type] = 2
        else:
            for inner_dict in player.exchange_rate.values():
                keys = inner_dict.keys()
                for key in keys:
                    inner_dict[key] = 3
    
    def can_build_road(player): return True
    
    def can_build_settlement(player): return True
    
    def has_resources(player): return True
    
    def can_upgrade_settlement(player): return True
    
    def can_buy_dev_card(player): return True
    
    def has_knight_card(player): return True
    
    def has_road_building_card(player): return True
    
    def has_year_of_plenty_card(player): return True
    
    def has_monopoly_card(player): return True