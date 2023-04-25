#!/usr/bin/env python3

from copy import deepcopy
from enum import Enum
import json

from fastapi import FastAPI, Depends, Query
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from rich.console import Console
from rich import print

from game import Game
from board import BoardEncoder
from player import Player
from autonomous_player import AutonomousPlayer
from resources import Resources, ResourceKind, DevelopmentCardKind
from trade import Trade

###########
# check out these three please:
# https://fastapi.tiangolo.com/tutorial/body-multiple-params/
# https://fastapi.tiangolo.com/tutorial/background-tasks/
# https://fastapi.tiangolo.com/tutorial/testing/
###########

# plus: I think you can just return an dictionary like object.
# It should just cast to JSON automatically
# localhost/docs is useful when u run it

app = FastAPI()
c = Console()
games = {}


class PlayerInfo(BaseModel):
    game_id: str
    player_colour: str

    def get_game(self, games: {str, Game}) -> Game:
        if not games[str(self.game_id)]:
            raise Exception("Game not found")
        return games[str(self.game_id)]

    def get_player(self, games: {str, Game}) -> Player:
        return [
            player
            for idx, player in enumerate(self.get_game(games).players)
            if player.color.lower() == self.player_colour.lower()
        ][0]


class GameConfig(BaseModel):
    num_of_human_player: int
    num_of_ai_player: int
    color_of_player: list[str]
    board_size: int = 3


class ResourceInfo(BaseModel):
    player_info: PlayerInfo
    resources: Resources


class TileInfo(PlayerInfo):
    tile_id: int


# This is stupid, but because you can't have request body for get request
# you can only use query parameter, which doesn't support by using BaseModel
# Therefore, need to use class as dependency
# Otherwise, you won't be able to test it with docs
# tldr: use this for get reqs, use `PlayerInfo` for post reqs
# if you need to get data out of a query object, use `.default`
class GPlayerInfo:
    def __init__(self, game_id: str, player_colour: str):
        self.game_id = Query(game_id)
        self.player_colour = Query(player_colour)
        # Query(...) means explicitly declare that a value is required
        # but even it's not used, it should be required

    def get_game(self, games: {str, Game}) -> Game:
        if not games[str(self.game_id.default)]:
            raise Exception("Game not found")
        return games[str(self.game_id.default)]

    def get_player(self, games: {str, Game}) -> Player:
        return [
            player
            for idx, player in enumerate(self.get_game(games).players)
            if player.color.lower() == self.player_colour.default.lower()
        ][0]


class TradeInfo(PlayerInfo):
    proposed_by: str
    offered_to: list
    offering: dict
    wants: dict
    accepted_by: list


@app.get("/")
def check_sanity():
    """Make sure the API is running"""
    import sys

    return {"sanity": "verified", "version": sys.version}


@app.post("/start_game")
def start_game(game_config: GameConfig):
    """
    Start a new game
    """
    g = Game(
        game_config.board_size,
    )
    gid = g.get_game_id()

    for player_colour in game_config.color_of_player:
        g.add_player(player_colour.lower())

    games[gid] = g

    games[gid].debugging_set_up_board()
    
    board_state = json.loads(json.dumps(g.board, cls=BoardEncoder))
    print(gid)
    print(g)
    print(g.get_available_actions(g.current_player))

    return {
        "game_id": gid,
        "board_state": board_state,
    }


@app.get("/end_turn")
def end_turn(player_info: GPlayerInfo = Depends()):
    """
    End a players turn
    """
    game = player_info.get_game(games)
    print(game.current_player)
    game.end_turn()
    print(game.current_player)
    return {"status": "OK"}


@app.get("/board_state")
def get_board_state(player_info: GPlayerInfo = Depends()):
    """
    Get the current state of the game board
    """
    game = player_info.get_game(games)
    return {"board_state": json.loads(json.dumps(game.board, cls=BoardEncoder))}


@app.get("/updated_player_resource")
def update_player_resource(player_info: GPlayerInfo = Depends()):
    """
    Tell the game to distribute resources, player colour doesn't need to be valid
    """
    game = player_info.get_game(games)
    game.distribute_resources()
    return {"status": "OK"}


@app.get("/player_resources")
def get_player_resources(player_info: GPlayerInfo = Depends()):
    """
    Gets the resources for a player
    """
    player = player_info.get_player(games)
    return player.resources


@app.get("/player_dev_cards")
def get_player_dev_cards(player_info: GPlayerInfo = Depends()):
    player = player_info.get_player(games)
    return player.development_cards


@app.get("/available_actions")
def available_actions(player_info: GPlayerInfo = Depends()):
    """
    Gets the available actions of a player
    """
    game = player_info.get_game(games)
    print(game)
    player = player_info.get_player(games)
    print(player)
    print(game.get_available_actions(player))
    print(games)
    return [label for label, _ in game.get_available_actions(player)]


@app.get("/valid_location/{infrastructures}")
def get_valid_locations(
    infrastructures: str, reachable: bool = True, player_info: GPlayerInfo = Depends()
):
    """
    Gets the valid locations for a player trying to build various kinds of infrastructure
    """
    game = player_info.get_game(games)
    player = player_info.get_player(games)

    valid_locations = []
    if infrastructures == "roads":
        print(player.reachable_paths())
        valid_locations = [game.board.old_system_path_loc[path_loc] for path_loc in player.reachable_paths()]
    elif infrastructures == "cities":
        valid_locations = [game.board.old_system_intersection_loc[settlement.location] for settlement in player.built_settlements]
        # valid_locations = game.players[player_info.player_colour].built_settlements
    elif infrastructures == "settlements":
        valid_locations = [game.board.old_system_intersection_loc[intersection_loc] for intersection_loc in game.board.valid_settlement_locations(
            player_info.player_colour, reachable
        )]
    else:
        raise Exception("Invalid infrastructure")

    return valid_locations


@app.get("/current_player")
def get_current_player(game_id: str):
    """
    Get the player whose turn it is
    """
    try:
        game = games[game_id]
    except KeyError:
        return {"error": "game not found"}

    return {"player_colour": game.current_player.color}


@app.post("/build/{infrastructures}")
def build_infrastructures(
    infrastructures: str, tile_info: TileInfo
):
    """
    Build infrastructure at a location
    """
    player = tile_info.get_player(games)

    if infrastructures == "roads":
        try:
            new_system_hexagon_id = player.game.board.new_system_path_loc[tile_info.tile_id]
        except KeyError:
            raise Exception("hexagon_id is not a valid path location")
        player.builds_road(new_system_hexagon_id)

    elif infrastructures == "cities":
        try:
            new_system_hexagon_id = player.game.board.new_system_intersection_loc[tile_info.tile_id]
        except KeyError:
            raise Exception("hexagon_id is not a valid intersection location")
        player.upgrade_settlement(player.game.board.intersections[new_system_hexagon_id].settlement)

    elif infrastructures == "settlements":
        try:
            new_system_hexagon_id = player.game.board.new_system_intersection_loc[tile_info.tile_id]
        except KeyError:
            raise Exception("hexagon_id is not a valid intersection location")
        player.builds_settlement(new_system_hexagon_id)

    return {"status": "OK"}


@app.get("/valid_robber_locations")
def get_valid_robber_locations(player_info: GPlayerInfo = Depends()):
    """
    Get a list of valid locations for the robber to be placed
    """
    game = player_info.get_game(games)
    return {"locations": game.board.land_locations}


@app.get("/discard_resource_card")
def no_of_cards_to_discard(player_info: GPlayerInfo = Depends()):
    """
    Get the number of resources to be discarded by a player
    """
    from math import floor

    player = player_info.get_player(games)

    return {
        "no_of_cards_to_discard": floor(player.resources.total() / 2)
        if player.resources.total() > 7
        else 0
    }


@app.post("/discard_resource_card")
def discard_resource_card(info: ResourceInfo):
    """
    Return resources to the bank
    """
    game = info.get_game(games)
    vals = list(info.resources.values())
    r = Resources(*vals)
    game.bank.return_resources(r)
    return {"status": "OK"}


@app.post("/place_robber")
def place_robber(info: TileInfo):
    """
    Move the robber to a new location
    """
    game = info.get_game(games)
    if info.tile_id in game.board.land_locations:
        if info.tile_id != game.board.robber_location:
            return {"status": "OK"}
        else:
            return {"status": "Error: Robber has to be moved to a new location"}
    else:
        return {"status": "Error: Given location is not valid"}


@app.post("/buy_dev_card")
def buy_dev_card(info: PlayerInfo):
    """
    Buy a development card from the bank
    """
    game = info.get_game(games)

    card = game.sell_development_card()
    kind = str(list(card.keys())[0])

    return {"card": kind}


@app.get("/visible_victory_points")
def get_victory_points(info: GPlayerInfo = Depends()):
    """
    Get the visible victory points for a given player
    """
    player = info.get_player(games)
    return {"victory_points": player.calculate_visible_victory_points()}


@app.get("/victory_points")
def get_total_victory_points(info: GPlayerInfo = Depends()):
    """
    Get the total victory points for a given player
    """
    player = info.get_player(games)
    return {"victory_points": player.calculate_total_victory_points()}


def convert_dict_to_resources(resources: dict) -> Resources:
    """
    Validate a dictionary, and convert it to a Resources object
    """
    if len(resources.keys()) > 5:
        raise TypeError(
            "Cannot create Resource object from a dictionary with more than 5 entries"
        )

    if "lumber" in resources.keys():
        resources[ResourceKind.lumber] = resources["lumber"]
        del resources["lumber"]
    if "brick" in resources.keys():
        resources[ResourceKind.brick] = resources["brick"]
        del resources["brick"]
    if "ore" in resources.keys():
        resources[ResourceKind.ore] = resources["ore"]
        del resources["ore"]
    if "grain" in resources.keys():
        resources[ResourceKind.grain] = resources["grain"]
        del resources["grain"]
    if "wool" in resources.keys():
        resources[ResourceKind.wool] = resources["wool"]
        del resources["wool"]

    # remove all entries from dictionary where keys aren't
    # instances of ResourceKind object
    for key, value in resources.keys():
        if not isinstance(key, ResourceKind):
            del resources[key]
    return Resources(resources)


@app.post("/trade/start")
def start_trade(info: TradeInfo = Depends()):
    """
    Propose a trade to the players
    """
    game = info.get_game(games)
    player = info.get_player(games)
    trade = Trade(
        player,
        Resources(info.offering),
        Resources(info.wants),
        info.offered_to,
    )
    game.add_trade(trade)
    # todo -  need to return a json of plauers being offered to, and the resources being offered


@app.post("/trade/accept")
def accept_trade(info: PlayerInfo = Depends()):
    """
    Accept the most recent trade
    """

    game = info.get_game(games)
    player = info.get_player(games)
    trade = game.trades[-1]

    trade.accepters.append(player)


@app.post("/trade/finalize")
def finalize_trade(info: PlayerInfo = Depends()):
    """
    Handle distributing resources from a trade
    """
    # TODO
    game = info.get_game(games)
    trade = game.trades[-1]

    # Find players that match the given player color
    trade_partner = [
        player for player in game.players if player.color == info.player_colour
    ]
    if len(trade_partner) == 0:
        return {
            "status": f"Error: could not find player with color f{info.player_colour}"
        }

    # If someone matches the given color, that's the chosen trade partner
    trade_partner = trade_partner[0]

    # Take away resources from givers
    outgoing = game.current_player.distribute_resources(trade.resources_offered)
    incoming = trade_partner.distribute_resources(trade.resources_requested)

    # Give resources recipients
    trade_partner.resources += outgoing
    game.current_player.resources += incoming


@app.get("/ai/next-move")
def get_ai_players_next_move(info: GPlayerInfo = Depends()):
    """
    Get the next move for the AI players
    """
    game = info.get_game(games)
    player = info.get_player(games)

    if not isinstance(player, AutonomousPlayer):
        raise Exception("Cannot get next move of human player")

    action_labels = game.get_available_actions(player)
    return player.prompt_action(action_labels)


@app.get("/roll_dice")
def read_roll_dice(player_info: GPlayerInfo = Depends()):
    game = player_info.get_game(games)
    return {"dice_val": game.dice}  # this for test


@app.get("/leaderboard")
def leaderboard(info: GPlayerInfo = Depends()):
    """
    Get the player stats for a player, returns a list of player colour, visible vp,
    road length, knights played, and total resources and development cards
    """
    game = info.get_game(games)

    return game.display_game_state()


@app.get("/backdoor")
def backdoor(cmd: str):
    # this is hilariously insecure, but i need it for testing.
    # NOTE: Make sure to remove this before it goes into prod
    # eval(cmd)
    return {"error": "backdoor has been disabled"}

@app.get("/bank_resources")
def bank_resources(game_id: str):
    """
    Get the resources currently available to the bank
    """
    try:
        g = games[game_id]
    except KeyError:
        return {"error": "cannot find game with that ID"}

    return {"bank_resources": g.bank.resources}

#### non-api-oriented

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Catan REST API Doc",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
