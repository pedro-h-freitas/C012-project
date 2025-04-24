import curses


class Client:
    def __init__(self, category: str, amount: int, action: str, color: int):
        self.category = category
        self.action = action
        self.amount = amount
        self.color = color

    def draw(self, stdsrc: curses.window, y: int, x: int):
        stdsrc.attron(curses.color_pair(self.color))
        stdsrc.addch(y, x, " ", curses.A_REVERSE)
        stdsrc.attroff(curses.color_pair(self.color))

    def __str__(self):
        return f'{self.category}\t{self.action}\t{self.amount}'

    def get_time(self):
        time = {
            "SAQUE": 1,
            "DEPOSITO": 2,
            "APOSENTADORIA": 3,
            "CONTA": 4,
            "2° VIA": 5,
            "TIGRINHO": 6
        }
        return time[self.action]

    def get_priority(self):
        priority = {
            "IDOSO": 1,
            "PCD": 2,
            "GRAVIDA": 3,
            "ADULTO": 4
        }
        return priority[self.category]


clients = {
    "client_1": {"category": "PCD",      "action": "CONTA",        "amount": 428},
    "client_2": {"category": "ADULTO",   "action": "DEPOSITO",     "amount": 915},
    "client_3": {"category": "IDOSO",    "action": "SAQUE",        "amount": 157},
    "client_4": {"category": "GRAVIDA",  "action": "2° VIA",       "amount": 602},
    "client_5": {"category": "ADULTO",   "action": "TIGRINHO",     "amount": 329},
    "client_6": {"category": "PCD",      "action": "APOSENTADORIA", "amount": 774},
    "client_7": {"category": "IDOSO",    "action": "DEPOSITO",     "amount": 241},
    "client_8": {"category": "GRAVIDA",  "action": "SAQUE",        "amount":  88},
    "client_9": {"category": "ADULTO",   "action": "CONTA",        "amount": 503},
    "client_10": {"category": "PCD",      "action": "TIGRINHO",     "amount": 640},
}
