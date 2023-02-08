#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum


class ResourceKind(Enum):
    Brick = 0
    Lumber = 1
    Ore = 2
    Grain = 3
    Wool = 4


@dataclass(order=True)
class Resources:
    brick: int = 0
    lumber: int = 0
    ore: int = 0
    grain: int = 0
    wool: int = 0

    def __add__(self, other):
        return Resources(
            self.brick + other.brick,
            self.lumber + other.lumber,
            self.ore + other.ore,
            self.grain + other.grain,
            self.wool + other.wool,
        )

    def __sub__(self, other):
        return Resources(
            self.brick - other.brick,
            self.lumber - other.lumber,
            self.ore - other.ore,
            self.grain - other.grain,
            self.wool - other.wool,
        )

    def __iter__(self):
        # enables iteration over each resource in the class
        return iter([self.brick, self.lumber, self.ore, self.grain, self.wool])

    def can_build(self, building):
        return all(pr >= br for pr, br in zip(self, building))

    def __getitem__(self, key: str) -> int:
        if key.lower() == "brick":
            return self.brick
        elif key.lower() == "lumber":
            return self.lumber
        elif key.lower() == "ore":
            return self.ore
        elif key.lower() == "grain":
            return self.grain
        elif key.lower() == "wool":
            return self.wool
        else:
            raise Exception("Unrecognised resource")


RESOURCE_REQUIREMENTS = {
    "road": Resources(brick=1, lumber=1),
    "settlement": Resources(brick=1, lumber=1, wool=1, grain=1),
    "city": Resources(ore=3, grain=2),
    "development_card": Resources(ore=1, wool=1, grain=1),
}
