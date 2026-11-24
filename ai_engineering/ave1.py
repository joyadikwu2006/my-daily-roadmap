def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    total = 0

    for number in numbers:
        total += number
    average = total / len(numbers)
    return average
scores = []
print(calculate_average(scores))