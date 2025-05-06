import threading
import time


class LotteryVault:
    def __init__(self, initial_amount=0, with_lock: bool = True):
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.amount = initial_amount

        self.__with_lock = with_lock
        self.__transaction_var = 0

    def deposit_withdraw_money(self, thread_number, is_deposit, amount):
        with self.lock:
            if is_deposit:
                self.amount += amount
            else:
                self.amount -= amount
            print(f"Incremented to {self.amount} - Thread {thread_number}")

    def transaction(self, arr):
        if self.__with_lock:
            return self.transaction_with_lock(arr)
        self.transaction_without_lock(arr)

    def transaction_with_lock(self, arr):
        with self.lock:
            self.__transaction_var = 0
            for i in arr:
                self.__transaction_var += i
                time.sleep(0.5)

            self.amount += self.__transaction_var

    def transaction_without_lock(self, arr):
        self.__transaction_var = 0
        for i in arr:
            self.__transaction_var += i
            time.sleep(0.5)

        self.amount += self.__transaction_var
