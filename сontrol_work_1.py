from abc import ABC, abstractmethod


def show_message(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("Действие выполнено")
        return result

    return wrapper


class Product(ABC):

    def __init__(self, name, price, quantity, category):
        self.name = name
        self.__price = price
        self.__quantity = quantity
        self.category = category
        self.__id = id(self)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value >= 0:
            self.__price = value
        else:
            print("Цена не может быть отрицательной")

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if value >= 0:
            self.__quantity = value
        else:
            print("Количество не может быть отрицательным")

    @abstractmethod
    def get_info(self):
        pass

    def change_quantity(self, value):
        if self.__quantity + value >= 0:
            self.__quantity += value
        else:
            print("Недостаточно товара на складе")

    def get_total_price(self, count):
        return self.__price * count


class Book(Product):

    def __init__(self, name, price, quantity, category, author):
        super().__init__(name, price, quantity, category)
        self.author = author

    def get_info(self):
        return f"Книга: {self.name}, автор: {self.author}, цена: {self.price}, количество: {self.quantity}"


class Phone(Product):

    def __init__(self, name, price, quantity, category, manufacturer):
        super().__init__(name, price, quantity, category)
        self.manufacturer = manufacturer

    def get_info(self):
        return f"Телефон: {self.name}, производитель: {self.manufacturer}, цена: {self.price}, количество: {self.quantity}"


class Clothes(Product):

    def __init__(self, name, price, quantity, category, size):
        super().__init__(name, price, quantity, category)
        self.size = size

    def get_info(self):
        return f"Одежда: {self.name}, размер: {self.size}, цена: {self.price}, количество: {self.quantity}"


class Cart:

    def __init__(self):
        self.items = {}

    @show_message
    def add_product(self, product, quantity):
        if quantity <= 0:
            print("Количество должно быть больше 0")
            return

        if product.quantity >= quantity:
            self.items[product] = self.items.get(product, 0) + quantity
            product.change_quantity(-quantity)
            print(f"{product.name} добавлен в корзину")
        else:
            print("Недостаточно товара на складе")

    def remove_product(self, product):
        if product in self.items:
            quantity = self.items[product]
            product.change_quantity(quantity)
            del self.items[product]
            print(f"{product.name} удалён из корзины")
        else:
            print("Товара нет в корзине")

    def change_quantity(self, product, quantity):
        if product not in self.items:
            print("Товара нет в корзине")
            return

        if quantity <= 0:
            print("Количество должно быть больше 0")
            return

        old_quantity = self.items[product]
        difference = quantity - old_quantity

        if difference > 0:
            if product.quantity >= difference:
                product.change_quantity(-difference)
                self.items[product] = quantity
            else:
                print("Недостаточно товара на складе")

        elif difference < 0:
            product.change_quantity(-difference)
            self.items[product] = quantity

    def show_cart(self):
        print("\nКорзина:")

        if not self.items:
            print("Корзина пустая")
            return

        for product, quantity in self.items.items():
            print(
                f"{product.name} — {quantity} шт. — "
                f"{product.price * quantity} сом"
            )

    def get_total(self):
        total = 0

        for product, quantity in self.items.items():
            total += product.get_total_price(quantity)

        return total


class User:

    def __init__(self, name, email):
        self.__name = name
        self.email = email
        self.cart = Cart()

    def add_product(self, product, quantity):
        self.cart.add_product(product, quantity)

    def remove_product(self, product):
        self.cart.remove_product(product)

    def show_cart(self):
        self.cart.show_cart()

    def order(self):
        total = self.cart.get_total()

        if total == 0:
            print("Корзина пустая")
        else:
            print(f"Заказ оформлен на сумму: {total} сом")
            self.cart.items.clear()


book = Book(
    "Гарри Поттер",
    800,
    10,
    "Книги",
    "Дж. Роулинг"
)

phone = Phone(
    "iPhone 14 pro max",
    70000,
    5,
    "Телефоны",
    "Apple"
)

clothes = Clothes(
    "Футболка",
    1000,
    8,
    "Одежда",
    "M"
)

products = [book, phone, clothes]

print("ТОВАРЫ:")

for product in products:
    print(product.get_info())


user = User(
    "Алина",
    "alina@gmail.com"
)

print("\nДОБАВЛЕНИЕ В КОРЗИНУ:")

user.add_product(book, 2)
user.add_product(clothes, 1)

user.show_cart()

print(f"\nОбщая стоимость: {user.cart.get_total()} сом")
print("\nУДАЛЕНИЕ ТОВАРА:")

user.remove_product(clothes)
user.show_cart()

print("\nОФОРМЛЕНИЕ ЗАКАЗА:")
user.order()

