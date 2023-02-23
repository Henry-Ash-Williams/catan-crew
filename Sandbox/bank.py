#!/usr/bin/env python3
import random
from resources import Resources, ResourceKind, RESOURCE_REQUIREMENTS, DevelopmentCardKind, InsufficientResources
from player import Player


class BankException(Exception): pass


class Bank:
    development_card_deck = []

    # In the standard board game, there are 19 of each resource card.
    def __init__(self, available: int = 19):
        self.resources = Resources(
            available, available, available, available, available
        )
        """self.development_card_deck = DevelopmentCard(
            tuple(DEVELOPMENT_CARD_COUNTS.values())
        )"""
        self.development_card_deck = (
            [DevelopmentCardKind.knight for i in range(14)]
            + [DevelopmentCardKind.hidden_victory_point for i in range(5)]
            + [DevelopmentCardKind.road_building for i in range(2)]
            + [DevelopmentCardKind.year_of_plenty for i in range(2)]
            + [DevelopmentCardKind.monopoly for i in range(2)]
        )
        random.shuffle(self.development_card_deck)
        self.color = "Bank"
        
    def __str__(self): return 'Bank'

    def distribute(self, amount: int, resource_kind: ResourceKind) -> Resources:
        r = Resources() if resource_kind == None else Resources(resource_kind)
        try:
            self.resources -= r
            return r
        except InsufficientResources:
            r[resource_kind] = self.resources[resource_kind]
            self.resources -= r
            return r

    def distribute_resources(self, resources: Resources) -> Resources:
        self.resources -= resources
        return resources


    def return_resources(self, returned_resources: Resources):
        self.resources += returned_resources

    def sell_development_card(self, player: Player):
        if not player.can_buy_dev_card():
            raise Exception("Player does not have resources to purchase dev card")
        elif len(self.development_card_deck) <= 0:
            raise Exception("Bank is out of development cards")
        else:
            player.resources -= RESOURCE_REQUIREMENTS["development_card"]
            dev_card = self.development_card_deck.pop().name.replace("_", " ")
            player.development_cards[dev_card] += 1

    def distribute_dev_card(self):
        """ pops a development card from the development card stack and returns it"""
        if not self.development_card_deck:
            raise BankException('Bank is out of development cards')
        return self.development_card_deck.pop()
        
    def accepts_trade(self, trade):
        # TODO
        # This is just some filler code that makes the bank always
        # accept the trade if they have the resources for it
        return self.resources >= trade.resources_requested
