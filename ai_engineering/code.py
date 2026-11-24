def check_grade(score):
    if score >= 80:
        return("A")
    elif score >= 70:
        return("B")
    elif score >= 60:
        return("C")
    elif score >= 50:
        return("D")
    else:
        return("F")    
score = 85
print(check_grade(score))

score = 75
print(check_grade(score))

score = 65
print(check_grade(score))

score = 55
print(check_grade(score))

score = 40
print(check_grade(score))