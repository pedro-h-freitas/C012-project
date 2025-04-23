class Client:
    def __init__(self, category: str, amount: int, action: str):
        self.category = category
        self.action = action
        self.amount = amount

    def get_time(self, action: str):
        time = {
            "SAQUE":1,
            "DEPOSITO":2,
            "APOSENTADORIA":3,
            "CONTA":4,
            "2° VIA":5,
            "TIGRINHO":6
        }
        return time[action]

    def get_priority(self, category: str):
        priority = {
            "IDOSO":1,
            "PCD": 2,
            "GRAVIDA":3,
            "ADULTO":4
        }
        return priority[category]