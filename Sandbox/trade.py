#!/usr/bin/env python3

# from Player import Player
# from Resources import Resources
from dataclasses import dataclass


# @dataj
# class Trade:
#    sender: Player
#    resources_offered: Resources
#    resources_requested: Resources
#    proposees: list[Player]
#    accepters: list[Player]


class Trade:
    def __init__(self, sender, resources_offered, resources_requested, proposees):
        self.sender = sender
        self.resources_offered = resources_offered
        self.resources_requested = resources_requested
        self.proposees = proposees
        self.accepters = []
