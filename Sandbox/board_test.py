#!/usr/bin/env python3

from Board import *
from Player import *
from Game import *
import unittest, pickle, random, sys


class BoardTester(unittest.TestCase):
    def setUp(test):
        test.board = Board(seed=random.random())
        test.players = [Player(color) for color in ["red", "green", "blue", "purple"]]
        test.game = Game(test.board, test.players)
        try:
            with open("BoardTestResults.pickle", "rb+") as f:
                test.past_results = pickle.load(f)
        except FileNotFoundError:
            test.past_results = {
                "resource_distributions": [],
                "token_distributions": [],
            }

    def test_init(test):
        test.assertTrue(type(test.board) == Board)

    def test_harbor_count(test):
        test.assertEqual(len(test.board.harbor_locations), 18)

    def test_bridge_count(test):
        test.assertEqual(len(test.board.bridge_locations), 108)

    def test_tile_count(test):
        test.assertEqual(len(test.board.tile_locations), 19)

    def test_intersection_count(test):
        test.assertEqual(len(test.board.intersection_locations), 54)

    def test_path_count(test):
        test.assertEqual(len(test.board.path_locations), 72)

    def test_resource_randomness(test):
        tiles = [test.board.cells[location] for location in test.board.tile_locations]
        resource_distribution = tuple([tile.resource for tile in tiles])
        test.assertFalse(
            resource_distribution in test.past_results["resource_distributions"]
        )
        test.past_results["resource_distributions"].append(resource_distribution)

    def test_resource_type_count(test):
        tiles = [test.board.cells[location] for location in test.board.tile_locations]
        resources = tuple([tile.resource for tile in tiles])
        test.assertEqual(resources.count(ResourceKind.Grain), 4)
        test.assertEqual(resources.count(ResourceKind.Wool), 4)
        test.assertEqual(resources.count(ResourceKind.Lumber), 4)
        test.assertEqual(resources.count(ResourceKind.Brick), 3)
        test.assertEqual(resources.count(ResourceKind.Ore), 3)
        test.assertEqual(resources.count(None), 1)

    def test_number_token_randomness(test):
        tiles = [test.board.cells[location] for location in test.board.tile_locations]
        token_distribution = tuple([tile.number_token for tile in tiles])
        test.assertFalse(token_distribution in test.past_results["token_distributions"])
        test.past_results["token_distributions"].append(token_distribution)

    def test_token_count(test):
        tiles = [test.board.cells[location] for location in test.board.tile_locations]
        tokens = tuple([tile.number_token for tile in tiles])
        test.assertEqual(set(tokens), set([None, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]))

    def test_add_road(test):
        test_player = Player("blue")
        for path_location in test.board.path_locations:
            test_road = Road(path_location, test_player)
            with test.assertRaises(RoadBuildingException) as e:
                test.board.add_road(path_location, test_road)

    def test_tiles_with_token(test):
        test.assertEqual(
            [len(tiles) for tiles in test.board.tiles_with_token],
            [0, 0, 1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1],
        )
        for dice_roll in range(2, 13):
            for tile in test.board.tiles_with_token[dice_roll]:
                test.assertEqual(tile.number_token, dice_roll)

    def test_settlements_neighboring(test):
        test_player = Player("blue")
        settlement1 = Settlement(test_player)
        settlement2 = Settlement(test_player)
        test.board.add_settlement(46, settlement1, True)
        test.board.add_settlement(505, settlement2, True)
        neighboring = {
            location: test.board.settlements_neighboring(test.board.cells[location])
            for location in [0, 90, 42, 465]
        }
        test.assertEqual(list(map(len, neighboring.values())), [2, 1, 1, 0])

    def test_get_settlements_and_cities(test):
        target = {player: [] for player in test.players}
        for player in test.players:
            for i in range(2):
                settlement = Settlement(player)
                location = random.choice(
                    list(test.board.available_intersection_locations)
                )
                test.board.add_settlement(location, settlement, True)
                target[player].append(settlement)
        result = test.board.get_settlements_and_cities()
        for player in test.players:
            test.assertEqual(set(target[player]), set(result[player]))

    def test_available_settlements_paths(test):
        created_settlement_locations = []
        created_road_locations = []

        for player in test.players:
            intersection_location = random.choice(
                list(test.board.available_intersection_locations)
            )
            settlement = Settlement(player)
            test.board.add_settlement(intersection_location, settlement, True)
            created_settlement_locations.append(intersection_location)

            path_locations = test.board.select(
                intersection_location, 1, matching=test.board.has_path
            )
            path_location_sample = random.sample(
                path_locations, random.randint(1, len(path_locations))
            )
            for path_location in path_location_sample:
                test.board.add_road(path_location, Road(path_location, player))
                created_road_locations.append(path_location)

        unavailable_intersection_locations = list(
            set(
                join(
                    test.board.select(
                        intersection_location,
                        1,
                        (2,),
                        matching=test.board.has_intersection,
                    )
                    for intersection_location in created_settlement_locations
                )
            )
        )
        unavailable_intersection_locations += created_settlement_locations
        unavailable_intersection_locations = list(
            set(unavailable_intersection_locations)
        )

        # print(created_settlement_locations)
        # print(unavailable_intersection_locations)
        # print(set(test.board.intersection_locations) - (set(unavailable_intersection_locations)|set(test.board.available_intersection_locations)))

        test.assertEqual(len(created_settlement_locations), len(test.players))
        test.assertTrue(
            len(test.players) <= len(created_road_locations) <= 3 * len(test.players)
        )
        test.assertEqual(
            len(
                set(unavailable_intersection_locations)
                | set(test.board.available_intersection_locations)
            ),
            len(test.board.intersection_locations),
        )
        test.assertEqual(
            len(
                set(unavailable_intersection_locations)
                & set(test.board.available_intersection_locations)
            ),
            0,
        )
        test.assertEqual(
            len(set(created_road_locations) | set(test.board.available_path_locations)),
            len(test.board.path_locations),
        )
        test.assertEqual(
            len(set(created_road_locations) & set(test.board.available_path_locations)),
            0,
        )

    def test_bridge_count(test):
        bridge_count = 0

        for intersection_location in test.board.intersection_locations:
            intersection = test.board.cells[intersection_location]
            if intersection.has_harbor:
                bridge_count += len(intersection.harbors)

        test.assertEqual(bridge_count, 18)

    def tearDown(test):
        del test.board
        with open("BoardTestResults.pickle", "wb+") as f:
            pickle.dump(test.past_results, f)


if __name__ == "__main__":
    #    unittest.main()
    for iteration in range(1, 101):
        print("\n\n" + "[" * 20 + "  Test #%i  " % (iteration) + "]" * 20)
        wasSuccessful = unittest.main(exit=False).result.wasSuccessful()
        if not wasSuccessful:
            sys.exit(1)