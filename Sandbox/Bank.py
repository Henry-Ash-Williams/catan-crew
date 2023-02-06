#!/usr/bin/env python3
from Resources import Resources, ResourceCard

class Bank:

   def __init__(self, available: int = 19):
       self.available_resources = Resources(available, available, available, available, available)

   def distribute_brick(self, amount: int) -> ResourceCard:
       self.available_resources.brick -= amount
       return [ResourceCard.Brick] * amount

   def distribute_lumber(self, amount: int) -> ResourceCard:
       self.available_resources.lumber -= amount
       return [ResourceCard.Lumber] * amount

    def distribute_ore(self, amount: int) -> ResourceCard:
       self.available_resources.ore -= amount
       return [ResourceCard.Ore] * amount

    def distribute_grain(self, amount: int) -> ResourceCard:
        self.available_resources.grain -= amount
        return [ResourceCard.Grain] * amount

    def distribute_wool(self, amount: int) -> ResourceCard:
        self.available_resources.wool -= amount
        return [ResourceCard.Wool] * amount

   def return(self, cards: [ResourceCard])
