# Модель - спец.класс, кот. наследуется от некоего базового класса. Создается с помощью функции declarative_base
# кот. умеет  регистрировать всех своих наследников и по ним создавать таблицы

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Course, Homework

DSN = "postgresql://postgres:yana22@localhost:5432/netology_db_models"
engine = sq.create_engine(DSN)

create_tables(engine) # вызвали функцию создания таблиц

# сессия
Session = sessionmaker(bind=engine)
session = Session()


course1 = Course(name='Python')


session.add(course1)
session.commit()
print(course1)

session.close()
