import psycopg2
from  sqlalchemy.orm import sessionmaker

DSN = 'postgresql://postgres:yana22@localhost:5432/netology_db' # data source name
engine = sqlalchemy.create_engine(DSN) # объект, кот. может подключиться к базе данных

# сессия - аналог курсора, через него можно добавлять объекты в БД и извлекать данные
Session = sessionmaker(bind = engine) # как бы класс, кот. может создавать сессию
session = Session() # создали экземпляр класса Session



session.close()

