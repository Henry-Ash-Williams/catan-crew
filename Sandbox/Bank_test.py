#!/usr/bin/env python3

from Resources import *
from Bank import *

import unittest


class BankTester(unittest.TestCase):
    def test_bank_distribution(self):
        bank = Bank()

        brick = bank.distribute_brick(3)

        # Ensure that the bank distributes the correct number of resources
        # and that the total resource tracker is updated accordingly
        self.assertEqual(brick, Resources(brick=3))
        self.assertEqual(bank.available_resources, Resources(16, 19, 19, 19, 19))

        lumber = bank.distribute_lumber(4)
        self.assertEqual(lumber, Resources(lumber=4))
        self.assertEqual(bank.available_resources, Resources(16, 15, 19, 19, 19))

        ore = bank.distribute_ore(1)
        self.assertEqual(ore, Resources(ore=1))
        self.assertEqual(bank.available_resources, Resources(16, 15, 18, 19, 19))

        grain = bank.distribute_grain(2)
        self.assertEqual(grain, Resources(grain=2))
        self.assertEqual(bank.available_resources, Resources(16, 15, 18, 17, 19))

        wool = bank.distribute_wool(3)
        self.assertEqual(wool, Resources(wool=3))
        self.assertEqual(bank.available_resources, Resources(16, 15, 18, 17, 16))

    def test_bank_return(self):
        bank = Bank(0)

        bank.return_to_bank(RESOURCE_REQUIREMENTS["settlement"])
        self.assertEqual(
            bank.available_resources, Resources(brick=1, lumber=1, wool=1, grain=1)
        )

        bank.return_to_bank(RESOURCE_REQUIREMENTS["settlement"])
        self.assertEqual(
            bank.available_resources, Resources(brick=2, lumber=2, wool=2, grain=2)
        )

        bank.return_to_bank(RESOURCE_REQUIREMENTS["road"])
        self.assertEqual(
            bank.available_resources, Resources(brick=3, lumber=3, wool=2, grain=2)
        )

        bank.return_to_bank(Resources(ore=4))
        self.assertEqual(
            bank.available_resources,
            Resources(brick=3, lumber=3, wool=2, grain=2, ore=4),
        )


if __name__ == "__main__":
    unittest.main()
