import os
from typing import Optional
import uuid
import pymongo

from decouple import config
from pathlib import Path


def db_connect():
    cert_path = Path(os.path.dirname(os.path.abspath(__file__)))
    uri = "mongodb+srv://cluster0.9gl06.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=str(cert_path) + '.\\X509-cert-3795259400974282102.pem')
    print(client)
    return client['WordsDB']

db = db_connect()


def save_stats(user_id: str, winner: bool, attempts: int = None) -> None:
    if winner and not attempts:
        print('Can\'t save win without number of attempts')
        return

    db.users.update_one(filter = {
        'user_id': user_id
    }, update = {
        '$set': {
            'played_today': True
        }
    })

    if winner:
        # save to db
        stats = db.get_collection('stats').find_one(filter={
            'user_id': user_id
        })
        if stats is not None:
            db.get_collection('stats').update_one(filter={
                'user_id': user_id
            }, update = {
                '$inc': {
                    f'attempts.{attempts}': 1,
                    'games': 1,
                    'wins': 1
                }
            })
        else:
            db.stats.insert_one(document={
                'user_id': user_id,
                'attempts': { str(key): value for key, value in zip(range(-1, 7), [ 0 if attempts != i else 1 for i in range(-1, 7) ] ) },
                'games': 1,
                'wins': 1
            })
    else:
        attempts = -1
        #save to db
        stats = db.get_collection('stats').find_one(filter={
            'user_id': user_id
        })
        if stats is not None:
            db.get_collection('stats').update_one(filter={
                'user_id': user_id
            }, update = {
                '$inc': {
                    'games': 1,
                }
            })
        else:
            db.stats.insert_one(document={
                'user_id': user_id,
                'attempts': { str(key): value for key, value in zip(range(-1, 8), [ 0 for i in range(-1, 7) ] ) },
                'games': 1,
                'wins': 0
            })
        

def get_stats(user_id: str) -> dict:
    stats = db.get_collection('stats').find(filter = {
        'user_id': user_id
    })
    print(stats)
    for stat in stats:
        return {key: value for key, value in stat.items() if key != '_id'} # lol


def login_user(username: str, password: str) -> Optional[str]:
    match = db.get_collection('users').find_one(filter = {
        'username': username
    })
    return match['user_id'] if match['password'] == password else None
    

def register_user(username: str, password: str) -> bool:
    uid = str(uuid.uuid4())
    
    db.get_collection('users').insert_one({
        'username': username,
        'password': password,
        'user_id': uid,
        'played_today': False
    })

    return uid


def can_play(uid: str) -> bool:
    return not db.get_collection('users').find_one(filter = {
        'user_id': uid
    })['played_today']

