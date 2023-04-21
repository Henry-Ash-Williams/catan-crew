#!/usr/bin/env python3

import random

from board import *
from player import *
from human_player import HumanPlayer
from game import *
import unittest, pickle, random, sys

past_results = {"resource_distributions": [], "token_distributions": []}


class BoardTester(unittest.TestCase):
    def setUp(test):
        test.board = Board(size=3, seed=random.random())

    def test_init(test):
        test.assertTrue(type(test.board) is Board)

    def test_tile_count(test):
        """Make sure number of tiles match expected"""

        # Make sure total number of tiles is 37 (19 land + 18 sea)
        test.assertEqual(test.board.tile_count, 37)
        test.assertEqual(len(test.board.tiles), 37)

        # Make sure number of land tiles is 19
        test.assertEqual(test.board.land_tile_count, 19)

    def test_intersection_count(test):
        test.assertEqual(len(test.board.intersections), 37 * 2)

    def test_path_count(test):
        test.assertEqual(len(test.board.paths), 37 * 3)

    def test_directions(test):
        """Make sure directions are configured properly"""
        n = test.board.tile_count
        east, northeast, northwest, west, southwest, southeast = test.board.directions

        # Make sure if you make a step in two opposite directions you end up where you started
        test.assertEqual((east + west) % n, 0)
        test.assertEqual((northeast + southwest) % n, 0)
        test.assertEqual((northwest + southeast) % n, 0)

        # Make sure making a step east, then northwest, then southwest you end up where you started
        test.assertEqual((east + northwest + southwest) % n, 0)

    def test_resource_randomness(test):
        resource_tiles = filter(lambda t: type(t) is ResourceTile, test.board.tiles)
        resource_distribution = tuple([tile.resource for tile in resource_tiles])
        test.assertFalse(
            resource_distribution in past_results["resource_distributions"]
        )
        past_results["resource_distributions"].append(resource_distribution)

    def test_resource_type_count(test):
        resource_tiles = filter(lambda t: type(t) is ResourceTile, test.board.tiles)
        resources = tuple([tile.resource for tile in resource_tiles])
        test.assertEqual(resources.count(ResourceKind.grain), 4)
        test.assertEqual(resources.count(ResourceKind.wool), 4)
        test.assertEqual(resources.count(ResourceKind.lumber), 4)
        test.assertEqual(resources.count(ResourceKind.brick), 3)
        test.assertEqual(resources.count(ResourceKind.ore), 3)

    def test_number_token_randomness(test):
        resource_tiles = filter(lambda t: type(t) is ResourceTile, test.board.tiles)
        token_distribution = tuple([tile.number_token for tile in resource_tiles])
        test.assertFalse(token_distribution in past_results["token_distributions"])
        past_results["token_distributions"].append(token_distribution)

    def test_token_count(test):
        resource_tiles = filter(lambda t: type(t) is ResourceTile, test.board.tiles)
        tokens = tuple([tile.number_token for tile in resource_tiles])
        test.assertEqual(set(tokens), set([2, 3, 4, 5, 6, 8, 9, 10, 11, 12]))

    def tearDown(test):
        del test.board


if __name__ == "__main__":
    #    unittest.main()
    for iteration in range(1, 101):
        print("\n\n" + "[" * 20 + "  Test #%i  " % (iteration) + "]" * 20)
        wasSuccessful = unittest.main(exit=False).result.wasSuccessful()
        if not wasSuccessful:
            sys.exit(1)
