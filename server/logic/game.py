import random

class Game:

    def __init__(self, owner_id):
        self.score = 0
        self.lives = 6
        self.owner = owner_id
        self.players = []
        self.players.append(owner_id)
        self.to_update = []
        self.current_player = 0

    def start_game(self, words):
        self.word = self.choose_word(words)

    def player_join(self, player):
        self.players.append(player)

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
            return [1 for i in range(5)]

        return [1 if player[i] == self.word[i] else 0.5 if player[i] in self.word else 0 for i in range(5)]

