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

    def __str__(self): return self.name.capitalize()

globals().update(ResourceKind.__members__)

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

    def __add__(self, other):  pass

    def __sub__(self, other):  pass

    def card_count(self) -> int:  return sum(self)

    def get_random_dev_card(self):
        no_of_cards = self.card_count()
        idx = randint(0, no_of_cards - 1)

        for i, dc in enumerate(self):
            if idx<dc: break
            else: idx-=dc

        q = DevelopmentCardKind(i)


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
            else: raise TypeError(f"Resources object can't be initialized with parameters {resources_spec}")
            
        elif len(resources_spec) == len(ResourceKind):
            super().__init__(dict(zip(ResourceKind,resources_spec)))
            
        else:
            raise TypeError(f"Resources object can't be initialized with parameters {resources_spec}")
        
    def __add__(self, other): return Resources(super().__add__(other))
    
    def __sub__(self, other):
        if not(self >= other): raise InsufficientResources()
        return Resources(super().__sub__(other))
    
    def __isub__(self, other): return self - other

    def __str__(self):
        if self == NO_RESOURCES: return "Nothing!"
        else: return ", ".join(f"{amount}x {kind}" for kind, amount in self.items() if amount > 0)


RESOURCE_REQUIREMENTS = {
    "road": Resources({brick:1, lumber:1}),
    "settlement": Resources({brick:1, lumber:1, wool:1, grain:1}),
    "city": Resources({ore:3, grain:2}),
    "development_card": Resources({ore:1, wool:1, grain:1}),
}

NO_RESOURCES = Resources()