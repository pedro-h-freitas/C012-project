from math import floor, ceil
import curses
import time

from lottery_booth import LotteryBooth
from client import Client
from consts import *


class LotteryApp():
    def __init__(self):
        self.stdsrc: curses.window

        self.height: int
        self.width: int

        self._vault = 100

        self.booths = [
            LotteryBooth('1', BLUE, Client("PCD", 428, "CONTA", BLUE)),
            LotteryBooth('2', CYAN),
            LotteryBooth('3', MAGENTA),
            LotteryBooth('4', YELLOW),
            LotteryBooth('5', RED)
        ]

        self.clients = [
            Client("PCD", 428, "CONTA", BLUE),
            Client("ADULTO", 915, "DEPOSITO", CYAN),
            Client("IDOSO", 157, "SAQUE", MAGENTA),
            Client("GRAVIDA", 602, "2° VIA", YELLOW),
            Client("ADULTO", 329, "TIGRINHO", RED)
        ]

        self.booths_space = len(self.booths) * 5 + (len(self.booths) - 1) * 4

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

    def draw_lottery_booths(self):
        y = 8
        x = floor(self.width / 2) - ceil(self.booths_space / 2)

        for booth in self.booths:
            booth.draw(self.stdsrc, y, x)
            x += 9

    def draw_queue(self):
        x = floor(self.width / 2) - ceil(self.booths_space / 2)

        for client in self.clients:
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

        while True:
            stdsrc.clear()

            self.draw_lottery()
            self.draw_lottery_booths()
            self.draw_queue()

            stdsrc.refresh()
            time.sleep(0.2)  # Reduzindo o tempo de espera


if __name__ == '__main__':
    app = LotteryApp()
    curses.wrapper(app.run)
