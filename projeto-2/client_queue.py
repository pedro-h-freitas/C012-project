from client import Client
from typing import Literal


class ClientQueue:
    def __init__(self, scheduling: Literal['SJF', 'PS'], clients: list[Client] = []):
        self.clients = clients
        self.scheduling = scheduling

    def __order(self):
        if self.scheduling == 'SJF':
            self.clients = sorted(self.clients, key=lambda c: c.action_time)
        elif self.scheduling == 'PS':
            self.clients = sorted(self.clients, key=lambda c: c.priority)

    def get_next(self):
        if self.clients:
            return self.clients.pop(0)

    def get_clients(self) -> list[Client]:
        return self.clients.copy()

    def add_client(self, client: Client):
        self.clients.append(client)
        self.__order()
        return self.clients


if __name__ == "__main__":
    queue = ClientQueue('PS')

    print('-----------')
    print(f'Fila vazia: {queue.get_next()}\n\n')

    print(f'Adicionando Clientes na fila')
    for client in queue.add_client(Client("ADULTO", 1000, "2° VIA", 1)):
        print(client)
    print('-----------\n\n-----------')

    print(f'Pegando o Próximo da fila')
    print(queue.get_next())
    print('-----------\n\n-----------')

    print(f'Listando clientes na fila')
    for client in queue.get_clients():
        print(client)
    print('-----------\n\n-----------')

    print(f'Adicionando Clientes na fila')
    for client in queue.add_client(Client("ADULTO", 1000, "CONTA", 1)):
        print(client)
    print('-----------\n\n-----------')

    print(f'Adicionando Clientes na fila')
    for client in queue.add_client(Client("ADULTO", 1000, "DEPOSITO", 1)):
        print(client)
    print('-----------')
