import random
import json
from tkinter import E

from pydantic.types import Dict

class Game:

    def __init__(self, owner_id):
        self.score = 0
        self.lives = 6
        self.owner = str(owner_id)
        self.players = []
        self.guesses = dict()
        self.players.append(owner_id)
        self.to_update = {
            key: 0 for key in self.players
        }
        self.current_player = 0
        self.started = False
        self.terminated = False
        self.last_update = None

    # def last_update_factory(code: int):
    #     def last_update(fn):
    #         def inner(self, *args, **kwargs):
    #             self.last_update = code
    #             fn(*args, **kwargs)

    # @last_update_factory(0x02)
    def start_game(self, words):
        try:
            self.last_update = 0x02
            self.started = True
            self.word = self.choose_word(words)
            self.set_update()
            self.to_update[self.owner] = []
        except Exception as e:
            print(e)
            raise e

    # @last_update_factory(0x04)
    def player_join(self, player):
        self.last_update = 0x04
        self.players.append(str(player))
        self.set_update()
        self.to_update[str(player)] = 0

    def make_move(self, move, words):
        if not self.validate_input(move, words):
            return -1

        self.lives -= 1
        self.current_player = (self.current_player + 1) % len(self.players)
        self.set_update()

        return self.check_word(move)
    
    def choose_word(self, words):
        return words.loc[random.randint(0, len(words))].values
    
    def validate_input(self, player, words):
        return False if len(player) != 5 else words.word.str.contains(player).any()

    # @last_update_factory(0x01)
    def check_word(self, player) -> list:
        self.last_update = 0x01
        if player == self.word:
            self.score += 1
            return [1 for i in range(5)]

        self.guesses[player] = [1 if player[i] == self.word[i] else 0.5 if player[i] in self.word else 0 for i in range(5)]

        return self.guesses[player]

    def set_update(self):
        self.to_update = {
            key: 1 for key in self.players
        }

    def switch_update(self, user_id):
        if self.to_update[user_id]:
            self.to_update[user_id] = 0
            return True
        return False

    def check_updates(self, user_id) -> Dict:
        return {
            'game': self.to_dict(),
            'status_code': self.last_update
        } if self.switch_update(user_id) else {
            'status_code': 0x00
        }
            
    # @last_update_factory(0x08)
    def end_game(self):
        self.last_update = 0x08
        self.terminated = True
        self.set_update()
    
    def to_json(self, file=None):
        data = {
            'score': self.score,
            'lives': self.lives,
            'owner': self.owner,
            'players': self.players,
            'started': self.started,
            'current_player': self.current_player,
            'guesses': self.guesses,
            'terminated': self.terminated
        }

        if file:
            with open(file, 'w') as f:
                json.dumps(data, f)

        return json.dumps(data)

    def to_dict(self):
        data = {
            'score': self.score,
            'lives': self.lives,
            'owner': self.owner,
            'players': self.players,
            'started': self.started,
            'current_player': self.current_player,
            'guesses': self.guesses,
            'terminated': self.terminated
        }

        if self.last_update == 0x08: data['word'] = self.word

        return data