#!/usr/bin/env python3

import unittest
from resources import Resources, ore, brick, lumber, grain, wool, InsufficientResources, RESOURCE_REQUIREMENTS

class ResourcesTester(unittest.TestCase):
    def setUp(self):
        self.r = Resources({ore: 1, brick: 1, lumber: 1, grain: 1, wool: 1 })

    def test_init(self):
        """
        Check that the conuter initialised correctly
        """
        self.assertEqual(self.r[ore], 1)
        self.assertEqual(self.r[brick], 1)
        self.assertEqual(self.r[lumber], 1)
        self.assertEqual(self.r[grain], 1)
        self.assertEqual(self.r[wool], 1)

    def test_add(self):
        """
        Check that adding two Resources objects is handled correctly
        """
        new_r = self.r + Resources({ore: 1, lumber: 2})
        self.assertEqual(new_r[ore], 2)
        self.assertEqual(new_r[lumber], 3)

    def test_sub(self):
        """
        Check that subtracting two Resources objects is handled correctly
        """
        new_r = self.r - Resources({ore: 1, lumber: 1})
        self.assertEqual(new_r[ore], 0)
        self.assertEqual(new_r[lumber], 0)

        # verify that an exception is raised when attempting to subtracting a
        # Resource object with more resources than the other
        with self.assertRaises(InsufficientResources):
            self.r - Resources({ore: 2, lumber: 2})

    def test_comparisons(self):
        self.assertTrue(self.r > RESOURCE_REQUIREMENTS["settlement"]) # Can build settlement
        self.assertFalse(self.r <= RESOURCE_REQUIREMENTS["city"])




if __name__ == "__main__":
    unittest.main()
