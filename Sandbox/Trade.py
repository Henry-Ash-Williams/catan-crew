#!/usr/bin/env python3

from Player import Player
from Resources import Resources
from dataclasses import dataclass


@dataclass
class Trade:
    sender: Player
    recipient: Player
    resources_offered: Resources
    resources_requested: Resources
