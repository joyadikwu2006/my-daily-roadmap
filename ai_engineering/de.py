#def get_discount(price):
 # return price * 0.2


#def final_price(price):
 # discount = get_discount(price)
 # return price - discount
#print(final_price(5000))


def calculate_total(numbers):
    total = 0
    for number in numbers:
        total = total + number
    return total
prices = [200, 300, 500, 1000]
print(calculate_total(prices))        
