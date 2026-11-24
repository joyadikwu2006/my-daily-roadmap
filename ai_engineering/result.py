def process_results(score):
    if not score:
        return "No score provided"
    total = 0
    for num in score:
        total += num
    average = total / len(score)
    if average >= 50:
        return "pass"
    else:
            return "fail"
print(process_results([40, 60, 80]))
print(process_results([20, 30, 40]))
print(process_results([]))