from client import Client

class Queue:
    def __init__(self, clients: list[Client], scheduling: str):
        self.clients = clients
        self.scheduling = scheduling
    
    def __order(self):
        if self.scheduling == 'SJF':
            self.clients = sorted(self.clients, key=lambda c: c.get_time())
        elif self.scheduling == 'PS':
            self.clients = sorted(self.clients, key=lambda c: c.get_priority())

    def get_next(self):
        return self.clients.pop(0)

    def get_clients(self):
        return self.clients
    
    def add_client(self, client: Client):
        self.clients.append(client)
        self.__order()
        return self.clients
    
if __name__ == "__main__":
    clients = [Client("IDOSO", 1000, "SAQUE"),
            Client("PCD", 1000, "TIGRINHO"),
            Client("GRAVIDA", 1000, "APOSENTADORIA")]

    queue = Queue(clients, 'SJF')

    for client in queue.add_client(Client("ADULTO", 1000, "2° VIA")):
        print(client)
    print('-----------')

    print(queue.get_next())
    print('-----------')
    for client in queue.get_clients():
        print(client)
    print('-----------')
    for client in queue.add_client(Client("ADULTO", 1000, "CONTA")):
        print(client)
    print('-----------')
    for client in queue.add_client(Client("ADULTO", 1000, "DEPOSITO")):
        print(client)
    print('-----------')

