def get_number():
    try:
        choice = int(input("enter num: "))
        print("valid number")
    except ValueError:
        print("invalid num")
get_number()        
