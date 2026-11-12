try:
    amount = int(input("Enter withdrawal amount: "))
except ValueError:
   print("Invalid input, please enter number only") 

else:
    if amount <= 0:
        print("Withdrawal amount must be greater than zero.")
    else:
        with open("transaction_history.txt", "a") as file:
            file.write(f"withdrew {amount} naira\n")

        print("Transaction saved successfully.")  