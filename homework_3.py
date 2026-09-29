from abc import ABC, abstractmethod

class Transport(ABC):

    @abstractmethod
    def move(self):
        pass

class Car(Transport):

    def __init__(self, speed):
        self.__speed = speed

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if value < 0:
            self.__speed = 0
        elif value > 300:
            self.__speed = 300
        else:
            self.__speed = value

    def move(self):
        print(f"car moves at {self.speed} км/ч")

class Bike(Transport):

    def move(self):
        print("Bike moved")

class Bus(Transport):

    def move(self):
        print("Bus moved")

def main():
    car = Car(100)
    bike = Bike()
    bus = Bus()

    car.move()
    bike.move()
    bus.move()

main()