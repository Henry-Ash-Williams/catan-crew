#!/usr/bin/env python3

from fastapi import FastAPI
from random import randint
from pydantic import BaseModel
from game import Game
from pydantic import BaseModel

app = FastAPI()
g = Game.__new__(Game)

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


@app.get("/roll_dice")
def read_roll_dice():
    return {"result": randint(1, 6) + randint(1, 6)}

@app.get("/valid_settlement_locations")
def get_valid_settlement_locations(colour: str, reachable: bool = True):
    pass

class PlayerAtPosition(BaseModel):
    colour: str
    intersection_id: int

@app.post("/place_settlement")
def create_settlement(settlement: PlayerAtPosition):
    pass

@app.post("/place_road")
def place_road(info: PlayerAtPosition):
    pass

@app.get("valid_robber_locations")
def get_valid_robber_locations():
    pass
