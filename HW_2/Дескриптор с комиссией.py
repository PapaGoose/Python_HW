class Value:
    def __set__(self, obj, value):
        self.amount = value
        self.com = obj

    def __get__(self, obj, obj_type):
        return int(self.amount * (1 - self.com.commission))


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
