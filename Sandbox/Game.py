from Bank import Bank
from Player import Player
from typing import Union


class Game:
    def __init__(self, board, players):
        self.board = board
        board.game = self
        self.turn_count = 0
        self.bank = Bank()

        requested_colors = set(p.color for p in players)
        if len(requested_colors) != len(players):
            raise Exception("More than one player have the same color")

        self.players = players
        self.player_number = 0
        
        for player in self.players:
            player.game = self
            player.number = self.player_number
            self.player_number += 1

        self.current_player_number = 0
        self.current_player = self.players[self.current_player_number]

        self.is_just_starting = True
        self.is_on = True

    def verify_current_player_is(self, player):
        if player != self.current_player:
            raise Exception(
                f"Player {player.color} can't play as it's {self.current_player.color}'s turn."
            )

    def begin_setup_phase(self, player_order):
        pass

    def end_setup_phase(self):
        pass

    def check_win_condition(self) -> bool:
        victory_points = [
            player.victory_points + player.hidden_victory_points
            for player in self.players
        ]
        win_status = [vp >= 10 for vp in victory_points]
        return any(win_status)

    def end_turn(self):
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
