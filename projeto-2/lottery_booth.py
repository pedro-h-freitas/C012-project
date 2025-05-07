import threading
import time
import random
from client import Client
import curses
from lottery_vault import LotteryVault


class LotteryBooth:
    def __init__(self, booth_id, color, vault: LotteryVault, client=None):
        self.id = booth_id
        self.semaphore = threading.Semaphore(1)
        self.color = color
        self.client: Client | None = client

        self.__vault = vault
        self.__transaction_array = []

    def draw(self, stdsrc: curses.window, y: int, x: int, is_running: bool = True):
        stdsrc.attron(curses.color_pair(self.color))
        stdsrc.addstr(y, x,   "╭─────╮")
        stdsrc.addstr(y+1, x, "│╱   ╲│")
        stdsrc.addstr(y+2, x, "├┴───┴┤")
        stdsrc.addstr(y+3, x, "│     │")

        hr = time.time()
        if is_running and int(hr) % 2 == 0:
            stdsrc.addstr(y+1, x+2, "▝_▘")
        else:
            stdsrc.addstr(y+1, x+2, "-_-")
        stdsrc.attroff(curses.color_pair(self.color))

        if self.client:
            self.client.draw(stdsrc, y+3, x+3)

    def serve(self, client: Client):
        self.client = client
        print(
            f"ENTRADA - CABINE {self.id} - {client.category} - {client.amount} reais"
        )
        if client.action == 'SAQUE':
            self.__transaction_array.append(-client.amount)
        else:
            self.__transaction_array.append(client.amount)
        time.sleep(client.action_time)
        print(
            f"SAÍDA - CABINE {self.id} - {client.category} - {client.amount} reais"
        )
        self.client = None
        self.semaphore.release()

    def close_booth(self):
        print(f'Fechando o caixa: {self.id}')
        print(self.__transaction_array)
        threading.Thread(
            target=self.__vault.transaction,
            args=[self.__transaction_array]
        ).start()
