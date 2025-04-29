from math import floor, ceil
import curses
import time
from typing import Literal

from lottery_booth import LotteryBooth
from client import Client
from client_queue import ClientQueue
from consts import *

COLORS = [GREEN, BLUE, CYAN, MAGENTA, RED, WHITE, YELLOW]
NUMBER_OF_BOOTHS = 5


class LotteryApp():
    def __init__(self, clients: list[Client], booths: list[LotteryBooth], scheduling: Literal['SJF', 'PS']):
        self.booths = booths
        self.clients = clients

        self.booths_space = len(self.booths) * 5 + (len(self.booths) - 1) * 4

        self._vault = 100

        self.client_queue = ClientQueue(scheduling)

        self.stdsrc: curses.window
        self.height: int
        self.width: int

        self.start_time: float

    def _write_str_center(self, y, str):
        x = floor(self.width / 2) - ceil(len(str) / 2)

        self.stdsrc.addstr(y, x, str)

    def draw_lottery(self):
        loterica_str = '─'*10 + ' LOTERICA ' + '─'*10
        cofre_str = '─'*ceil((self.booths_space) / 2) + \
            ' COFRE '+'─'*floor((self.booths_space) / 2)

        self.stdsrc.attron(curses.color_pair(GREEN))
        self._write_str_center(0, loterica_str)
        self.stdsrc.attroff(curses.color_pair(GREEN))

        self._write_str_center(2, cofre_str)
        self._write_str_center(3, str(self._vault))
        self._write_str_center(4, '─'*(self.booths_space + 7))

        self.stdsrc.addstr(0, self.width-20, 'D: Depósito')

    def draw_lottery_booths(self):
        y = 8
        x = floor(self.width / 2) - ceil(self.booths_space / 2)

        for booth in self.booths:
            booth.draw(self.stdsrc, y, x)
            x += 9

    def draw_queue(self):
        x = floor(self.width / 2) - ceil(self.booths_space / 2)

        queue = self.client_queue.get_clients()
        for client in queue:
            client.draw(self.stdsrc, 16, x)
            x += 3

    def run(self, stdsrc: curses.window):
        curses.start_color()
        curses.init_pair(GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(PAIRS, curses.COLOR_PAIRS, curses.COLOR_BLACK)
        curses.init_pair(RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.stdsrc = stdsrc
        self.height, self.width = stdsrc.getmaxyx()

        self.start_time = time.time()
        while True:
            time_now = time.time()

            for i in range(len(clients)):
                if clients[i]:
                    if (time_now - self.start_time) >= clients[i].arrive_time:
                        self.client_queue.add_client(clients[i])
                        clients[i] = None

            stdsrc.clear()

            self.draw_lottery()
            self.draw_lottery_booths()
            self.draw_queue()

            stdsrc.refresh()
            time.sleep(0.2)  # Reduzindo o tempo de espera


if __name__ == '__main__':
    clients = [
        Client("PCD", 428, "CONTA",  1),
        Client("ADULTO", 915, "DEPOSITO",  1),
        Client("IDOSO", 157, "SAQUE",  1),
        Client("GRAVIDA", 602, "2° VIA",  1),
        Client("ADULTO", 329, "TIGRINHO",  2),
        Client("ADULTO", 329, "TIGRINHO",  2),
        Client("ADULTO", 329, "TIGRINHO",  3),
        Client("ADULTO", 329, "TIGRINHO",  2),
        Client("ADULTO", 329, "TIGRINHO",  2),
        Client("ADULTO", 329, "TIGRINHO",  4),
        Client("ADULTO", 329, "TIGRINHO",  5)
    ]

    booths = []
    color_index = 0
    for i in range(NUMBER_OF_BOOTHS):
        booths.append(LotteryBooth(i, COLORS[color_index]))
        color_index += 1
        if color_index >= len(COLORS):
            color_index = 0

    app = LotteryApp(clients, booths, 'SJF')
    curses.wrapper(app.run)
