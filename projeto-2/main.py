from math import floor, ceil
import curses
import time
import argparse
import threading

from lottery_booth import LotteryBooth
from lottery_booth import LotteryVault
from client import Client
from client_queue import ClientQueue
from consts import *

COLORS = [GREEN, BLUE, CYAN, MAGENTA, RED, WHITE, YELLOW]


class LotteryApp():
    def __init__(self, clients: list[Client], booths: list[LotteryBooth], client_queue: ClientQueue, vault: LotteryVault):
        self.clients = clients  # Lista dos clientes que chegarão na lotérica
        self.booths = booths
        self.client_queue = client_queue
        self.vault = vault

        # Lista de clientes que já foram atendidos
        self.served_clients: list[Client] = []

        # Variaveis para contr
        self.booths_space = len(self.booths) * 6 + (len(self.booths) - 1) * 4
        self.info_space = 25

        self.stdsrc: curses.window
        self.height: int
        self.width: int

        self.start_time: float

    def __write_str_center(self, y, str):
        x = floor(self.width / 2) - ceil(len(str) / 2)

        self.stdsrc.addstr(y, x, str)

    def draw_lottery(self):
        loterica_str = '─'*(ceil((self.booths_space) / 2)+3) + \
            ' LOTERICA '+'─'*(floor((self.booths_space) / 2)+3)
        cofre_str = '─'*ceil((self.booths_space) / 2) + \
            ' COFRE '+'─'*floor((self.booths_space) / 2)

        self.stdsrc.attron(curses.color_pair(GREEN))
        self.__write_str_center(0, loterica_str)
        self.stdsrc.attroff(curses.color_pair(GREEN))

        self.__write_str_center(2, cofre_str)
        self.__write_str_center(3, str(self.vault.amount))
        self.__write_str_center(4, '─'*(len(cofre_str)))

    def draw_hist(self):
        self.stdsrc.addstr(0, 0, '{:<16}{:<10}{}'.format(
            '   CATEGORIA', 'AÇÃO', ' TEMPO ESPERA'
        ))

        y = 1
        total_time = 0
        for client in self.served_clients:
            total_time += client.wait_time
            self.stdsrc.addstr(y, 0, str(client))
            y += 1

        self.stdsrc.attron(curses.color_pair(BLUE))
        for i in range(len(self.served_clients)+4):
            self.stdsrc.addstr(i, 40, '║')
        self.stdsrc.addstr(len(self.served_clients)+1, 0, '─'*40+'╢')
        self.stdsrc.addstr(len(self.served_clients)+4, 0, '═'*40+'╝')
        self.stdsrc.attroff(curses.color_pair(BLUE))

        mean_wait_time = total_time / \
            len(self.served_clients) if len(self.served_clients) != 0 else 0
        self.stdsrc.addstr(
            len(self.served_clients)+2, 0,
            '{:>26}{}{:>6.2f}'.format('', 'TOTAL: ', total_time)
        )
        self.stdsrc.addstr(
            len(self.served_clients)+3, 0,
            '{:>26}{}{:>6.2f}'.format('', 'MEDIA: ', mean_wait_time)
        )

    def draw_infos(self):
        self.stdsrc.addstr(
            0, self.width - self.info_space,
            "        INFOS       "
        )

        actions = [
            "  S - SAQUE         (3s)",
            "  D - DEPOSITO      (4s)",
            "  A - APOSENTADORIA (5s)",
            "  C - CONTA         (6s)",
            "  V - 2° VIA        (7s)",
            "  M - MEGA-SENA     (8s)",
        ]
        for i in range(len(actions)):
            self.stdsrc.addstr(
                i+2, self.width - self.info_space,
                actions[i]
            )

        categories = [
            (RED,       "IDOSO         (1)"),
            (YELLOW,    "PCD           (2)"),
            (BLUE,      "GRAVIDA       (3)"),
            (GREEN,     "ADULTO        (4)")
        ]
        for i in range(len(categories)):
            color, cat = categories[i]

            self.stdsrc.attron(curses.color_pair(color))
            self.stdsrc.addch(
                i+3+len(actions),
                self.width - self.info_space + 2,
                " ", curses.A_REVERSE
            )
            self.stdsrc.attroff(curses.color_pair(color))

            self.stdsrc.addstr(
                i+3+len(actions),
                self.width - self.info_space + 3,
                " - " + cat
            )

        self.stdsrc.attron(curses.color_pair(BLUE))
        for i in range(len(actions) + len(categories) + 3):
            self.stdsrc.addstr(
                i, self.width - self.info_space,
                "║"
            )
        self.stdsrc.addstr(
            len(actions) + len(categories) + 3,
            self.width - self.info_space,
            "╚════════════════════════"
        )
        self.stdsrc.attroff(curses.color_pair(BLUE))

    def draw_lottery_booths(self, is_running: bool = True):
        y = 8
        x = floor(self.width / 2) - ceil(self.booths_space / 2)

        for booth in self.booths:
            booth.draw(self.stdsrc, y, x, is_running)
            x += 9

    def draw_queue(self):
        x = floor(self.width / 2) - ceil(self.booths_space / 2)

        queue = self.client_queue.get_clients()
        for client in queue:
            client.draw(self.stdsrc, 16, x)
            x += 3

    def __reset_cursor(self):
        self.stdsrc.addch(self.height - 1, self.width - 2, ' ')

    def check_client_arrived(self, client: Client | None) -> bool:
        if client:
            return (time.time() - self.start_time) >= client.arrive_time
        return False

    def serve_clients_if_possible(self):
        for booth in self.booths:
            if booth.semaphore.acquire(blocking=False):
                client = self.client_queue.get_next()
                if client:
                    wait_time = time.time() - self.start_time - client.arrive_time
                    client.wait_time = wait_time
                    self.served_clients.append(client)
                    threading.Thread(target=booth.serve, args=[client]).start()
                else:
                    booth.semaphore.release()

    def check_clients_end(self) -> bool:
        is_empty_wait_queue = all(
            [client is None for client in self.clients]
        )
        is_empty_client_queue = len(self.client_queue.get_clients()) == 0
        all_booths_empty = all(
            [booth.client is None for booth in self.booths]
        )

        return is_empty_client_queue and is_empty_wait_queue and all_booths_empty

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
            # Processamento
            for i, client in enumerate(self.clients):
                if self.check_client_arrived(client):
                    client.arrive_time = time.time() - self.start_time
                    self.client_queue.add_client(client)
                    self.clients[i] = None

            self.serve_clients_if_possible()

            if self.check_clients_end():
                for booth in self.booths:
                    booth.close_booth()
                break

            # Desenha componentes
            self.stdsrc.clear()
            self.draw_lottery()
            self.draw_lottery_booths()
            self.draw_queue()
            self.draw_hist()
            self.draw_infos()
            self.__reset_cursor()

            self.stdsrc.refresh()

        while True:
            # Desenha componentes
            self.stdsrc.clear()
            self.draw_lottery()
            self.draw_lottery_booths(is_running=False)
            self.draw_hist()
            self.draw_infos()
            self.__reset_cursor()

            self.stdsrc.refresh()


class ArgumentParserBuilder():
    def build():
        parser = argparse.ArgumentParser(
            description="Simulação de uma Loteria utilizando múltiplas threads para representar atendimento em caixas."
        )
        parser.add_argument(
            "--monitor",
            action="store_true",
            help="Ativa o uso de monitor para controle de concorrência."
        )
        parser.add_argument(
            "--scheduling",
            type=str,
            choices=["PS", "SJF"],
            required=True,
            help="Define o algoritmo de escalonamento utilizado na fila de atendimento. 'PS' representa prioridade simples e 'SJF' representa o algoritmo Shortest Job First (menor tempo de atendimento primeiro)."
        )
        parser.add_argument(
            "--booth",
            type=int,
            default=2,
            required=True,
            help="Número de caixas de atendimento simultâneo disponíveis na loteria. Representa o grau de concorrência (quantas threads atenderão clientes em paralelo)."
        )
        return parser.parse_args()


if __name__ == '__main__':
    args = ArgumentParserBuilder.build()

    clients = [
        Client(1, "PCD", 100, "CONTA", 1),
        Client(2, "ADULTO", 200, "DEPOSITO", 1),
        Client(3, "IDOSO", 50, "SAQUE", 1),
        Client(4, "GRAVIDA", 600, "2° VIA", 1),
        Client(5, "PCD", 10, "MEGA-SENA", 1),
        Client(6, "ADULTO", 20, "MEGA-SENA", 2),
        Client(7, "PCD", 40, "APOSENTADORIA", 2),
        Client(8, "GRAVIDA", 50, "DEPOSITO", 2),
        Client(9, "IDOSO", 30, "APOSENTADORIA", 3),
        Client(10, "IDOSO", 60, "DEPOSITO", 3),
        Client(11, "IDOSO", 70, "SAQUE", 3),
        Client(12, "ADULTO", 80, "MEGA-SENA", 4),
        Client(13, "GRAVIDA", 100, "SAQUE", 4),
        Client(14, "ADULTO", 20, "SAQUE", 5),
        Client(15, "GRAVIDA", 20, "2° VIA", 5),
        Client(16, "ADULTO", 20, "2° VIA", 20)
    ]

    vault = LotteryVault(1000, with_lock=args.monitor)
    client_queue = ClientQueue(scheduling=args.scheduling)
    number_of_booths = args.booth

    booths = []
    color_index = 0
    for i in range(number_of_booths):
        booths.append(LotteryBooth(i, COLORS[color_index], vault))
        color_index += 1
        if color_index >= len(COLORS):
            color_index = 0

    app = LotteryApp(clients, booths, client_queue, vault)
    curses.wrapper(app.run)
