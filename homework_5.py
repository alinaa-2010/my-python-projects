
import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        grade REAL
    )
''')

conn.commit()


def add_student():
    try:
        name = input('Введите имя студента: ')
        if not name.strip():
            print('Имя не может быть пустым!')
            return

        age = int(input('Введите возраст: '))
        grade = float(input('Введите оценку: '))

        cursor.execute(
            'INSERT INTO students (name, age, grade) VALUES (?, ?, ?)',
            (name, age, grade)
        )

        conn.commit()
        print('Студент успешно добавлен!')

    except ValueError:
        print('Ошибка! Введите возраст числом, а оценку числом.')


def show_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()

    if not students:
        print('Список студентов пуст.')
        return

    for student in students:
        print(student)


def find_student():
    try:
        student_id = int(input('Введите ID студента: '))

        cursor.execute(
            'SELECT * FROM students WHERE id = ?',
            (student_id,)
        )

        student = cursor.fetchone()

        if student:
            print(student)
        else:
            print('Студент не найден.')

    except ValueError:
        print('Ошибка! ID должен быть числом.')


def update_student():
    try:
        student_id = int(input('Введите ID студента: '))

        cursor.execute(
            'SELECT * FROM students WHERE id = ?',
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print('Студент не найден.')
            return

        print('Текущие данные:', student)

        name = input('Введите новое имя: ')
        if not name.strip():
            print('Имя не может быть пустым!')
            return

        age = int(input('Введите новый возраст: '))
        grade = float(input('Введите новую оценку: '))

        cursor.execute('''
            UPDATE students
            SET name = ?, age = ?, grade = ?
            WHERE id = ?
        ''', (name, age, grade, student_id))

        conn.commit()
        print('Данные студента успешно изменены!')

    except ValueError:
        print('Ошибка! Проверьте правильность введённых данных.')


def delete_student():
    try:
        student_id = int(input('Введите ID студента: '))

        cursor.execute(
            'SELECT * FROM students WHERE id = ?',
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print('Студент не найден.')
            return

        cursor.execute(
            'DELETE FROM students WHERE id = ?',
            (student_id,)
        )

        conn.commit()
        print('Студент успешно удалён!')

    except ValueError:
        print('Ошибка! ID должен быть числом.')


while True:
    print('\n--- МЕНЮ УПРАВЛЕНИЯ СТУДЕНТАМИ ---')
    print('1. Добавить студента')
    print('2. Показать всех студентов')
    print('3. Найти студента по ID')
    print('4. Изменить данные студента')
    print('5. Удалить студента')
    print('6. Выйти из программы')

    choice = input('Выберите действие: ')

    if choice == '1':
        add_student()
    elif choice == '2':
        show_students()
    elif choice == '3':
        find_student()
    elif choice == '4':
        update_student()
    elif choice == '5':
        delete_student()
    elif choice == '6':
        conn.close()
        print('Программа завершена.')
        break
    else:
        print('Неверный пункт меню! Выберите от 1 до 6.')
