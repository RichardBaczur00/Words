from game import Game

from pydantic import typing

class MultiplayerGame:

    def __init__(self, player_one: str, player_two: str):
        self.game_one = Game(player_one)
        self.game_two = Game(player_two)
        self.players = [player_one, player_two]
        self.to_update = [0, 0]

    def make_move(self, player_id: str, word: str, words):
        check_winner = lambda player: self.game_one.score > self.game_two.score + 1 if player == self.players[0] else self.game_two.score > self.game_one.score + 1

        if player_id == self.players[0]:
            self.to_update = [0, 1]
            move_result = self.game_one.make_move(word, words)
            return move_result if not check_winner(player_id) else [ ord(i) for i in 'pwned' ]
        else:
            self.to_update = [1, 0]
            move_result = self.game_two.make_move(word, words)
            return move_result if not check_winner(player_id) else [ ord(i) for i in 'pwned' ]

