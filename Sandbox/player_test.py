from player import Player
from resources import Resources, ResourceKind
from board import Settlement

import unittest

# TODO: Update the player tester class to reflect current interface design


class PlayerTester(unittest.TestCase):
    def setUp(self):
        self.p = Player("blue")

    def test_constructor(self):
        self.assertEqual(self.p.color, "blue")
        self.assertEqual(len(self.p.available_settlements), 5)
        self.assertEqual(len(self.p.available_cities), 4)
        self.assertEqual(len(self.p.available_roads), 15)

        self.assertEqual(self.p.built_settlements, [])
        self.assertEqual(self.p.built_cities, [])
        self.assertEqual(self.p.built_roads, [])
        self.assertEqual(self.p.resources, Resources())

    def test_available_builds(self):
        self.p.resources = Resources({ ResourceKind.brick:1, ResourceKind.lumber:1 })
        self.assertEqual(self.p.view_available_builds(), ["road"])
        self.p.resources += Resources({ResourceKind.brick:1, ResourceKind.lumber:1, ResourceKind.wool:1, ResourceKind.grain:1})
        self.assertEqual(self.p.view_available_builds(), ["road", "settlement"])
        self.p.resources = Resources({ResourceKind.ore:3, ResourceKind.grain:2})
        self.assertEqual(self.p.view_available_builds(), ["city"])

    def test_has_resources(self):
        self.p.resources = Resources()
        self.assertFalse(self.p.has_resources())
        self.p.resources = Resources({ ResourceKind.brick:1, ResourceKind.lumber:1 })
        self.assertTrue(self.p.has_resources())

    def test_can_upgrade_settlement(self):
        self.p.resources = Resources()
        self.assertFalse(self.p.can_upgrade_settlement())
        self.p.resources = Resources({ ResourceKind.ore:3, ResourceKind.grain:2 })
        self.p.built_settlements.append(Settlement(self.p))
        self.assertTrue(self.p.can_upgrade_settlement())

    def test_can_buy_dev_card(self):
        self.p.resources = Resources()
        self.assertFalse(self.p.can_buy_dev_card())
        self.p.resources = Resources({ ResourceKind.ore:1, ResourceKind.wool:1, ResourceKind.grain:1 })
        self.assertTrue(self.p.can_buy_dev_card())


if __name__ == "__main__":
    unittest.main()
