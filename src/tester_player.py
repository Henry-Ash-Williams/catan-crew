#!/usr/bin/env python3
from autonomous_player import AutonomousPlayer
from board import Settlement, City


class TesterPlayer(AutonomousPlayer):
    def upgrade_settlement(player, settlement: Settlement):
        settlement_location = settlement.intersection.location
        settlement_intersection = settlement.intersection

        assert settlement in player.built_settlements
        assert not (settlement in player.available_settlements)

        super().upgrade_settlement(settlement)

        assert not (settlement in player.built_settlements)
        assert settlement in player.available_settlements

        assert settlement_intersection.settlement
        assert type(settlement_intersection.settlement) is City

        new_city = settlement_intersection.settlement
        assert new_city.intersection.location == settlement_location
        assert new_city in player.built_cities
        assert not (new_city in player.available_cities)
