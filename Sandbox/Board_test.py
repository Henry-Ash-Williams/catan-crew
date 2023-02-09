#!/usr/bin/env python3

from Board import *
from Player import *
import unittest, pickle, random


class BoardTester(unittest.TestCase):

    def setUp(test):
      test.board = Board(seed=random.random())
      try:
        with open('BoardTestResults.pickle','rb+') as f:
          test.past_results = pickle.load(f)
      except FileNotFoundError:
        test.past_results = {'resource_distributions':[], 'token_distributions': []}

    def test_init(test):
      test.assertTrue(type(test.board)==Board)
    
    def test_harbor_count(test):
      test.assertEqual(len(test.board.harbors),18)
    
    def test_count_count(test):
      test.assertEqual(len(test.board.bridges),108)
    
    def test_tile_count(test):
      test.assertEqual(len(test.board.tiles),19)
    
    def test_intersection_count(test):
      test.assertEqual(len(test.board.intersections),54)
    
    def test_path_count(test):
      test.assertEqual(len(test.board.paths),72)
      
    def test_resource_randomness(test):
      tiles = [test.board.cells[location] for location in test.board.tiles]
      resource_distribution = tuple([tile.resource for tile in tiles])
      test.assertFalse(resource_distribution in test.past_results['resource_distributions'])
      test.past_results['resource_distributions'].append(resource_distribution)
      
    def test_resource_type_count(test):
      tiles = [test.board.cells[location] for location in test.board.tiles]
      resources = tuple([tile.resource for tile in tiles])
      test.assertEqual(resources.count(ResourceKind.Grain),4)
      test.assertEqual(resources.count(ResourceKind.Wool),4)
      test.assertEqual(resources.count(ResourceKind.Lumber),4)
      test.assertEqual(resources.count(ResourceKind.Brick),3)
      test.assertEqual(resources.count(ResourceKind.Ore),3)
      test.assertEqual(resources.count(None),1)
      
    def test_number_token_randomness(test):
      tiles = [test.board.cells[location] for location in test.board.tiles]
      token_distribution = tuple([tile.number_token for tile in tiles])
      test.assertFalse(token_distribution in test.past_results['token_distributions'])
      test.past_results['token_distributions'].append(token_distribution)
      
    def test_token_count(test):
      tiles = [test.board.cells[location] for location in test.board.tiles]
      tokens = tuple([tile.number_token for tile in tiles])
      test.assertEqual(set(tokens), set([None,2,3,4,5,6,8,9,10,11,12]))
      
    def test_add_road(test):
      test_player = Player('blue')
      for path_location in test.board.paths:
        test_road = Road(path_location, test_player)
        with test.assertRaises(PathBuildingException) as e:
          test.board.add_road(path_location, test_road)
      
    def tearDown(test):
      del test.board
      with open('BoardTestResults.pickle','wb+') as f:
        pickle.dump(test.past_results, f)


if __name__ == "__main__":
    unittest.main()
