import json
import uuid
import pandas as pd

from pathlib import Path

from typing import Optional
from typing_extensions import final

from fastapi import FastAPI, Request, Cookie, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic.types import Json

import starlette.status as status

from pydantic import BaseModel

from auth.auth_bearer import JWTBearer

from logic.game import Game

from models.game_data import GameDataModel
from models.move import MoveModel
from models.user import UserModel
from models.game_join import JoinGameModel

from utils.utils import read_dataset, choose_word


app = FastAPI()

games = dict()

word_dataset = read_dataset()


@app.get('/', tags=['Gameplay'], dependencies=[Depends(JWTBearer())], response_class=JSONResponse)
async def refresh(request: Request):
    '''
        Endpoint used to get updates (each player involved in a game will send a request to this endpoint
        checking for changes, server will responde with any changes).
        This is only available if the player is in a game.
    '''
    pass


@app.get('/word', tags=['Gameplay'], dependencies=[Depends(JWTBearer())], response_class=JSONResponse)
def get_word(request: Request):
    '''
        Endpoint used to get a random word from the dataset.
        This will return a random word.
    '''
    ret = {
        'word': choose_word(word_dataset)
    }
    return JSONResponse(content=ret)


@app.post('/game/create', response_class=JSONResponse, response_model=GameDataModel, tags=['Gameplay'])
async def create_game(request: Request, user: UserModel):
    '''
        Endpoint will create a game and will share details for ui.
    '''
    game_id = uuid.uuid4()
    user_id = user.user_id
    game = Game(user_id)
    games[str(game_id)] = game


@app.delete('/game', dependencies=[Depends(JWTBearer())], response_class=JSONResponse, tags=['Gameplay'])
async def end_game(request: Request):
    '''
        Endpoint will delete a game from the server.
        This will be called whenever a game ends or is terminated manually.
    '''
    pass


@app.post('/game/join', response_class=JSONResponse, response_model=GameDataModel, tags=['Gameplay'])
async def join_game(request: Request, join_game: JoinGameModel):
    '''
        Endpoint will attempt to join a user to an existing game
    '''
    pass


@app.post('/game/start', dependencies=[Depends(JWTBearer())], response_class=JSONResponse, tags=['Gameplay'])
async def start_game(request: Request):
    '''
        Endpoint will start a game (initialize the game after all users joined)
    '''
    pass


@app.post('/move', dependencies=[Depends(JWTBearer())], response_class=JSONResponse, tags=['Gameplay'])
async def make_move(request: Request, move: MoveModel):
    '''
        Endpoint that makes a move in a game.
    '''
    pass