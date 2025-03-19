from __future__ import annotations
from threading import Thread
from typing import Literal


class Player:
    def __init__(self, simbol: str):
        self.simbol = simbol
        self.type: Literal['L', 'R'] | None = None

        self.match: Match | None = None
        self.match_end: bool | None = None

    def play(self):
        while not self.match_end:
            self.match.bar += 1 if self.type == 'L' else -1

    def start(self, m: Match, player_type: Literal['L', 'R']):
        self.match = m
        self.type = player_type
        self.match_end = False

        t = Thread(target=self.play)
        t.start()

    def finish(self):
        self.match_end = True


class Match:
    def __init__(self, left_player: Player, right_player: Player):
        self.bar: int = 500000
        self.left_player = left_player
        self.right_player = right_player
        self.winner: Player | None = None

    def check_winner(self):
        while True:
            if self.bar <= 0:
                self.winner = self.right_player
                self.right_player.finish()
                self.left_player.finish()
                break

            elif self.bar >= 1000000:
                self.winner = self.left_player
                self.right_player.finish()
                self.left_player.finish()
                break

    def start(self):
        self.left_player.start(self, 'L')
        self.right_player.start(self, 'R')

        t = Thread(target=self.check_winner)
        t.start()


class Game:
    def __init__(self):
        self.player_1 = Player('*')
        self.player_2 = Player('+')

    def verify_winner(self, m: Match):
        while m.winner is None:
            pass
        print(f'Vencendor é: {m.winner.simbol}')

    def start(self):
        m = Match(self.player_1, self.player_2)
        m.start()

        t = Thread(target=self.verify_winner, args=[m])
        t.start()


if __name__ == '__main__':
    g = Game()
    g.start()
