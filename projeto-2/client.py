import curses
from consts import *


class Client:
    def __init__(self, id: int, category: str, amount: int, action: str, arrive_time: int):
        self.id = id
        self.category = category
        self.action = action
        self.amount = amount
        self.color = self.__get_color(category)
        self.char = self.__get_char(action)
        self.priority = self.__get_priority(category)
        self.action_time = self.__get_time_action(action)
        self.arrive_time = arrive_time
        self.wait_time: float | None = None
        self.end_time: float | None = None

    def __str__(self):
        # return '{:<3}({}){:<10}({}){:<15}{:>5.2f}'.format(self.id, self.priority, self.category, self.action_time, self.action, self.wait_time)
        return '{:>2} {}-{}   {}-{}   {:>5.2f}s'.format(self.id, self.priority, self.category[0], self.action_time, self.action[0], self.wait_time)

    def __get_priority(self, category):
        priority = {
            "IDOSO": 1,
            "PCD": 2,
            "GRAVIDA": 3,
            "ADULTO": 4
        }
        return priority[category]

    def __get_color(self, category: str):
        category_color = {
            "IDOSO": RED,
            "PCD": YELLOW,
            "GRAVIDA": BLUE,
            "ADULTO": GREEN
        }
        return category_color[category]

    def __get_char(self, action: str):
        action_char = {
            "SAQUE": 'S',
            "DEPOSITO": 'D',
            "APOSENTADORIA": 'A',
            "CONTA": 'C',
            "2° VIA": 'V',
            "MEGA-SENA": 'M'
        }
        return action_char[action]

    def __get_time_action(self, action):
        time = {
            "SAQUE": 3,
            "DEPOSITO": 4,
            "APOSENTADORIA": 5,
            "CONTA": 6,
            "2° VIA": 7,
            "MEGA-SENA": 8
        }
        return time[action]

    def draw(self, stdsrc: curses.window, y: int, x: int):
        stdsrc.attron(curses.color_pair(self.color))
        stdsrc.addch(y, x, self.char, curses.A_REVERSE)
        stdsrc.attroff(curses.color_pair(self.color))
        stdsrc.addstr(y+1, x-1, f'{self.id:>2}')
