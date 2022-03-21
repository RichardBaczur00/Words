import pymongo

from decouple import config

DB_NAME = config('dbName')
DB_PASS = config('dbPass')

client = pymongo.MongoClient("mongodb+srv://app:{DB_PASS}@cluster0.9gl06.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
db = client.WordsDB

def save_stats(user_id: str, winner: bool, attempts: int = None) -> None:
    if winner and not attempts:
        print('Can\'t save win without number of attempts')
        return
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
                    attempts: 1,
                    'games': 1,
                    'wins': 1
                }
            })
        else:
            db.stats.insert_one(document={
                'user_id': user_id,
                'attempts': { key: value for key, value in zip(range(-1, 7), [ 0 if attempts != i else 1 for i in range(7) ] ) },
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
                    attempts: 1,
                    'games': 1,
                }
            })
        else:
            db.stats.insert_one(document={
                'user_id': user_id,
                'attempts': { key: value for key, value in zip(range(-1, 7), [ 0 for i in range(7) ] ) },
                'games': 1,
                'wins': 0
            })
        


def get_stats(user_id: str) -> dict:
    stats = db.get_collection('stats').find(filter = {
        'user_id': user_id
    })
    print(stats)
    for stat in stats:
        return stat # lol
    

