#!/usr/bin/env python3

from Player import Player
from Resources import Resources
from dataclasses import dataclass
from typing import Union


@dataclass
class Trade:
    sender: Player
    proposeess: list[Player]
    resources_offered: Resources
    resources_requested: Resources
    accepters: list[Player]
