#!/usr/bin/env python3

from fastapi import FastAPI
from random import randint
from game import Game
from pydantic import BaseModel

app = FastAPI()
g = Game()

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
