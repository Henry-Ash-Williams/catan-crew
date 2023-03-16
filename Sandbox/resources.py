#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
from collections import Counter
from random import randint


class ResourceKind(Enum):
    brick = 0
    lumber = 1
    ore = 2
    grain = 3
    wool = 4

    def __str__(self):
        # return self.name.capitalize()
        return self.name

    def __repr__(self):
        return str(self)


globals().update(ResourceKind.__members__)


class DevelopmentCardKind(Enum):
    knight = 0
    hidden_victory_point = 1
    road_building = 2
    year_of_plenty = 3
    monopoly = 4


globals().update(DevelopmentCardKind.__members__)


class DevelopmentCards(Counter):
    def pop(self):
        total = self.total()
        if total == 0:
            raise IndexError("pop from empty stack of development cards")
        choice = randint(0, total - 1)
        for resource_kind in self:
            if choice < self[resource_kind]:
                self[resource_kind] -= 1
                return DevelopmentCards([resource_kind])
            else:
                choice -= self[resource_kind]

    def __str__(self):
        if self.total() == 0:
            return "Nothing!"
        elif self.total() == 1:
            return self.most_common()[0][0].name.replace("_", " ").title()
        else:
            return ", ".join(
                f"{amount}x {kind}" for kind, amount in self.items() if amount > 0
            )


class InsufficientResources(Exception):
    pass


class Resources(Counter):
    def __init__(self, *resources_spec):
        if len(resources_spec) == 0:
            super().__init__()

        elif len(resources_spec) == 1:
            if isinstance(resources_spec[0], ResourceKind):
                super().__init__(resources_spec)
            elif isinstance(resources_spec[0], dict):
                super().__init__(resources_spec[0])
            else:
                raise TypeError(
                    f"Resources object can't be initialized with parameters {resources_spec}"
                )

        elif len(resources_spec) == len(ResourceKind):
            super().__init__(dict(zip(ResourceKind, resources_spec)))

        else:
            raise TypeError(
                f"Resources object can't be initialized with parameters {resources_spec}"
            )

    def __add__(self, other):
        return Resources(super().__add__(other))

    def __sub__(self, other):
        if not (self >= other):
            raise InsufficientResources()
        return Resources(super().__sub__(other))

    def __isub__(self, other):
        return self - other

    def __str__(self):
        if self == NO_RESOURCES:
            return "Nothing!"
        else:
            return ", ".join(
                f"{amount}x {kind}" for kind, amount in self.items() if amount > 0
            )

    def of_one_kind(self):
        nonzero_kinds = [kind for kind in self if self[kind] > 0]
        if len(nonzero_kinds) != 1:
            return False
        return nonzero_kinds[0]

    def random_subset(self):
        return Resources({kind: randint(0, self[kind]) for kind in self})


RESOURCE_REQUIREMENTS = {
    "road": Resources({brick: 1, lumber: 1}),
    "settlement": Resources({brick: 1, lumber: 1, wool: 1, grain: 1}),
    "city": Resources({ore: 3, grain: 2}),
    "development_card": Resources({ore: 1, wool: 1, grain: 1}),
}

NO_RESOURCES = Resources()
