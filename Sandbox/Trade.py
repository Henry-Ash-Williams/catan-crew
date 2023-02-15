#!/usr/bin/env python3

from Player import Player
from Resources import Resources
from dataclasses import dataclass


@dataclass
class Trade:
    sender: Player
    proposees: list[Player]
    resources_offered: Resources
    resources_requested: Resources
    accepters: list[Player]

    def __init__(self):
        self.proposees = []
        super() #