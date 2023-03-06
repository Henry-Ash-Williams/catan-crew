#!/usr/bin/env python3

from dataclasses import dataclass

class Trade:
    def __init__(self, sender, resources_offered, resources_requested, proposees):
        self.sender = sender
        self.resources_offered = resources_offered
        self.resources_requested = resources_requested
        self.proposees = proposees
        self.accepters = []
