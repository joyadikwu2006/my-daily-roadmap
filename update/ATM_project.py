def withdraw():
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

def view_history():
    try:
        with open("transaction_history.txt", "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("no transaction history found")

def main():
    while True:
        print("\nWelcome to our ATM\n")
        print("1. withdraw")
        print("2. view history")
        print("Q. Quit")

        choice = input("Enter input: ")
        if choice == "1":
            withdraw()
        elif choice == "2":
            view_history()
        elif choice.lower() == "q":
            print("thanks for using our ATM")
            break
        else:
            print("Invalid input, try again") 
main()                    



