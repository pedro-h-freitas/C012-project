import threading
import time
import random
import client as c_module

class LotteryBooth:
    def __init__(self, booth_id):
        self.id = booth_id
        self.semaphore = threading.Semaphore(1)
        
    def serve(self, category, amount, job_time):
        print(f"ENTRADA - CABINE {self.id} - {category} - {amount} reais")
        time.sleep(job_time)
        print(f"SAÍDA - CABINE {self.id} - {category} - {amount} reais")

def client_task(booths, category, amount, job_time):
    while True:
        random.shuffle(booths)
        for booth in booths:
            if booth.semaphore.acquire(blocking=False):
                try:
                    booth.serve(category, amount, job_time)
                    return 
                finally:
                    booth.semaphore.release()
        time.sleep(0.1)

if __name__ == "__main__":
    booths = [LotteryBooth(i) for i in range(1, 5)]
    
    clients = []
    for c in c_module.clients:
        c = c_module.clients[c]
        t = threading.Thread(target=client_task, args=(
            booths, 
            f"{c["category"]} - {c["action"]}", 
            c["amount"], 
            c_module.Client.get_time(c_module.Client, c["action"])
        ))
        t.start()
        clients.append(t)
    
    for t in clients:
        t.join()

    print("Todos os clientes foram atendidos.")
