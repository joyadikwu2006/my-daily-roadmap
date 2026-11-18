class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduction(self):
        print(f" my name is {self.name}, and i am {self.age} years old.")    
student1 = Student("diamond", 21)
student2 = Student("john", 20)
student1.introduction()
student2.introduction()