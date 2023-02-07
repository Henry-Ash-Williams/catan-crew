from Board import *
from Resources import Resources


class Player:

    def __init__(self, color):

        self.color = color

        self.free_settlements = [Settlement(self) for i in range(5)]
        self.free_cities = [City(self) for i in range(4)]
        # TODO: change this so the location of possible roads is accurate
        self.free_roads = [Road(0, self) for i in range(15)]

        self.built_settlements = []
        self.built_cities = []
        self.built_roads = []

        self.resources = Resources()


    def builds_settlement(self, location):

        if self.free_settlements:
            settlement = self.free_settlements.pop()
        else:
            raise Exception("Player has no available settlements to build")

        try:
            self.game.add_settlement(location, settlement)
            self.built_settlements.append(settlement)
        except Exception as e:
            self.free_settlements.append(settlement)
            raise e

    def builds_road(self, location):

        if self.free_roads:
            road = self.free_roads.pop()
        else:
            raise Exception("Player has no available roads to build")

        try:
            self.game.add_road(location, road)
            self.built_roads.append(road)
        except Exception as e:
            self.free_roads.append(road)
            raise e
    
    # TODO
    def request_trade(player, ):
        return ""

    def ends_turn(self):
        self.game.end_turn()
