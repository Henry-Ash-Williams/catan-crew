#!/usr/bin/env python3

from player import Player
from resources import Resources, ResourceKind
from trade import Trade
from board import Settlement, Tile
import rich


class HumanPlayer(Player):
    def prompt_settlement_location(player, valid_settlement_locations):
        choice = None
        rich.print(f"Valid settlement locations: {valid_settlement_locations}")
        while not (choice in valid_settlement_locations):
            choice = int(player.get("Pick a location to place a settlement: "))
        return choice

    def prompt_road_location(player, valid_road_locations):
        choice = None
        rich.print(f"Valid road locations: {valid_road_locations}")
        while not (choice in valid_road_locations):
            choice = int(player.get("Pick a location to place a road: "))
        return choice

    def prompt_resources(player, prompt_string) -> Resources:
        resources_requested_input = player.get(
            f"{prompt_string} in format {', '.join(ResourceKind.__members__)}: "
        )

        while True:
            try:
                return Resources(*eval(resources_requested_input))
            except Exception:
                resources_requested_input = player.get(
                    "That doesn't look right. Try again: "
                )

    def prompt_resources_to_give_up(player):
        rich.print(
            f"[b {player.color}]{player}[/b {player.color}]: you have {player.resources}"
        )
        resources = player.prompt_resources(
            f"[b {player.color}]{player}[/b {player.color}]: choose resources to give up"
        )
        return resources

    def prompt_trade_proposees(player) -> list[Player]:
        rich.print("You can propose this trade to:")
        other_players = [p for p in player.game.players if not (p is player)]

        for index, proposee in enumerate(other_players, 1):
            rich.print("%i. %s" % (index, proposee))

        prompt1 = "Who would you like to propose this trade to? "
        choices = [p.strip() for p in player.get(prompt1).split(",")]
        choices_are_numbers = all(p.isnumeric() for p in choices)

        if choices_are_numbers:
            numeric_choices = [int(choice) for choice in choices]
            choices_in_range = min(numeric_choices) > 0 and max(numeric_choices) <= len(
                other_players
            )

        while not (choices_are_numbers and choices_in_range):
            prompt2 = "That is not a valid selection of players. Try again: "
            choices = [p.strip() for p in player.get(prompt2).split(",")]
            choices_are_numbers = all([p.isnumeric() for p in choices])
            if choices_are_numbers:
                numeric_choices = [int(choice) for choice in choices]
                choices_in_range = min(numeric_choices) > 0 and max(
                    numeric_choices
                ) <= len(other_players)

        return [other_players[choice - 1] for choice in numeric_choices]

    def prompt_trade_details(player):
        """Called when user chooses to propose a trade.
        Prompts user for proposed trade details, verifies
        the trade is valid, then returns trade object."""

        resources_offered = player.prompt_resources("Enter resources you're offering")
        while not (player.resources >= resources_offered):
            resources_offered = player.prompt_resources(
                "You don't have that many resources. Try again:"
            )

        resources_requested = player.prompt_resources("Enter resources you want to get")
        while not (player.resources >= resources_offered):
            resources_offered = player.prompt_resources(
                "You don't have that many resources. Try again:"
            )

        proposees = player.prompt_trade_proposees()

        return Trade(
            sender=player,
            resources_offered=resources_offered,
            resources_requested=resources_requested,
            proposees=proposees,
        )

    def accepts_trade(player, trade):
        if player.resources >= trade.resources_requested:
            response = player.get(
                f"[b {player.color}]{player}[/b {player.color}]: would you like to accept this trade? (y/n) "
            )
            decision = True if response.lower() == "y" else False
        else:
            decision = False
        rich.print(
            f"[b {player.color}]{player}[/b {player.color}] {['rejects','accepts'][decision]} trade proposed by {trade.sender}"
        )
        return decision

    def prompt_trade_partner(player, trade):
        rich.print("\nYou can trade with:")
        for index, accepter in enumerate(trade.accepters, 1):
            rich.print(f"{index}. {accepter}")

        choice = int(player.get("Pick a trade partner: "))

        return trade.accepters[choice - 1]

    def prompt_settlement_for_upgrade(player) -> Settlement:
        """Called when the user chooses to upgrade a settlement.
        Prompts user for settlement they want to upgrade."""
        choice = None
        rich.print(
            f"Your settlements: {[settlement.location for settlement in player.built_settlements]}"
        )
        while not (
            choice in [settlement.location for settlement in player.built_settlements]
        ):
            choice = int(player.get("Pick one of your settlement to upgrade: "))
        return player.game.board.cells[choice].settlement

    def prompt_knight(player):
        """Called when user plays knight card.
        Prompts user for tile they want to place the robber on,
        then initiates robbery."""
        choice = None
        while not (choice in player.game.board.tile_locations):
            choice = player.get("Pick a tile to place the robber on: ")
        return choice

    def prompt_road_building(player):
        """Called when user plays Road_Building card.
        Prompts user for the location of a path to build a road on,
        initiates the building of that road, then repeats this again for
        second road."""
        # the reason why we don't return 2 chocie at the same time
        # is because we can build 1 road and build the next road next to the first road
        choice = None
        while not (choice in player.reachable_paths()):
            choice = int(player.get("Pick a location to place a road: "))
        return choice

    def prompt_robbing_victim(player, robbee_options: list[Player]) -> Player:
        """Prompts the player for a choice of other player to rob."""
        available_robbees = [
            (potential_robbee.color, potential_robbee)
            for potential_robbee in robbee_options
        ]

        rich.print("\nYou can rob:")
        for index, (color, robbee) in enumerate(available_robbees, 1):
            rich.print(f"{index}. {color}")

        choice = int(player.get("Who would you like to rob? ")) - 1

        return robbee_options[choice]

    def prompt_robber_location(player) -> Tile:
        """Prompts player for a location at which to place the robber."""
        rich.print("Pick a location at which to place the robber: ")
        chosen_tile_location = int(
            player.get(f"Valid locations: {player.game.board.land_locations}")
        )
        valid_tile = chosen_tile_location in player.game.board.land_locations
        robber_moved = chosen_tile_location != player.game.board.robber_location
        while not (valid_tile and robber_moved):
            if not robber_moved:
                chosen_tile_location = int(
                    player.get("The robber is already on that tile. Pick another: ")
                )
            elif not valid_tile:
                chosen_tile_location = int(
                    player.get(
                        "Sorry, that's not a valid tile location. Pick another: "
                    )
                )
            valid_tile = chosen_tile_location in player.game.board.land_locations
            robber_moved = chosen_tile_location != player.game.board.robber_location
        chosen_tile = player.game.board.tiles[chosen_tile_location]
        return chosen_tile

    def prompt_resource(player, prompt) -> ResourceKind:
        choice = player.get(prompt).lower()
        while choice not in ResourceKind.__members__:
            choice = player.get(
                "That is not a valid resource name. Try again: "
            ).lower()
        resource = ResourceKind(ResourceKind[choice])
        return resource

    def prompt_monopoly_resource(player) -> ResourceKind:
        return player.prompt_resource("Select a resource to monopolize: ")

    def prompt_YoP_resource(player) -> ResourceKind:
        return player.prompt_resource("Select a resource to get from bank: ")

    def prompt_action(player, action_labels):
        rich.print("\nYou can:")
        for index, action_label in enumerate(action_labels, 1):
            rich.print(f"{index}. {action_label}")
        return int(player.get("What would you like to do? ")) - 1
