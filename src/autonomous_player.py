#!/usr/bin/env python3
from player import Player
from resources import Resources, ResourceKind
from trade import Trade
from board import Settlement, Tile

import random


class AutonomousPlayer(Player):
    def prompt_settlement_location(player, valid_settlement_locations):
        location = random.choice(valid_settlement_locations)
        # rich.print(f"{player} builds a settlement at location {location}")
        return location

    def prompt_road_location(player, valid_road_locations):
        location = random.choice(valid_road_locations)
        return location

    def prompt_trade_details(player):
        individual_resources = [Resources(kind) for kind in ResourceKind]
        resources_offered = random.choice(individual_resources)
        resources_requested = random.choice(individual_resources)
        other_players = [p for p in player.game.players if not (p is player)]
        proposees = random.sample(other_players, random.randint(1, len(other_players)))
        # rich.print(
        # f"{player} proposes a trade of {resources_offered} for {resources_requested} to {proposees}"
        # )
        return Trade(player, resources_offered, resources_requested, proposees)

    def accepts_trade(player, trade):
        if player.resources >= trade.resources_requested:
            decision = random.choice([True, False])
        else:
            decision = False
        # rich.print(
        # f"{player} {['rejects','accepts'][decision]} trade proposed by {trade.sender}"
        # )
        return decision

    def prompt_trade_partner(player, trade):
        chosen_trade_partner = random.choice(trade.accepters)
        # rich.print(f"{player} chooses to trade with {chosen_trade_partner}")
        return chosen_trade_partner

    def prompt_settlement_for_upgrade(player) -> Settlement:
        settlement = random.choice(player.built_settlements)
        # rich.print(f"{player} upgrades settlement at location {settlement.location}")
        return settlement

    def prompt_knight(player):
        options = player.game.board.tile_locations[:]
        options.remove(player.game.board.robber_location)
        chosen_location = random.choice(options)
        # rich.print(f"{player} places Knight at location {chosen_location}")
        return chosen_location

    def prompt_road_building(player):
        location = random.choice(player.game.board.valid_road_locations(player))
        # rich.print(f"{player} builds a road at location {location}")
        return location

    def prompt_robbing_victim(player, robbee_options: list[Player]) -> Player:
        robbing_victim = random.choice(robbee_options)
        # rich.print(f"{player} robs {robbing_victim}")
        return robbing_victim

    def prompt_robber_location(player) -> Tile:
        options = list(player.game.board.land_locations)
        # rich.print("Options:", options)
        # rich.print("Current robber location:", player.game.board.robber_location)
        options.remove(player.game.board.robber_location)
        tile_location = random.choice(options)
        # rich.print(f"{player} moves robber to location {tile_location}")
        return player.game.board.tiles[tile_location]

    def prompt_monopoly_resource(player) -> ResourceKind:
        choice = ResourceKind(random.randint(0, 4))
        # rich.print(f"{player} monopolizes {choice}")
        return choice

    def prompt_YoP_resource(player) -> ResourceKind:
        choice = ResourceKind(random.randint(0, 4))
        # rich.print(f"{player} uses Year of Plenty to get {choice} from the bank")
        return choice

    def prompt_action(player, action_labels):
        action_index = random.randint(0, len(action_labels) - 1)
        # rich.print(f"{player} chooses to ({action_labels[action_index]})")
        return action_index

    def prompt_resources_to_give_up(player):
        resources = player.resources.random_subset()
        while resources.total() > player.resources.total() // 2:
            resources = player.resources.random_subset()
        return resources
