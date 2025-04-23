import threading
import time
import random

class LotteryBooth:
    def __init__(self, booth_id):
        self.id = booth_id
        self.semaphore = threading.Semaphore(1)
        
    def serve(self, client_id, job_time):
        print(f"Cliente {client_id} entrou na cabine {self.id}")
        time.sleep(job_time)
        print(f"Cliente {client_id} saiu da cabine {self.id}")

def client_task(client_id, booths, job_time):
    while True:
        random.shuffle(booths)
        for booth in booths:
            if booth.semaphore.acquire(blocking=False):
                try:
                    booth.serve(client_id, job_time)
                    return 
                finally:
                    booth.semaphore.release()
        time.sleep(0.1)

if __name__ == "__main__":
    booths = [LotteryBooth(i) for i in range(1, 5)]
    
    clients = []
    for client_id in range(1, 11):
        t = threading.Thread(target=client_task, args=(client_id, booths, 2))
        t.start()
        clients.append(t)
    
    for t in clients:
        t.join()

    print("Todos os clientes foram atendidos.")
