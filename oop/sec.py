class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def show_balance(self):
        print(self.__balance)

    def set_balance(self, new_balance):
        if new_balanceb >= 0:
            self.__balance = new_balance
        else:
            print("invalid balance")    




account1 = BankAccount(50000)

account1.show_balance()

account1.set_balance(70000)

account1.show_balance()