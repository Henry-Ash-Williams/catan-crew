#!/usr/bin/env python3

from Game import Game
from Player import Player
from Bank import Bank
from Trade import Trade

ROAD_LENGTH_THRESHOLD = 5
ARMY_SIZE_THRESHOLD = 3


class GameMaster:
    def __init__(self, game):
        self.game = game
        self.bank = game.bank

    def check_longest_road(self) -> Player:
        player = max(self.game.players, key=lambda player: player.road_length)
        return player if player.road_length > ROAD_LENGTH_THRESHOLD else None

    def check_largest_army(self) -> Player:
        player = max(self.game.players, key=lambda player: player.knights_played)
        return player if player.knights_played > ARMY_SIZE_THRESHOLD else None

    def distribute_resources(self, roll: int):
        tiles = self.game.board.tiles_with_token[roll]
        for tile in tiles:
            neighboring_settlements = self.game.board.settlements_neighboring(tile)
            for settlement in neighboring_settlements:
                new_resource = self.bank.distribute(
                    settlement.distribution_rate, tile.resource
                )
                settlement.owner.resources += new_resource

    def handle_trade(self, trade: Trade):
        pass
