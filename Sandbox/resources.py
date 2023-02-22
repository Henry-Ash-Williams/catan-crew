#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
from collections import Counter
from random import randint
from typing import Union

RESOURCE_NAMES = ["brick", "lumber", "ore", "grain", "wool"]


class DevelopmentCardKind(Enum):
    knight = 0
    hidden_victory_point = 1
    road_building = 2
    year_of_plenty = 3
    monopoly = 4


DEVELOPMENT_CARD_COUNTS = {
    DevelopmentCardKind.knight: 14,
    DevelopmentCardKind.hidden_victory_point: 5,
    DevelopmentCardKind.road_building: 2,
    DevelopmentCardKind.year_of_plenty: 2,
    DevelopmentCardKind.monopoly: 2,
}


@dataclass
class DevelopmentCard:
    knight: int = 0
    hidden_victory_point: int = 0
    road_building: int = 0
    year_of_plenty: int = 0
    monopoly: int = 0

    def __iter__(self):
        return iter(
            [
                self.knight,
                self.hidden_victory_point,
                self.road_building,
                self.year_of_plenty,
                self.monopoly,
            ]
        )

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def card_count(self) -> int:
        return sum(self)

    def get_random_dev_card(self):
        no_of_cards = self.card_count()
        idx = randint(0, no_of_cards - 1)

        for i, dc in enumerate(self):
            if idx<dc: break
            else: idx-=dc

        q = DevelopmentCardKind(i)








class ResourceKind(Enum):
    brick = 0
    lumber = 1
    ore = 2
    grain = 3
    wool = 4

    def __str__(self):
        return self.name.capitalize()


class InsufficientResources(Exception):
    pass


# ResourceTuple: TypeAlias = (int, int, int, int, int)


@dataclass  # (order=True)  This yields wrong results, replaced with
# comparison methods
class Resources:
    brick: int = 0
    lumber: int = 0
    ore: int = 0
    grain: int = 0
    wool: int = 0
    development_cards: DevelopmentCard = DevelopmentCard()

    # def __init__(self, resources: Union[ResourceKind, ()]):
    # if type( resources ) is ResourceKind:
    # pass
    # else:
    # super.__init__(resources)

    def __add__(self, other):
        return Resources(
            self.brick + other.brick,
            self.lumber + other.lumber,
            self.ore + other.ore,
            self.grain + other.grain,
            self.wool + other.wool,
            self.development_cards,
        )

    def __mul__(self, scalar: float):
        return Resources(
            self.brick * scalar,
            self.lumber * scalar,
            self.ore * scalar,
            self.grain * scalar,
            self.wool * scalar,
            self.development_cards,
        )

    def __sub__(self, other):
        new_resources = Resources(
            self.brick - other.brick,
            self.lumber - other.lumber,
            self.ore - other.ore,
            self.grain - other.grain,
            self.wool - other.wool,
            self.development_cards,
        )
        if any(map(lambda r: r < 0, new_resources)):
            raise InsufficientResources("Insufficient resources")

        return new_resources

    def __iter__(self):
        # enables iteration over each resource in the class
        return iter([self.brick, self.lumber, self.ore, self.grain, self.wool])

    def can_build(self, building):
        return all(pr >= br for pr, br in zip(self, building))

    def __getitem__(self, key: Union[str, ResourceKind]) -> int:
        if isinstance(key, ResourceKind):
            return self[key.name]

        key = key.lower()
        if key == "brick":
            return self.brick
        elif key == "lumber":
            return self.lumber
        elif key == "ore":
            return self.ore
        elif key == "grain":
            return self.grain
        elif key == "wool":
            return self.wool

    def __setitem__(self, key: Union[str, ResourceKind], new_value: int):
        if isinstance(key, ResourceKind):
            self[key.name] = new_value

        key = key.lower()
        if key == "brick":
            self.brick = new_value
        elif key == "lumber":
            self.lumber = new_value
        elif key == "ore":
            self.ore = new_value
        elif key == "grain":
            self.grain = new_value
        elif key == "wool":
            self.wool = new_value
        else:
            raise Exception("Unrecognised resource")

    def data_rep(self) -> list[(ResourceKind, int)]:
        return [
            (ResourceKind.brick, self.brick),
            (ResourceKind.lumber, self.lumber),
            (ResourceKind.ore, self.ore),
            (ResourceKind.grain, self.grain),
            (ResourceKind.wool, self.wool),
        ]

    def card_count(self) -> (int, int):
        return (sum(self), self.development_cards.card_count())

    def __str__(self):
        rep = ""
        if all(map(lambda r: r == 0, self)):
            return "Nothing!"

        rep = ", ".join(
            f"{amount}x {kind.name}" for kind, amount in self.data_rep() if amount > 0
        )

        return rep

    def counter(self):
        return Counter({r: self[r] for r in RESOURCE_NAMES})

    def __eq__(self, other):
        return self.counter() == other.counter()

    def __lt__(self, other):
        return self.counter() < other.counter()

    def __le__(self, other):
        return self.counter() <= other.counter()

    def __gt__(self, other):
        return self.counter() > other.counter()

    def __ge__(self, other):
        return self.counter() >= other.counter()


RESOURCE_REQUIREMENTS = {
    "road": Resources(brick=1, lumber=1),
    "settlement": Resources(brick=1, lumber=1, wool=1, grain=1),
    "city": Resources(ore=3, grain=2),
    "development_card": Resources(ore=1, wool=1, grain=1),
}
