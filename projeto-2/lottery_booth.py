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

    def draw(self, stdsrc: curses.window, y: int, x: int):
        stdsrc.attron(curses.color_pair(self.color))
        stdsrc.addstr(y, x, "┌─────┐")
        stdsrc.addstr(y+1, x, "│     │")
        stdsrc.addstr(y+2, x, "├─────┤")
        stdsrc.addstr(y+3, x, "│     │")
        stdsrc.attroff(curses.color_pair(self.color))

        stdsrc.addstr(y+1, x+2, "😊")

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


# Testing
def client_task(booths: list[LotteryBooth], client):
    while True:
        random.shuffle(booths)
        for booth in booths:
            if booth.semaphore.acquire(blocking=False):
                booth.serve(client)
                return

        time.sleep(0.1)


if __name__ == "__main__":
    booths = [LotteryBooth(i, 1) for i in range(1, 5)]

    clients = [
        Client(category='PCD', action='CONTA', amount=428, arrive_time=5),
        Client(category='ADULTO', action='DEPOSITO',
               amount=915, arrive_time=12),
        Client(category='IDOSO', action='SAQUE', amount=157, arrive_time=3),
        Client(category='GRAVIDA', action='2° VIA', amount=602, arrive_time=8),
        Client(category='ADULTO', action='MEGA-SENA',
               amount=329, arrive_time=20),
        Client(category='PCD', action='APOSENTADORIA',
               amount=774, arrive_time=1),
        Client(category='IDOSO', action='DEPOSITO',
               amount=241, arrive_time=15),
        Client(category='GRAVIDA', action='SAQUE', amount=88, arrive_time=7),
        Client(category='ADULTO', action='CONTA', amount=503, arrive_time=18),
        Client(category='PCD', action='MEGA-SENA', amount=640, arrive_time=0)
    ]

    threads = []
    for c in clients:
        print(c)
        t = threading.Thread(target=client_task, args=(booths, c))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("Todos os clientes foram atendidos.")
