#!/usr/bin/env python3

from resources import Resources, ResourceKind
from bank import *

import unittest


class BankTester(unittest.TestCase):
    def test_bank_distribution(self):

        brick = self.bank.distribute(3, ResourceKind.brick)

        self.assertEqual(brick, Resources({ResourceKind.brick:3}))
        self.assertEqual(self.bank.resources, Resources({ResourceKind.brick:16, ResourceKind.lumber:19, ResourceKind.ore:19, ResourceKind.grain:19, ResourceKind.wool:19}))

        lumber = self.bank.distribute(4, ResourceKind.lumber)
        self.assertEqual(lumber, Resources({ ResourceKind.lumber:4 }))
        self.assertEqual(self.bank.resources, Resources({ResourceKind.brick:16, ResourceKind.lumber:15, ResourceKind.ore:19, ResourceKind.grain:19, ResourceKind.wool:19}))

        ore = self.bank.distribute(1, ResourceKind.ore)
        self.assertEqual(ore, Resources({ ResourceKind.ore:1 }))
        self.assertEqual(self.bank.resources, Resources({ResourceKind.brick:16, ResourceKind.lumber:15, ResourceKind.ore:18, ResourceKind.grain:19, ResourceKind.wool:19}))

        grain = self.bank.distribute(2, ResourceKind.grain)
        self.assertEqual(grain, Resources({ ResourceKind.grain:2 }))
        self.assertEqual(self.bank.resources, Resources({ResourceKind.brick:16, ResourceKind.lumber:15, ResourceKind.ore:18, ResourceKind.grain:17, ResourceKind.wool:19}))

        wool = self.bank.distribute(3, ResourceKind.wool)
        self.assertEqual(wool, Resources({ ResourceKind.wool:3 }))
        self.assertEqual(self.bank.resources, Resources({ResourceKind.brick:16, ResourceKind.lumber:15, ResourceKind.ore:18, ResourceKind.grain:17, ResourceKind.wool:16}))

    def test_bank_return(self):
        self.bank = Bank()
        self.bank.resources = Resources()

        self.bank.return_resources(RESOURCE_REQUIREMENTS["settlement"])
        self.assertEqual(
            self.bank.resources, Resources({ ResourceKind.brick:1, ResourceKind.lumber:1, ResourceKind.wool:1, ResourceKind.grain:1 })
        )

        self.bank.return_resources(RESOURCE_REQUIREMENTS["settlement"])
        self.assertEqual(
            self.bank.resources, Resources({ ResourceKind.brick:2, ResourceKind.lumber:2, ResourceKind.wool:2, ResourceKind.grain:2 })
        )

        self.bank.return_resources(RESOURCE_REQUIREMENTS["road"])
        self.assertEqual(
            self.bank.resources, Resources({ ResourceKind.brick:3, ResourceKind.lumber:3, ResourceKind.wool:2, ResourceKind.grain:2 })
        )

        self.bank.return_resources(Resources({ ResourceKind.ore:4 }))
        self.assertEqual(
            self.bank.resources,
            Resources({ ResourceKind.brick:3, ResourceKind.lumber:3, ResourceKind.wool:2, ResourceKind.grain:2, ResourceKind.ore:4 }),
        )


if __name__ == "__main__":
    unittest.main()
