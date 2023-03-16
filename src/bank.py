#!/usr/bin/env python3

from resources import (
    Resources,
    ResourceKind,
    RESOURCE_REQUIREMENTS,
    DevelopmentCardKind,
    InsufficientResources,
    DevelopmentCards,
)
from player import Player

DEFAULT_BANK_DEV_CARDS = DevelopmentCards(
    {
        DevelopmentCardKind.knight: 14,
        DevelopmentCardKind.hidden_victory_point: 5,
        DevelopmentCardKind.road_building: 2,
        DevelopmentCardKind.year_of_plenty: 2,
        DevelopmentCardKind.monopoly: 2,
    }
)

DEFAULT_BANK_RESOURCES = Resources(19, 19, 19, 19, 19)


class BankException(Exception):
    pass


class Bank:
    def __init__(self):
        self.development_cards = DEFAULT_BANK_DEV_CARDS.copy()
        self.resources = DEFAULT_BANK_RESOURCES.copy()
        self.color = "Bank"
    def __str__(self):
        return f"Bank(resources={self.resources}, development_cards={self.development_cards})"

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
        elif self.development_cards.total() <= 0:
            raise Exception("Bank is out of development cards")
        else:
            player.resources -= RESOURCE_REQUIREMENTS["development_card"]
            dev_card = self.development_cards.pop()
            player.development_cards += dev_card

    def distribute_dev_card(self):
        """pops a development card from the development card stack and returns it"""
        if self.development_cards.total() <= 0:
            raise BankException("Bank is out of development cards")
        return self.development_cards.pop()

    def accepts_trade(self, trade):
        if not (self.resources >= trade.resources_requested):
            return False

        single_kind_offered = trade.resources_offered.of_one_kind()
        if not single_kind_offered:
            return False

        single_kind_requested = trade.resources_requested.of_one_kind()
        if not single_kind_requested:
            return False

        if single_kind_offered == single_kind_requested:
            return False

        exchange_rate = trade.sender.exchange_rate[single_kind_requested][
            single_kind_offered
        ]
        amount_requested = trade.resources_requested.total()
        amount_offered = trade.resources_offered.total()

        return amount_requested * exchange_rate <= amount_offered
