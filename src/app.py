#!/usr/bin/env python3

from copy import deepcopy
from enum import Enum
import json

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from rich.console import Console
from rich import print

from game import Game
from board import BoardEncoder
from player import Player, PlayerEncoder
from autonomous_player import AutonomousPlayer
from resources import Resources, ResourceKind
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
            if player.color.lower() == self.player_colour.default.lower()
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
    return {"sanity": "verified"}

@app.post("/start_game")
def start_game(game_config: GameConfig):
    """
    Start a new game
    """
    g = Game(
        game_config.board_size,
    )
    gid = g.get_game_id()
    board_state = json.loads(json.dumps(g.board, cls=BoardEncoder))

    for player_colour in game_config.color_of_player:
        g.add_player(player_colour.lower())

    games[gid] = deepcopy(g)

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
    game.end_turn()
    return {"status": "OK"}


@app.get("/board_state")
def get_board_state(player_info: GPlayerInfo = Depends()):
    """
    Get the current state of the game board
    """
    game = player_info.get_game(games)
    return {"state": json.dumps(game.board, cls=BoardEncoder)}


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


@app.get("/available_actions")
def available_actions(player_info: GPlayerInfo = Depends()):
    """
    Gets the available actions of a player
    """
    game = player_info.get_game(games)
    player = player_info.get_player(games)

    return [label for label, _ in game.get_available_actions(player)]


@app.get("/valid_location/{infrastructures}")
def get_valid_locations(
    infrastructures: str,
    reachable: bool = True,
    player_info: GPlayerInfo = Depends()
):
    """
    Gets the valid locations for a player trying to build various kinds of infrastructure
    """
    game = player_info.get_game(games)
    player = player_info.get_player(games)

    valid_locations = []
    if infrastructures == "roads":
        valid_locations = player.reachable_paths()
    elif infrastructures == "cities":
        valid_locations = game.players[player_info.player_colour].built_settlements
    elif infrastructures == "settlements":
        valid_locations = game.board.valid_settlement_locations(
            player_info.player_colour, reachable
        )
    else:
        raise Exception("Invalid path")

    return valid_locations


@app.post("/build/{infrastructures}")
def build_infrastructures(
    hexagon_id: int, infrastructures: str, player_info: PlayerInfo
):
    """
    Build infrastructure at a location
    """
    player = player_info.get_player(games)

    if infrastructures == "roads":
        player.build_road(hexagon_id)
    elif infrastructures == "cities":
        player.upgrade_settlement(hexagon_id)
    elif infrastructures == "settlements":
        player.build_settlement(hexagon_id)

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

    return {"no_of_cards_to_discard": floor(player.resources.total() / 2) if player.resources.total() > 7 else 0}


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
    # game = info.get_game(games)
    # player = info.get_player(games)

    # no game.place_robber method ¯\_(ツ)_/¯
    return {"status": "TODO", "locations": []}


@app.post("/buy_dev_card")
def buy_dev_card(info: PlayerInfo):
    """
    Buy a development card from the bank
    """
    game = info.get_game(games)

    card = game.sell_development_card()

    return {"card": card}

@app.get("/visible_victory_points")
def get_victory_points(info: GPlayerInfo = Depends()):
    """
    Get the visible victory points for a given player
    """
    player = info.get_player(games)
    return { "victory_points": player.calculate_visible_victory_points() }

@app.get("/victory_points")
def get_total_victory_points(info: GPlayerInfo = Depends()):
    """
    Get the total victory points for a given player
    """
    player = info.get_player(games)
    return { "victory_points": player.calculate_total_victory_points() }

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
    for key,value in resources.keys():
        if not isinstance(key,ResourceKind):
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

    if len( trade.accepters ) == 1 and trade.accepters[-1] == "bank":

        pass
    elif len(trade.accepters) == 2:
        # handle trade with only one accepter
        pass
    else:
        # handle trade with more than one accepter
        pass

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

@app.get("/leaderboard")
def leaderboard(info: GPlayerInfo = Depends()):
    """
    Get the player stats for a player, returns a list of player colour, visible vp, total vp,
    road length, knights played, and total resources and development cards
    """
    game = info.get_game(games)
    player = info.get_player(games)

    stats = [ player_stats for player_stats in game.display_game_state() if player_stats[0] == player.color]

    return stats

@app.get("/backdoor")
def backdoor(cmd: str):
    """
    If this is visible then I've fucked up and I need to remove this method from prod
    """
    # this is hilariously insecure, but i need it for testing.
    # NOTE: Make sure to remove this before it goes into prod
    eval(cmd)
