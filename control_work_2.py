
import sqlite3


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        print(f"Имя: {self.name}, возраст: {self.age}")


class Reader(Person):
    def __init__(self, name, age, reader_id=None, borrowed_books=None):
        super().__init__(name, age)
        self.reader_id = reader_id
        self.borrowed_books = borrowed_books or []

    def introduce(self):
        print(f"Читатель: {self.name}, ID: {self.reader_id}")

    def get_info(self):
        print(f"Читатель: {self.name}, возраст: {self.age}")

    def __str__(self):
        return f"{self.name}, {self.age} лет"

    @staticmethod
    def is_adult(age):
        return age >= 18

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["age"],
            data.get("reader_id"),
            data.get("borrowed_books", [])
        )


class Book:
    def __init__(self, title, author, year, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.__copies = copies

    def get_info(self):
        print(f"Книга: {self.title}, автор: {self.author}, год: {self.year}")

    def __str__(self):
        return f"{self.title} — {self.author}"

    @property
    def copies(self):
        return self.__copies

    def change_copies(self, amount):
        if self.__copies + amount >= 0:
            self.__copies += amount
            return True
        return False


class Logger:
    def log_action(self, message):
        print(f"[LOG] {message}")


class Library(Logger):
    def __init__(self):
        self.conn = sqlite3.connect("library.db")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                year INTEGER,
                reader_id INTEGER,
                FOREIGN KEY (reader_id)
                    REFERENCES readers(id)
                    ON DELETE SET NULL
            )
        """)

        self.cursor.execute("""
            CREATE VIEW IF NOT EXISTS borrowed_books AS
            SELECT books.id, books.title, books.author,
                   readers.name AS reader_name
            FROM books
            JOIN readers ON books.reader_id = readers.id
        """)

        self.conn.commit()

    def add_reader(self):
        name = input("Имя читателя: ")
        age = int(input("Возраст: "))

        self.cursor.execute(
            "INSERT INTO readers (name, age) VALUES (?, ?)",
            (name, age)
        )
        self.conn.commit()
        self.log_action("Добавлен читатель")

    def add_book(self):
        title = input("Название книги: ")
        author = input("Автор: ")
        year = int(input("Год выпуска: "))
  
        self.cursor.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year)
        )
        self.conn.commit()
        self.log_action("Добавлена книга")

    def show_readers(self):
        self.cursor.execute("SELECT * FROM readers")
        rows = self.cursor.fetchall()

        for row in rows:
            reader = Reader(row[1], row[2], row[0])
            reader.get_info()

    def show_books(self):
        self.cursor.execute("""
            SELECT books.id, books.title, books.author,
                   books.year, readers.name
            FROM books
            LEFT JOIN readers ON books.reader_id = readers.id
        """)
        rows = self.cursor.fetchall()

        for row in rows:
            book = Book(row[1], row[2], row[3])
            print(f"ID: {row[0]}, {book}, год: {row[3]}")
            if row[4]:
                print(f"Выдана читателю: {row[4]}")
            else:
                print("Книга свободна")

    def update_book(self):
        book_id = int(input("ID книги: "))
        title = input("Новое название: ")
        author = input("Новый автор: ")
        year = int(input("Новый год: "))

        self.cursor.execute("""
            UPDATE books
            SET title = ?, author = ?, year = ?
            WHERE id = ?
        """, (title, author, year, book_id))

        self.conn.commit()
        self.log_action("Информация о книге изменена")

    def delete_book(self):
        book_id = int(input("ID книги для удаления: "))

        self.cursor.execute(
            "DELETE FROM books WHERE id = ?", (book_id,)
        )
        self.conn.commit()
        self.log_action("Книга удалена")

    def give_book(self):
        book_id = int(input("ID книги: "))
        reader_id = int(input("ID читателя: "))

        self.cursor.execute(
            "SELECT reader_id FROM books WHERE id = ?", (book_id,)
        )
        book = self.cursor.fetchone()

        self.cursor.execute(
            "SELECT id FROM readers WHERE id = ?", (reader_id,)
        )
        reader = self.cursor.fetchone()

        if book is None:
            print("Книга не найдена")
        elif reader is None:
            print("Читатель не найден")
        elif book[0] is not None:
            print("Книга уже выдана")
        else:
            self.cursor.execute(
                "UPDATE books SET reader_id = ? WHERE id = ?",
                (reader_id, book_id)
            )
            self.conn.commit()
            self.log_action("Книга выдана читателю")

    def return_book(self):
        book_id = int(input("ID возвращаемой книги: "))

        self.cursor.execute(
            "SELECT reader_id FROM books WHERE id = ?", (book_id,)
        )
        book = self.cursor.fetchone()

        if book is None:
            print("Книга не найдена")
        elif book[0] is None:
            print("Книга уже находится в библиотеке")
        else:
            self.cursor.execute(
                "UPDATE books SET reader_id = NULL WHERE id = ?",
                (book_id,)
            )
            self.conn.commit()
            self.log_action("Книга возвращена")

    def count_books(self):
        self.cursor.execute("SELECT COUNT(*) FROM books")
        print("Всего книг:", self.cursor.fetchone()[0])

    def books_by_author(self):
        self.cursor.execute("""
            SELECT author, COUNT(*)
            FROM books
            GROUP BY author
        """)

        for row in self.cursor.fetchall():
            print(f"Автор: {row[0]}, книг: {row[1]}")

    def books_above_average_year(self):
        self.cursor.execute("""
            SELECT title, author, year
            FROM books
            WHERE year > (
                SELECT AVG(year) FROM books
            )
        """)

        for row in self.cursor.fetchall():
            print(f"{row[0]} — {row[1]}, {row[2]}")

    def show_borrowed_books(self):
        self.cursor.execute("SELECT * FROM borrowed_books")

        for row in self.cursor.fetchall():
            print(
                f"ID: {row[0]}, книга: {row[1]}, "
                f"автор: {row[2]}, читатель: {row[3]}"
            )

    def close(self):
        self.conn.close()


library = Library()

while True:
    print("""
    ===== БИБЛИОТЕКА =====
    1. Добавить читателя
    2. Добавить книгу
    3. Показать читателей
    4. Показать книги
    5. Изменить книгу
    6. Удалить книгу
    7. Выдать книгу
    8. Вернуть книгу
    9. Количество книг
    10. Количество книг каждого автора
    11. Книги новее среднего года
    12. Показать выданные книги
    0. Выход
    """)

    choice = input("Выберите действие: ")

    if choice == "1":
        library.add_reader()
    elif choice == "2":
        library.add_book()
    elif choice == "3":
        library.show_readers()
    elif choice == "4":
        library.show_books()
    elif choice == "5":
        library.update_book()
    elif choice == "6":
        library.delete_book()
    elif choice == "7":
        library.give_book()
    elif choice == "8":
        library.return_book()
    elif choice == "9":
        library.count_books()
    elif choice == "10":
        library.books_by_author()
    elif choice == "11":
        library.books_above_average_year()
    elif choice == "12":
        library.show_borrowed_books()
    elif choice == "0":
        library.close()
        print("Программа завершена")
        break
    else:
        print("Неверный выбор")
