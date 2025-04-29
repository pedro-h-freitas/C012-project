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
        self.arrive_time = arrive_time

    def __str__(self):
        return '({}){:<10}({}){:<15} {}'.format(self.priority, self.category, self.char, self.action, self.amount)

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

    def get_time(self):
        time = {
            "SAQUE": 1,
            "DEPOSITO": 2,
            "APOSENTADORIA": 3,
            "CONTA": 4,
            "2° VIA": 5,
            "MEGA-SENA": 6
        }
        return time[self.action]

    def draw(self, stdsrc: curses.window, y: int, x: int):
        stdsrc.attron(curses.color_pair(self.color))
        stdsrc.addch(y, x, self.char, curses.A_REVERSE)
        stdsrc.attroff(curses.color_pair(self.color))
