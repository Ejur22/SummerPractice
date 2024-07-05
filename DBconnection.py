from parsing import get_vacancies
import sqlalchemy as db
from bs4 import BeautifulSoup
import requests
import psycopg2

#postgresql://postgres:123@localhost/ParserDatabase

db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres' ,
    'host': 'localhost',
    'port': '5555'
}



vacancies_array = get_vacancies("Питон разработчик", 5, 1)

engine = db.create_engine('postgresql://postgres:123@localhost/ParserDatabase', echo=True)
conn = engine.connect()
metadata = db.MetaData()

vacancies = db.Table('vacancies', metadata,
                     db.Column('id', db.Integer, primary_key=True),
                     db.Column('title', db.Text),
                     db.Column('experience', db.Text),
                     db.Column('salary', db.Text),
                     db.Column('city', db.Text),
                     db.Column('subway', db.Text),
                     db.Column('company', db.Text),
                     db.Column('link', db.Text))

metadata.create_all(engine)

vacancies_query = vacancies.insert().values(vacancies_array)

conn.execute(vacancies_query)
conn.commit()

