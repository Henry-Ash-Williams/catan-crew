#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum

class ResourceCard(Enum):
    Brick = 0
    Lumber = 1
    Ore = 2
    Grain = 3
    Wool = 4

@dataclass
class Resources:
    brick: int = 0
    lumber: int = 0
    ore: int = 0
    grain: int = 0
    wool: int = 0

RESOURCE_REQUIREMENTS = {
    "road": Resources(brick=1, lumber=1),
    "settlement": Resources(brick=1, lumber=1, wool=1, grain=1),
    "city": Resources(ore=3, grain=2),
    "development_card": Resources(ore=1, wool=1, grain=1)
}
