#!/usr/bin/env python3

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from game import Game
from pydantic import BaseModel
from copy import deepcopy

app = FastAPI()
games = {}

###########
# check out these three please:
# https://fastapi.tiangolo.com/tutorial/body-multiple-params/
# https://fastapi.tiangolo.com/tutorial/background-tasks/
# https://fastapi.tiangolo.com/tutorial/testing/
###########

# plus: I think you can just return an dictionary like object.
# It should just cast to JSON automatically
# localhost/docs is useful when u run it

### ** to run it: uvicorn app:app --reload ** ###


class PlayerInfo(BaseModel):
    game_id: int
    player_colour: str


class GameConfig(BaseModel):
    num_of_human_player: int
    num_of_ai_player: int
    color_of_player: list[str]
    board_size: int = 3


# This is stupid, but because you can't have request body for get request
# you can only use query parameter, which doesn't support by using BaseModel
# Therefore, need to use class as dependency
# Otherwise, you won't be able to test it with docs
class GPlayerInfo:
    def __init__(self, game_id: str, player_colour: str):
        self.game_id = Query(game_id)
        self.player_colour = Query( player_colour )
        # Query(...) means explicitly declare that a value is required
        # but even it's not used, it should be required


def get_game(game_uuid: str, games: {str, Game}) -> Game:
    if not games[str( game_uuid )]:
        raise Exception("Game not found")
    return games[str(game_uuid)]



@app.get("/")
def hello_word():
    return "I am running"


@app.post("/add_player")
def create_player(player: PlayerInfo):
    # curl -X POST
    #      --header "Content-Type: application/json"
    #      --data '{"colour": "red"}'
    #      127.0.0.1:8000/add_player

    games[player.game_id].add_player(player.player_colour)
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
    [g.add_player(player_colour.lower())
     for player_colour in game_config.color_of_player]
    games[gid] = deepcopy(g)
    print(games)
    return {
        "game_id": gid,
        "board_state": board_state,
    }


@app.get("/dump_games")
def dump_games():
    print(games)
    return { "status": 200 }



@app.get("/roll_dice")
def read_roll_dice(player_info: GPlayerInfo = Depends()):
    return {player_info.game_id, player_info.player_colour}  # this for test


@app.get("/end_turn")
def end_turn(player_info: GPlayerInfo = Depends()):
    pass


@app.get("/board_state")
def get_board_state(player_info: GPlayerInfo = Depends()):
    game = get_game(player_info.game_id, games)
    return str(game.board.to_json())


@app.get("/updated_player_resource")
def update_player_resource(player_info: GPlayerInfo = Depends()):
    pass


@app.get("/available_actions")
def available_actions(player_info: GPlayerInfo = Depends()):
    game = get_game(player_info.game_id.default, games)
    player = [
        player
        for idx, player in enumerate( game.players )
        if player.color.lower() == player_info.player_colour.default.lower()
    ][0]

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
    game = get_game(player_info.game_id, games)
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
    if infrastructures == "roads":
        pass
    elif infrastructures == "cities":
        pass
    elif infrastructures == "settlements":
        pass


# refactor with the use of get valid locations method
# @app.post("/place_settlement")
# def create_settlement(settlement: PlayerAtPosition):
#     pass

# @app.post("/place_road")
# def place_road(info: PlayerAtPosition):
#     pass


@app.get("valid_robber_locations")
def get_valid_robber_locations():
    pass
