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
