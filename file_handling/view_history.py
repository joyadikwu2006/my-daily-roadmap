with open("transaction_history.txt", "r") as file:
    for line in file:
        print(line.strip())