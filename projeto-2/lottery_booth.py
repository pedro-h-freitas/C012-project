
import time
import curses
import threading
from typing import Callable

from client import Client
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

    def serve(self, client: Client, start_time: float, add_to_hist: Callable[[Client], None] | None = None):
        self.client = client

        wait_time = time.time() - start_time - client.arrive_time
        call_time = time.time() - start_time

        client.wait_time = wait_time

        if client.action == 'SAQUE':
            self.__transaction_array.append(-client.amount)
        else:
            self.__transaction_array.append(client.amount)

        sleep_start = time.time()
        time.sleep(client.action_time)
        sleep_end = time.time()

        end_time = call_time + sleep_end - sleep_start
        self.client.end_time = end_time

        if add_to_hist:
            add_to_hist(self.client)

        self.client = None
        self.semaphore.release()

    def close_booth(self):
        print(f'Fechando o caixa: {self.id}')
        print(self.__transaction_array)
        threading.Thread(
            target=self.__vault.transaction,
            args=[self.__transaction_array]
        ).start()
