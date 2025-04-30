import threading


class lottery_vault:
    def __init__(self):
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.amount = 0

    def deposit_withdraw_money(self, thread_number, is_deposit, amount):
        with self.lock:
            if is_deposit:
                self.amount += amount
            else:
                self.amount -= amount
            print(f"Incremented to {self.amount} - Thread {thread_number}")
