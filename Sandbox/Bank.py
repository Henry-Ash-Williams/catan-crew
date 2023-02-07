#!/usr/bin/env python3
from Resources import Resources

class Bank:

   def __init__(self, available: int = 19):
      self.available_resources = Resources(available, available, available, available, available)

   def distribute_brick(self, amount: int) -> Resources:
      self.available_resources.brick -= amount
      return Resources(brick=amount)

   def distribute_lumber(self, amount: int) -> Resources:
      self.available_resources.lumber -= amount
      return Resources(lumber=amount)

   def distribute_ore(self, amount: int) -> Resources:
      self.available_resources.ore -= amount
      return Resources(ore=amount)

   def distribute_grain(self, amount: int) -> Resources:
      self.available_resources.grain -= amount
      return Resources(grain=amount)

   def distribute_wool(self, amount: int) -> Resources:
      self.available_resources.wool -= amount
      return Resources(wool=amount)

   def return_to_bank(self, returned_resources: Resources):
      self.available_resources += returned_resources
