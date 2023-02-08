#!/usr/bin/env python3
from Resources import *


class Bank:
    def __init__(self, available: int = 19):
        self.available_resources = Resources(
            available, available, available, available, available
        )

    # TODO: Maybe refactor the distribution functions so we don't have 5
    # practically identical functions
    def distribute(self, amount: int, resource_kind: ResourceKind) -> Resources:
        self.available_resources[resource_kind] -= amount
        r = Resources()
        r[resource_kind] = amount
        return r

    def distribute_brick(self, amount: int) -> Resources:
        """
        TODO: Idea for how to generalize these functions
        self.available_resources[resource_kind] -= amount
        r = Resources()
        r[resource_kind] = amonut
        return r"""
        self.available_resources.brick -= amount
        return Resources(brick=amount)

    def distribute_lumber(self, amount: int) -> Resources:
        self.available_resources.lumber -= amount
        return Resources(lumber=amount)

    def distribute_ore(self, amount: int) -> Resources:
        self.available_resources.ore -= amount
        return Resources(ore=amount)

    def distribute_grain(self, amount: int) -> Resources:
        self.available_resources.grain -= amount
        return Resources(grain=amount)

    def distribute_wool(self, amount: int) -> Resources:
        self.available_resources.wool -= amount
        return Resources(wool=amount)

    def return_to_bank(self, returned_resources: Resources):
        self.available_resources += returned_resources
