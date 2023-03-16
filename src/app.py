#!/usr/bin/env python3

from copy import deepcopy
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from rich.console import Console

from game import Game
from player import Player
from resources import Resources

###########
# check out these three please:
# https://fastapi.tiangolo.com/tutorial/body-multiple-params/
# https://fastapi.tiangolo.com/tutorial/background-tasks/
# https://fastapi.tiangolo.com/tutorial/testing/
###########

# plus: I think you can just return an dictionary like object.
# It should just caGt to JSON automatically
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


class GameConfig(BaseModel):
    num_of_human_player: int
    num_of_ai_player: int
    color_of_player: list[str]
    board_size: int = 3


class ResourceInfo(PlayerInfo):
    resources: Resources

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
        if not games[str(self.game_id)]:
            raise Exception("Game not found")
        return games[str(self.game_id)]

    def get_player(self, game: Game, games: {str, Game}) -> Player:
        return [
            player
            for idx, player in enumerate(self.get_game(games).players)
            if player.color.lower() == self.player_colour.default.lower()
        ][0]


@app.get("/")
def hello_word():
    return {"hello": "world"}


@app.post("/add_player")
def create_player(player: PlayerInfo):
    player \
        .get_game(player.game_id.default, games) \
        .add_player(player.player_colour)

    return {"player": games[player.game_id].players[-1]}

@app.post("/start_game")
def start_game(game_config: GameConfig):
    g = Game(
        num_of_human_players=game_config.num_of_ai_player,
        num_of_ai_player=game_config.num_of_ai_player,
        color_of_player=game_config.color_of_player,
        board_size=game_config.board_size,
    )
    gid = g.get_game_id()
    board_state = g.board.to_json()

    for player_colour in game_config.color_of_player:
        g.add_player(player_colour.lower())

    games[gid] = deepcopy(g)

    return {
        "game_id": gid,
        "board_state": board_state,
    }


@app.get("/dump_games")
def dump_games():
    print(games)
    return {"status": "OK"}



@app.get("/roll_dice")
def read_roll_dice(player_info: GPlayerInfo = Depends()):
    return {player_info.game_id, player_info.player_colour}  # this for test


@app.get("/end_turn")
def end_turn(player_info: GPlayerInfo = Depends()):
    game = player_info.get_game(games)
    game.end_turn()
    return {"status": "OK"}


@app.get("/board_state")
def get_board_state(player_info: GPlayerInfo = Depends()):
    game = player_info.get_game(games)
    return str(game.board.to_json())


@app.get("/updated_player_resource")
def update_player_resource(player_info: GPlayerInfo = Depends()):
    game = player_info.get_game(games)
    game.distribute_resources()
    return { "status": "OK" }


@app.get("/player_resources")
def get_player_resources(player_info: GPlayerInfo = Depends()):
    player = player_info.get_player(games)
    return player.resources


@app.get("/available_actions")
def available_actions(player_info: GPlayerInfo = Depends()):
    game = player_info.get_game(games)
    player = player_info.get_player(games)

    actions = []

    if player.has_resources():
        actions.append("trade")

    if player.can_build_road():
        actions.append("build_road")

    if player.can_build_settlement():
        actions.append("build_settlement")

    if player.can_upgrade_settlement():
        actions.append("upgrade_settlement")

    if player.can_buy_dev_card():
        actions.append("buy_dev_card")

    if (not game.dev_card_played) and player.has_knight_card():
        actions.append("play_knight")

    if (not game.dev_card_played) and player.can_play_road_building():
        actions.append("play_road_building")

    if (not game.dev_card_played) and player.has_year_of_plenty_card():
        actions.append("play_year_of_plenty")

    if (not game.dev_card_played) and player.has_monopoly_card():
        actions.append("play_monopoly")

    actions.append("end_turn")
    return actions


@app.get("/valid_location/{infrastructures}")
def get_valid_locations(
    infrastructures: str, reachable: bool = None, player_info: GPlayerInfo = Depends()
):
    game = player_info.get_game(games)
    valid_locations = []
    if infrastructures == "roads":
        valid_locations = ["TODO: idk how to get the road locations"]
    elif infrastructures == "cities":
        valid_locations = game.players[player_info.player_colour].built_settlements
    elif infrastructures == "settlements" and (reachable is not None):
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
    game = player_info.get_game(games)
    player = player_info.get_player

    if infrastructures == "roads":
        player.build_road(hexagon_id)
    elif infrastructures == "cities":
        player.upgrade_settlement(hexagon_id)
    elif infrastructures == "settlements":
        player.build_settlement(hexagon_id)

    return { "status": "OK" }

@app.get("/valid_robber_locations")
def get_valid_robber_locations(player_info: GPlayerInfo = Depends()):
    game = player_info.get_game(games)
    return { "locations": game.board.land_locations }

@app.get("/discard_resource_card")
def no_of_cards_to_discard(player_info: GPlayerInfo = Depends()):
    from math import floor
    game = player_info.get_game(games)
    player = player_info.get_player(games)

    return {"no_of_cards_to_discard": floor(player.resources.total() / 2) if player.resources.total() > 7 else 0 }


@app.post("/discard_resource_card")
def discard_resource_card(info: ResourceInfo):
    game = info.get_game(games)
    vals = list(info.resources.values())
    r = Resources(*vals)
    game.bank.return_resources(r)
    return {"status": "ok"}
