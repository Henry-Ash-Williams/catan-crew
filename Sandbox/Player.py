from Board import *
from Resources import Resources


class Player:
    def __init__(self, color):
        self.color = color

        self.available_settlements = [Settlement(self) for i in range(5)]
        self.available_cities = [City(self) for i in range(4)]
        # TODO: change this so the location of possible roads is accurate
        self.available_roads = [Road(0, self) for i in range(15)]

        # built
        self.built_settlements = []
        self.built_cities = []
        self.built_roads = []

        # Victory point related
        self.road_length = 0
        self.knights_played = 0
        self.victory_points = 0

        self.resources = Resources()
        self.exchange_rate = (
            0  # TODO: defaultdict(defaultdict(int)) -> predefined exchange rate
        )

    def builds_settlement(self, location):
        if self.available_settlements:
            settlement = self.available_settlements.pop()
        else:
            raise Exception("Player has no available settlements to build")

        try:
            self.game.add_settlement(location, settlement)
            self.built_settlements.append(settlement)
        except Exception as e:
            self.available_settlements.append(settlement)
            raise e

    def upgrade_settlement(self, location):
        # TODO
        return 0

    def builds_road(self, location):
        if self.available_roads:
            road = self.available_roads.pop()
        else:
            raise Exception("Player has no available roads to build")

        try:
            self.game.add_road(location, road)
            self.built_roads.append(road)
        except Exception as e:
            self.available_roads.append(road)
            raise e

    # TODO
    def request_trade(
        player,
    ):
        return ""

    def ends_turn(self):
        self.game.end_turn()
