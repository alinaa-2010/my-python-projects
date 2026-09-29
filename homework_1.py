# class BankAccount:
#     def __init__(self, owner, balance):
#         self.owner = owner
#         self.balance = balance

#     def deposit(self, amount):
#         self.balance += amount

#     def withdraw(self, amount):
#         self.balance -= amount

# account = BankAccount("Beksultan", 1000)

# account.deposit(500)
# account.withdraw(200)

# print(account.balance)

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def buy(self, amount):
        self.quantity -= amount

    def add(self, amount):
        self.quantity += amount

    def get_total_price(self):
        return self.price * self.quantity

product = Product("Ноутбук", 50000, 5) 

product.buy(2) 
product.add(3) 

print(product.quantity) 
print(product.get_total_price())