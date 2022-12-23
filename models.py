# Модель - спец.класс, кот. наследуется от некоего базового класса. Создается с помощью функции declarative_base
# кот. умеет  регистрировать всех своих наследников и по ним создавать таблицы

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


Base = declarative_base()

class Course (Base):
    __tablename__ = 'course'  # имя таблицы, кот. будет создана в Postgres

    id = sq.Column(sq.Integer, primary_key = True) # колонки
    name = sq.Column(sq.String(length=48), Unique = True) # колонки

    # homeworks = relationship('Homework', back_populates = 'course') # чтобы связать две таблицы, необходимо внести изменения и в класс course, и в класс Homework 

    def __str__(self): #для того, чтобы отобразить данные таблицы, кот. вносим, нужно определить метод __str__
        return f' Course {self.id}: {self.name}'


class Homework(Base):
    __tablename__ = "homework"

    id = sq.Column(sq.Integer, primary_key=True)
    number = sq.Column(sq.Integer, nullable=False)
    description = sq.Column(sq.Text, nullable=False)
    course_id = sq.Column(sq.Integer, sq.ForeignKey("course.id"), nullable=False)

    # course = relationship(Course, back_populates="homeworks") # чтобы связать две таблицы, необходимо внести изменения и в класс course, и в класс Homework
    course = relationship(Course, backref="homeworks")  # backref автоматически связывает таблицы ссылкой


    def __str__(self): #для того, чтобы отобразить данные таблицы, кот. вносим, нужно определить метод __str__
        return f' Homework {self.id}: ({self.number}, {self.description}, {self.course_id})'

def create_tables(engine): # функция создания таблиц
    Base.metadata.drop_all(engine) # если БД уже создавалась, удалить все предыдущие данные из нее
    Base.metadata.create_all(engine) # метод создает таблицы, при этом если уже есть таблица, повторно создавать не будет



# создание объектов
js = Course(name="JavaScript")
print(js.id)

hw1 = Homework(number=1, description="первое задание", course=js)
hw2 = Homework(number=2, description="второе задание (сложное)", course=js)

session.add(js)
print(js.id)

session.add_all([hw1, hw2])
session.commit()  # фиксируем изменения
print(js.id)

# Запросы
for c in session.query(Course).join(Homework.course).filter(Homework.number  == 2).all():
    print(c)



# запросы, извлечение данных
q = session.query(Course).join(Homework.course).filter(Homework.number == 1)
print(q)
for s in q.all():
    print(s.id, s.name)
    for hw in s.homeworks:
        print("\t", hw.id, hw.number, hw.description)

# вложенный запрос
subq = session.query(Homework).filter(Homework.description.like("%сложн%")).subquery("simple_hw")
q = session.query(Course).join(subq, Course.id == subq.c.course_id)
print(q)
for s in q.all():
    print(s.id, s.name)
    for hw in s.homeworks:
        print("\t", hw.id, hw.number, hw.description)


# обновление объектов
session.query(Course).filter(Course.name == "JavaScript").update({"name": "NEW JavaScript"})
session.commit()  # фиксируем изменения


# удаление объектов
session.query(Homework).filter(Homework.number > 1).delete()
session.commit()  # фиксируем изменения