def calculate_average(numbers):
    total = 0

    for number in numbers:
        total += number
    average = total / len(numbers)
    return average
scores = [70, 80, 90, 100]
print(calculate_average(scores))