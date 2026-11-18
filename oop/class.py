class Animal:
    def eat(self):
        print("the animal is eating")

class Dog(Animal):
    def bark(self):
        print("the dog is barking")

dog1 = Dog()

dog1.eat()
dog1.bark()