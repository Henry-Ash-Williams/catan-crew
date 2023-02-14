from Player import Player
from Resources import Resources

import unittest

class PlayerTester(unittest.TestCase):
    def setUp(self):
        self.p = Player("blue")

    def test_constructor(self):
        # TODO
        pass

    def test_available_builds(self):
        self.p.resources = Resources(brick=1, lumber=1)
        self.assertEqual(self.p.view_available_builds(), ["road"])
        self.p.resources += Resources(brick=1, lumber=1, wool=1, grain=1)
        self.assertEqual(self.p.view_available_builds(), ["road", "settlement"])
        self.p.resources = Resources(ore=3, grain=2)
        self.assertEqual(self.p.view_available_builds(), ["city"])


if __name__ == "__main__":
    unittest.main()
