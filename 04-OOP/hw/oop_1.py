"""
Необходимо создать 3 класса и взаимосвязь между ними (Student, Teacher,
Homework)
Наследование в этой задаче использовать не нужно.
Для работы с временем использовать модуль datetime

1. Homework принимает на вход 2 атрибута: текст задания и количество дней
на это задание
Атрибуты:
    text - текст задания
    deadline - хранит объект datetime.timedelta с количеством
    дней на выполнение
    created - c точной датой и временем создания
Методы:
    is_active - проверяет не истело ли время на выполнение задания,
    возвращает boolean

2. Student
Атрибуты:
    last_name
    first_name
Методы:
    do_homework - принимает объект Homework и возвращает его же,
    если задание уже просрочено, то печатет 'You are late' и возвращает None

3. Teacher
Атрибуты:
     last_name
     first_name
Методы:
    create_homework - текст задания и количество дней на это задание,
    возвращает экземпляр Homework
    Обратите внимание, что для работы этого метода не требуется сам объект.

PEP8 соблюдать строго, проверку делаю автотестами и просмотром кода.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""

import datetime


class Homework:
    """
    Represent information about homework.
    :text - text of hw
    :deadline - deadline of hw
    :created - auto attribute that takes timestamp when hw was created
    """
    def __init__(self, text: str, deadline: int):
        self.text = text
        self.deadline = datetime.timedelta(days=deadline)
        self.created = datetime.datetime.now()

    def is_active(self):
        return (datetime.datetime.now() - self.created) < self.deadline


class Student:
    """
    Represent information about student.
    available attributes:
    :first_name
    :last_name
    available methods:
    :do_homework(Homework()) -> returns "You are late"
    if deadline of hw is passed
    """
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def do_homework(homework: Homework):
        return homework if homework.is_active() else print("You are late!")


class Teacher:
    """
    Represent information about teacher.
    available attributes:
    :first_name
    :last_name
    available methods:
    :create_homework -> returns Homework object
    """
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def create_homework(text: str, days: int):
        return Homework(text, days)

if __name__ == '__main__':

    student = Student('Roman', 'Petrov')
    teacher = Teacher('Daniil', 'Shadrin')
    print(teacher.last_name, teacher.first_name)  # Shadrin
    print(student.first_name, student.last_name)  # Roman

    expired_homework = teacher.create_homework('Learn functions', 0)
    print(expired_homework.created)  # Example: 2019-05-26 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'
    print(expired_homework.is_active())

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    print(oop_homework.text)
    print(oop_homework.deadline)  # 5 days, 0:00:00

    print(student.do_homework(oop_homework))
    print(student.do_homework(expired_homework))  # You are late
