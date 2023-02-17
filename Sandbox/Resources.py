#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum


class ResourceKind(Enum):
    brick = 0
    lumber = 1
    ore = 2
    grain = 3
    wool = 4

    def __str__(self):
        return self.name.capitalize()


@dataclass
class DevelopmentCard:
    knight: int = 0
    hidden_victory_point: int = 0
    road_building: int = 0
    year_of_plenty: int = 0
    monopoly: int = 0

    def __iter__(self):
        return iter([self.knight, self.hidden_victory_point, self.road_building, self.year_of_plenty, self.monopoly])

    def card_count(self) -> int:
        return sum(self)


@dataclass(order=True)
class Resources:
    brick: int = 0
    lumber: int = 0
    ore: int = 0
    grain: int = 0
    wool: int = 0
    development_cards: DevelopmentCard = DevelopmentCard()

    def __add__(self, other):
        return Resources(
            self.brick + other.brick,
            self.lumber + other.lumber,
            self.ore + other.ore,
            self.grain + other.grain,
            self.wool + other.wool,
        )

    def __sub__(self, other):
        new_resources = Resources(
            self.brick - other.brick,
            self.lumber - other.lumber,
            self.ore - other.ore,
            self.grain - other.grain,
            self.wool - other.wool,
        )
        if any(map(lambda r: r < 0, new_resources)):
            raise Exception("Player cannot have negative resources")

        return new_resources

    def __iter__(self):
        # enables iteration over each resource in the class
        return iter([self.brick, self.lumber, self.ore, self.grain, self.wool])

    def can_build(self, building):
        return all(pr >= br for pr, br in zip(self, building))

    def __getitem__(self, key: str) -> int:
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
        else:
            raise Exception("Unrecognised resource")

    def __setitem__(self, key: str, new_value: int):
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

        for kind, amount in self.data_rep():
            if amount == 0:
                continue
            rep += f"{amount}x {kind.name}, "

        return rep


RESOURCE_REQUIREMENTS = {
    "road": Resources(brick=1, lumber=1),
    "settlement": Resources(brick=1, lumber=1, wool=1, grain=1),
    "city": Resources(ore=3, grain=2),
    "development_card": Resources(ore=1, wool=1, grain=1),
}
