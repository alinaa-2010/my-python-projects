# class Transport:
#     def move(self):
#         return "Транспорт движется"

# class Car(Transport):
#     def move(self):
#         return "Машина едет"

# class Bike(Transport):
#     def move(self):
#         return "Велосипед едет"

# class Boat(Transport):
#     def move(self):
#         return "Лодка плывет"

# class Plane(Transport):
#     def move(self):
#         return "Самолет летит"

# transports = [Car(), Bike(), Boat(), Plane()]

# for transport in transports:
#     print(transport.move())

# №1

# class Notification:
#     def send(self):
#         return "Отправка уведомления"

# class Email_Notification(Notification):
#     def send(self):
#         return "Отправка Email"

# class SMS_Notification(Notification):
#     def send(self):
#         return "Отправка SMS"

# class Telegram_Notification(Notification):
#     def send(self):
#         return "Отправка сообщения в Telegram"

# notifications = [
#     Email_Notification(),
#     SMS_Notification(),
#     Telegram_Notification()
# ]

# for notification in notifications:
#     print(notification.send())

# №2

class Figure:
    def area(self):
        return "Площадь фигуры"

class Square(Figure):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Rectangle(Figure):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Figure):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

figures = [
    Square(5),
    Rectangle(4, 6),
    Circle(3)
]

for figure in figures:
    print(figure.area())