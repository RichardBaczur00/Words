import json
import uuid
import pandas as pd

from pathlib import Path

from typing import Optional
from typing_extensions import final

from fastapi import FastAPI, Request, Cookie, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic.types import Json, Dict

import starlette.status as status

from pydantic import BaseModel

from auth.auth_bearer import JWTBearer

from logic.game import Game

from models.game_data import GameDataModel
from models.move import MoveModel
from models.user import UserModel
from models.game_join import JoinGameModel
from models.game_start import GameStartModel

from utils.utils import read_dataset, choose_word

from auth.auth_handler import signJWT


app = FastAPI()

games: Dict[str, Game] = dict()

word_dataset = read_dataset()


@app.get('/', tags=['Gameplay'], dependencies=[Depends(JWTBearer())], response_class=JSONResponse)
async def refresh(request: Request, refresh_data: JoinGameModel):
    '''
        Endpoint used to get updates (each player involved in a game will send a request to this endpoint
        checking for changes, server will responde with any changes).
        This is only available if the player is in a game.

        Return codes (stored with `status_code` as key):
        1. No updates    (0x00)
        2. New guess     (0x01)
        3. Game start    (0x02)
        4. Player joined (0x04)
        5. Game ended    (0x08)
    '''
    content = games[refresh_data.game_id].check_updates(refresh_data.user_id)
    return JSONResponse(content=content)


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
    games[game_id] = game
    return JSONResponse(content = {
        'game': games[game_id].to_dict(),
        'game_token': signJWT(user_id, game_id)
    })


@app.delete('/game/end', dependencies=[Depends(JWTBearer())], response_class=JSONResponse, tags=['Gameplay'])
async def end_game(request: Request, end: GameStartModel):
    '''
        Endpoint will delete a game from the server.
        This will be called whenever a game ends or is terminated manually.
    '''
    try:
        games[end.game_id].end_game()
    except:
        raise HTTPException(status_code=417, detail='Failed to end game!')
    else:
        return JSONResponse(content = {
            'game': games[end.game_id].to_dict()
        })


@app.post('/game/join', response_class=JSONResponse, response_model=GameDataModel, tags=['Gameplay'])
async def join_game(request: Request, join_game: JoinGameModel):
    '''
        Endpoint will attempt to join a user to an existing game
    '''
    try:
        games[join_game.game_id].player_join(join_game.user_id)
    except:
        return HTTPException(status_code=417, detail='Failed to join game!')
    else:
        return JSONResponse(content = {
            'game': games[join_game.game_id].to_dict(),
            'game_token': signJWT(join_game.user_id, join_game.game_id)
        })


@app.post('/game/start', dependencies=[Depends(JWTBearer())], response_class=JSONResponse, tags=['Gameplay'])
async def start_game(request: Request, start: GameStartModel):
    '''
        Endpoint will start a game (initialize the game after all users joined)
    '''
    try:
        games[start.game_id].start_game(word_dataset)
    except:
        return HTTPException(status_code=417, detail='Failed to start game!')
    else:
        return JSONResponse(content = {
            'game': games[start.game_id].to_dict()
        })


@app.post('/move', dependencies=[Depends(JWTBearer())], response_class=JSONResponse, tags=['Gameplay'])
async def make_move(request: Request, move: MoveModel):
    '''
        Endpoint that makes a move in a game.

        Return codes (stored with `status_code` as key):
        1. Valid Move     (0x00)
        2. Invalid Move   (0x01)
        3. Invalid Player (0x02)
    '''
    try:
        move_status = games[move.game_id].make_move(move.player_word, word_dataset) \
            if games[move.game_id].players[games[move.game_id].current_player] == move.user_id else None
    
        if move_status is None:
            return JSONResponse(content = {
                'status_code': 0x01
            })

        if move_status == -1:
            return JSONResponse(content = {
                'status_code': 0x02
            })

        return JSONResponse(content = {
            'status_code': 0x00,
            'game': games[move.game_id].to_dict()
        })
        
    except:
        raise HTTPException(status_code=417, detail='Failed to make move!')

