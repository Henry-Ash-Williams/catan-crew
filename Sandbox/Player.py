from Board import *
from Resources import Resources


class Player:
<<<<<<< Updated upstream
    def __init__(self, color):
        self.color = color
=======

    def __init__(player, color):

        player.color = color
>>>>>>> Stashed changes

        player.free_settlements = [Settlement(player) for i in range(5)]
        player.free_cities = [City(player) for i in range(4)]
        # TODO: change this so the location of possible roads is accurate
        player.free_roads = [Road(0, player) for i in range(15)]

        player.built_settlements = []
        player.built_cities = []
        player.built_roads = []

        player.resources = Resources()

<<<<<<< Updated upstream
        self.resources = Resources()
        self.exchange_rate = (
            0  # TODO: defaultdict(defaultdict(int)) -> predefined exchange rate
        )

    def builds_settlement(self, location):
        if self.available_settlements:
            settlement = self.available_settlements.pop()
=======
    #def builds_settlement(player, location):
    #  player.game.board.add_settlement(location, player)

    #def builds_road(player, location):
    #  player.game.board.add_road(location, player)

    def builds_settlement(player, location):

        if player.free_settlements:
            settlement = player.free_settlements.pop()
>>>>>>> Stashed changes
        else:
            raise Exception("Player has no free settlements to build")

        try:
            player.game.add_settlement(location, settlement)
            player.built_settlements.append(settlement)
        except Exception as e:
            player.free_settlements.append(settlement)
            raise e

<<<<<<< Updated upstream
    def upgrade_settlement(self, location):
        # TODO
        return 0

    def builds_road(self, location):
        if self.available_roads:
            road = self.available_roads.pop()
=======
    def builds_road(player, location):

        if player.free_roads:
            road = player.free_roads.pop()
>>>>>>> Stashed changes
        else:
            raise Exception("Player has no free roads to build")

        try:
            player.game.add_road(location, road)
            player.built_roads.append(road)
        except Exception as e:
            player.free_roads.append(road)
            raise e
<<<<<<< Updated upstream

    # TODO
    def request_trade(
        player,
    ):
        return ""
=======
>>>>>>> Stashed changes

    def ends_turn(player):
        player.game.end_turn()
