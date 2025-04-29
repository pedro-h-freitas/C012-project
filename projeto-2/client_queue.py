from client import Client
from typing import Literal


class ClientQueue:
    def __init__(self, scheduling: Literal['SJF', 'PS'], clients: list[Client] = []):
        self.clients = clients
        self.scheduling = scheduling

    def __order(self):
        if self.scheduling == 'SJF':
            self.clients = sorted(self.clients, key=lambda c: c.get_time())
        elif self.scheduling == 'PS':
            self.clients = sorted(self.clients, key=lambda c: c.get_priority())

    def get_next(self):
        return self.clients.pop(0)

    def get_clients(self) -> list[Client]:
        return self.clients.copy()

    def add_client(self, client: Client):
        self.clients.append(client)
        self.__order()
        return self.clients


if __name__ == "__main__":
    clients = [Client("IDOSO", 1000, "SAQUE", 4),
               Client("PCD", 1000, "MEGA-SENA", 4),
               Client("GRAVIDA", 1000, "APOSENTADORIA", 6)]

    queue = ClientQueue('SJF', clients)

    for client in queue.add_client(Client("ADULTO", 1000, "2° VIA", 1)):
        print(client)
    print('-----------')

    print(queue.get_next())
    print('-----------')
    for client in queue.get_clients():
        print(client)
    print('-----------')
    for client in queue.add_client(Client("ADULTO", 1000, "CONTA", 1)):
        print(client)
    print('-----------')
    for client in queue.add_client(Client("ADULTO", 1000, "DEPOSITO", 1)):
        print(client)
    print('-----------')
