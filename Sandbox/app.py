#!/usr/bin/env python3

from fastapi import FastAPI
from random import randint
from pydantic import BaseModel
from game import Game
from pydantic import BaseModel

app = FastAPI()
g = Game.__new__(Game)

###########
# check out these three please:
# https://fastapi.tiangolo.com/tutorial/body-multiple-params/
# https://fastapi.tiangolo.com/tutorial/background-tasks/
# https://fastapi.tiangolo.com/tutorial/testing/
###########
class PlayerColour(BaseModel):
    colour: str

@app.post("/add_player")
def create_player(player: PlayerColour):
    # curl -X POST
    #      --header "Content-Type: application/json"
    #      --data '{"colour": "red"}'
    #      127.0.0.1:8000/add_player

    g.add_player(player.colour)
    return { "player": g.players[-1] }

class GameConfig(BaseModel):
    num_of_human_player: int
    num_of_ai_player: int
    color_of_player: list[str]
    board_size: int = 3

@app.post("/start_game")
def start_game(game_config: GameConfig):
    g.__init__(
        num_of_human_players = game_config.num_of_ai_player,
        num_of_ai_player = game_config.num_of_ai_player,
        color_of_player = game_config.color_of_player,
        board_size=game_config.board_size
        )
    gid = g.get_game_id()
    board_state = g.board.to_json()
    return {
        "game id": gid,
        "board state": board_state,
    }

class PlayerInfo(BaseModel):
    game_id: int
    player_colour: str

@app.get("/roll_dice")
def read_roll_dice(player_info: PlayerInfo):
    pass

@app.get("/end_turn")
def end_turn(player_info: PlayerInfo):
    pass

@app.get("/board_state")
def get_board_state(player_info: PlayerInfo):
    pass

@app.get("/updated_player_resource")
def update_player_resource(player_info: PlayerInfo):
    pass

@app.get("/available_actions")
def available_actions(player_info: PlayerInfo):
    pass

@app.get("/valid_location/{infrastructures}")
def get_valid_locations(player_info: PlayerInfo, infrastructures: str, reachable: bool = None):
    if infrastructures == "roads":
        pass
    elif infrastructures == "cities":
        pass
    elif infrastructures == "settlements" and (reachable is not None):
        pass

# class PlayerAtPosition(BaseModel):
#     game_id: int
#     colour: str
#     intersection_id: int
#   I add extra parameters in stead of creating a new class

@app.get("/build/{infrastructures}")
def get_valid_locations(player_info: PlayerInfo, hexagon_id: int, infrastructures: str):
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
