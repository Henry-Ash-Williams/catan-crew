#!/usr/bin/env python3

from fastapi import FastAPI, Depends, Query
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

# plus: I think you can just return an dictionary like object.
# It should just cast to JSON automatically
# localhost/docs is useful when u run it


### ** to run it: uvicorn app:app --reload ** ###

@app.get("/")
def hello_word():
    return "I am running"

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

# This is stupid, but because you can't have request body for get request
# you can only use query parameter, which doesn't support by using BaseModel
# Therefore, need to use class as dependency
# Otherwise, you won't be able to test it with docs
class GPlayerInfo:
    def __init__(self, game_id: int, player_colour: str):
        self.game_id = game_id = Query(...)
        self.player_colour = player_colour = Query(...)
        # Query(...) means explicitly declare that a value is required
        # but even it's not used, it should be required

class PlayerInfo(BaseModel):
    game_id: int
    player_colour: str



@app.get("/roll_dice")
def read_roll_dice(player_info: GPlayerInfo = Depends()):
    return {player_info.game_id, player_info.player_colour} # this for test

@app.get("/end_turn")
def end_turn(player_info: GPlayerInfo = Depends()):
    pass

@app.get("/board_state")
def get_board_state(player_info: GPlayerInfo = Depends()):
    pass

@app.get("/updated_player_resource")
def update_player_resource(player_info: GPlayerInfo = Depends()):
    pass

@app.get("/available_actions")
def available_actions(player_info: GPlayerInfo = Depends()):
    pass

@app.get("/valid_location/{infrastructures}")
def get_valid_locations(infrastructures: str, reachable: bool = None, player_info: GPlayerInfo = Depends()):
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

@app.post("/build/{infrastructures}")
def build_infrastructures(hexagon_id: int, infrastructures: str, player_info: PlayerInfo):
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
