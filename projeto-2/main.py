import curses
import time
from math import floor, ceil

GREEN_BLACK = 1
BLUE_BLACK = 2

BLACK_GREEN = 3
BLACK_BLUE = 4


class LotteryApp():
    def __init__(self):
        self.stdscr: curses.window

        self.height: int
        self.width: int

        self._vault = 100

    def draw_queue(self):
        pass

    def write_str_center(self, y, str):
        x = floor(self.width / 2) - ceil(len(str) / 2)

        self.stdscr.addstr(y, x, str)

    def draw_lottery(self):
        self.stdscr.attron(curses.color_pair(GREEN_BLACK))
        self.write_str_center(0, '─'*10 + ' LOTERICA ' + '─'*10)
        self.stdscr.attroff(curses.color_pair(GREEN_BLACK))

        self.write_str_center(2, '─'*5 + ' COFRE ' + '─'*5)
        self.write_str_center(3, str(self._vault))
        self.write_str_center(4, '─'*17)

    def draw_lottery_booths(self):
        pass

    def run(self, stdscr: curses.window):
        curses.start_color()
        curses.init_pair(GREEN_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(BLACK_GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(BLUE_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(BLACK_BLUE, curses.COLOR_BLACK, curses.COLOR_BLUE)

        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

        while True:
            stdscr.clear()

            self.draw_lottery()
            self.draw_lottery_booths()

            stdscr.refresh()
            time.sleep(0.2)  # Reduzindo o tempo de espera


if __name__ == '__main__':
    app = LotteryApp()
    curses.wrapper(app.run)
