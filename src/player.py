from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel

import rich
import json

from board import Settlement, City, Road

from resources import (
    Resources,
    RESOURCE_REQUIREMENTS,
    ResourceKind,
    NO_RESOURCES,
    brick,
    lumber,
    ore,
    grain,
    wool,
    DevelopmentCards,
    knight,
    hidden_victory_point,
    road_building,
    year_of_plenty,
    monopoly,
)


def join(ll):
    return [i for k in ll for i in k]


class PlayerException(Exception):
    pass


class Player:
    def __init__(player, color, getter=None):
        player.game = None
        player.color = color
        player.get = getter if getter else input

        player.available_settlements = [Settlement(player) for i in range(5)]
        player.available_cities = [City(player) for i in range(4)]
        player.available_roads = [Road(player) for i in range(15)]

        player.built_settlements = []
        player.built_cities = []
        player.built_roads = []

        # TODO: calculate actual road length
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
            justify="center",
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
        city.intersection = settlement.intersection
        player.built_cities.append(city)

        player.built_settlements.remove(settlement)
        settlement.intersection = None
        player.available_settlements.append(settlement)

        city.intersection.settlement = city

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
        player.road_length += 1

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
        adjacent_to_settlement = join(
            settlement.neighboring_paths() for settlement in player.built_settlements
        )
        adjacent_to_city = join(
            city.neighboring_paths() for city in player.built_cities
        )
        adjacent_to_road = join(
            road.potential_expansions() for road in player.built_roads
        )
        paths = (
            set(adjacent_to_settlement) | set(adjacent_to_city) | set(adjacent_to_road)
        )
        paths &= player.game.board.land_paths
        path_locations = {path.location for path in paths}
        return list(path_locations & player.game.board.available_path_locations)

    ####### avavilable actions validation #######

    def can_build_road(player):
        """Returns whether a player can build a road or not."""
        if len(player.reachable_paths()) < 1:
            return False
        return (
            len(player.available_roads) > 0
            and player.resources >= RESOURCE_REQUIREMENTS["road"]
        )

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
        while (
            not (player.resources >= resources)
            or resources.total() < player.resources.total() // 2
        ):
            if not (player.resources >= resources):
                player.message("That's more than you have. Try again.")
                resources = player.prompt_resources_to_give_up()
            else:
                player.message(
                    f"You're giving up {resources.total()} "
                    + f"resource cards but the minimum is {player.resources.total()//2}. Try again"
                )
                resources = player.prompt_resources_to_give_up()
        rich.print()
        return resources

    def to_json(self):
        return { "colour": self.color, "built_settlements": self.built_settlements, "built_roads": self.built_roads, \
                 "road_length": self.road_length, "knights_played": self.knights_played, "resources": self.resources, \
                 "development_cards": self.development_cards + self.new_dev_cards, "proposed_trades": self.proposed_trades }

class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.to_json()
