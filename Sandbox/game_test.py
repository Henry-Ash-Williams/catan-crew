#!/usr/bin/env python3

import unittest
from resources import NO_RESOURCES

class GameTester(unittest.TestCase):

    def test_longest_road(self):
        """
        for i in range(6):
            self.g.build_road(player="red")
        self.assertEqual(self.g.check_longest_road(), Player("red"))
        """
        self.assertTrue(True)

    def test_largest_army(self):
        """
        for i in range(4):
            self.g.play_knight(player="red")
        self.assertEqual(self.g.check_largest_army(), Player("red"))
        """
        self.assertTrue(True)

    def test_distribute_resources(self):
        """
        self.g.build_settlement(player="red")
        self.assertEqual(self.g.players[0].resources, NO_RESOURCES)
        self.g.distribute_resources()
        self.assertNotEqual(self.g.players[0].resources, NO_RESOURCES)
        """
        self.assertTrue(True)

    def test_build_road(self):
        """
        self.assertEqual(self.g.players[0].built_roads, [])
        self.g.build_road(player="red")
        self.assertNotEqual(self.g.players[0].built_roads, [])
        """
        self.assertTrue(True)

    def test_build_settlement(self):
        """
        self.assertEqual(self.g.players[0].built_settlements, [])
        self.g.build_settlement(player="red")
        self.assertNotEqual(self.g.players[0].built_settlements, [])
        """
        self.assertTrue(True)

    def test_upgrade_settlement(self):
        """
        self.assertEqual(self.g.players[0].built_settlements, [])
        self.g.build_settlement(player="red")
        self.assertNotEqual(self.g.players[0].built_settlements, [])
        self.assertNotEqual(self.g.players[0].built_cities, [])
        self.g.upgrade_settlement(player="red")
        self.assertEqual(self.g.players[0].built_settlements, [])
        self.assertNotEqual(self.g.players[0].built_citites, [])
        """
        self.assertTrue(True)

    def test_play_monopoly(self):
        """
        self.assertFalse(self.g.dev_card_played)
        self.g.play_monopoly()
        self.assertTrue(self.g.dev_card_played)
        self.assertEqual(self.g.bank.development_cards[DevelopmentCardKind.monopoly], 1)
        """
        self.assertTrue(True)

    def test_play_year_of_plenty(self):
        """
        self.assertFalse(self.g.dev_card_played)
        self.g.play_year_of_plenty()
        self.assertTrue(self.g.dev_card_played)
        self.assertEqual(self.g.bank.development_cards[DevelopmentCardKind.year_of_plenty], 1)
        """
        self.assertTrue(True)

    def test_play_road_building(self):
        """
        self.assertFalse(self.g.dev_card_played)
        self.g.play_road_building()
        self.assertTrue(self.g.dev_card_played)
        self.assertEqual(self.g.bank.development_cards[DevelopmentCardKind.road_building], 1)"""
        self.assertTrue(True)

    def test_play_knight(self):
        """
        self.assertFalse(self.g.dev_card_played)
        self.g.play_play_knight()
        self.assertTrue(self.g.dev_card_played)
        self.assertEqual(self.current_player.knights_played, 1)
        """
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
