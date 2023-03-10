#!/usr/bin/env python3

from fastapi import FastAPI
from random import randint
from game import Game

app = FastAPI()

@app.get("/roll_dice")
def read_roll_dice():
    return {"result": randint(1, 6) + randint(1, 6)}
