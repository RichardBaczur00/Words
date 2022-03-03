import random
import json

class Game:

    def __init__(self, owner_id):
        self.score = 0
        self.lives = 6
        self.owner = owner_id
        self.players = []
        self.guesses = []
        self.players.append(owner_id)
        self.to_update = {
            key: 0 for key in self.players
        }
        self.current_player = 0
        self.started = False
        self.terminated = False

    def start_game(self, words):
        self.started = True
        self.word = self.choose_word(words)
        self.set_update()

    def player_join(self, player):
        self.players.append(player)
        self.to_update[player] = 0

    def make_move(self, move, words):
        if not self.validate_input(move, words):
            return -1

        self.lives -= 1
        self.current_player = (self.current_player + 1) % len(self.players)

        return self.check_word(move)
    
    def choose_word(self, words):
        return words.loc[random.randint(0, len(words))].values
    
    def validate_input(self, player, words):
        return False if len(player) != 5 else words.word.str.contains(player).any()

    def check_word(self, player) -> list:
        if player == self.word:
            self.score += 1
            return [1 for i in range(5)]

        self.guesses.append(player)

        return [1 if player[i] == self.word[i] else 0.5 if player[i] in self.word else 0 for i in range(5)]

    def set_update(self):
        self.to_update = {
            key: 1 for key in self.players
        }

    def end_game(self):
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

        return data