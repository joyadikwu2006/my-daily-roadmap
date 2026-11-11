class InsufficientFundsError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

def withdraw(balance, amount):
    if amount <= 0:
        raise InvalidAmountError("Withdrawal amount must be greater than zero.")

    if amount > balance:
        raise InsufficientFundsError("Insufficient funds.")

    return balance - amount

balance = 50000

print("\n===Welcome to the ATM===")
print("your current balance is:", balance)

try:
    amount = int(input("Enter amount to withdraw: "))
    print("you requested:", amount)

    balance = withdraw(balance, amount)   
except ValueError:
    print("invalid input. Please enter number only")
except InsufficientFundsError as error:
    print(error)
except InvalidAmountError as error:
    print(error)
else:
    print("Withdrawal successful.")
    print("remaining balance:", balance) 
    print("Transaction completed successfully.")
finally:
    print("Thank you for using our ATM.")

