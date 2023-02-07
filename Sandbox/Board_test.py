#!/usr/bin/env python3

from Board import *
import unittest

class BoardTester(unittest.TestCase):
    # Read the serialized board from disk and store it in a member variable,
    # `self.board` will always be available for use throughout the testing
    # suite
    def setUp(self):
        self.board = Board.read_state("board.pickle")

    def test_init(self):
        print(self.board)


if __name__ == "__main__":
    unittest.main()
