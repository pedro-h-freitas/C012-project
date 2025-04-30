import curses
from consts import *


class Client:
    def __init__(self, category: str, amount: int, action: str, arrive_time: int):
        self.category = category
        self.action = action
        self.amount = amount
        self.color = self.__get_color(category)
        self.char = self.__get_char(action)
        self.priority = self.__get_priority(category)
        self.action_time = self.__get_time_action(action)
        self.arrive_time = arrive_time
        self.wait_time: float

    def __str__(self):
        return '({}){:<10}({}){:<15}{:.2f}'.format(self.priority, self.category, self.action_time, self.action, self.wait_time)

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
