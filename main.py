import sqlite3

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    price INTEGER
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    balance INTEGER
    )""")

class Store:

    def __init__(self, name, balance, admin_name):
        self.name = name
        self.balance = balance
        self.admin_name = admin_name
    
    def register(self):
        cursor = connect.cursor()
        cursor.execute(f"""INSERT INTO users(name, balance) VALUES ('{self.name}', {self.balance})""")
        connect.commit()
        print(f"Добро пожаловать, {self.name}")

    def create_admins_table(self):
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS admins(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100)
            )""")
        connect.commit()

    def add_admins(self, admin_names):
        cursor = connect.cursor()
        admins = [(name,) for name in admin_names]
        cursor.executemany("INSERT INTO admins(name) VALUES (?)", admins)
        connect.commit()
        print("Администраторы успешно добавлены")
        
    def add_product(self, product_name, product_price):
        cursor = connect.cursor()
        cursor.execute(f"INSERT INTO products(name, price) VALUES ('{product_name}', {product_price})")
        connect.commit()
        print(f"Уважаемый {self.admin_name}, вы успешно добавили {product_name} по цене {product_price}")

    def buy(self, product_name):
        cursor = connect.cursor()
        cursor.execute(f"SELECT name, price FROM products WHERE name = '{product_name}'")
        product = cursor.fetchone()

        if product:
            product_name, price = product
            if self.balance >= price:
                cursor.execute(f"UPDATE users SET balance = balance - {price} WHERE name = '{self.name}'")
                connect.commit()
                self.balance -= price
                print(f"Вы успешно купили товар: {product_name}. Ваш баланс: {self.balance}")
            else:
                print("Недостаточно средств!")
        else:
            print("Товар не найден")
    
    def main(self):
        while True:
            command = input("""1 - регистрация
2 - добавление продукта
3 - покупка продукта
4 - информация
5 - выход
""")
            if command == '1':
                self.register()
            elif command == '2':
                if self.admin_name in self.get_admin_names():
                    product_name = input("Введите название продукта: ")
                    product_price = int(input("Введите цену продукта: "))
                    self.add_product(product_name, product_price)
                else:
                    print("У вас нет прав на добавление продукта.")
            elif command == '3':
                product_name = input("Введите название продукта для покупки: ")
                self.buy(product_name)
            elif command == '4':
                print(f"Имя магазина: {self.name}")
                print(f"Ваш баланс: {self.balance}")
            elif command == '5':
                print("Выход из программы.")
                break

    def get_admin_names(self):
        cursor = connect.cursor()
        cursor.execute("SELECT name FROM admins")
        admin_names = [row[0] for row in cursor.fetchall()]
        return admin_names

store = Store("Hikmatillo", 1000, "Hikmatillo")  # Используйте имя администратора из вашего списка

store.create_admins_table()
admin_names = ["Hikmatillo", "Nurbolot"]
store.add_admins(admin_names)

store.main()

connect.close()




