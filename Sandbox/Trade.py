#!/usr/bin/env python3

from Bank import Bank
from Player import Player
from Resources import Resources
from dataclasses import dataclass
from typing import Union


@dataclass
class Trade:
    sender: Union[Player, Bank]
    recipient: Player
    resources_offered: Resources
    resources_requested: Resources
