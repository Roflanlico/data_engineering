import os
import sqlite3
import json
import csv
import pandas as pd

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB1")

def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def drop_table(connection):
    connection.execute('''DROP TABLE IF EXISTS table1; ''')
    
def create_table(connection):
    connection.execute('''
CREATE TABLE table1 (
    id         INTEGER    PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE,
    title       TEXT (256) NOT NULL,
    author    TEXT (256) NOT NULL,
    genre       TEXT (256) NOT NULL,
    pages    INTEGER    NOT NULL,
    published_year     INTEGER    NOT NULL,
    isbn       TEXT (256)    NOT NULL,
    rating     FLOAT    NOT NULL,
    views       INTEGER    NOT NULL 
);
''')
    
def insert_data(connection, data):
    print(data)
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table1 (title, author, genre, pages, published_year, isbn, rating, views) 
        VALUES(:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)
        """, data
    )
    connection.commit()
    cursor.close()

def topPages(connection, top=80):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        ORDER BY pages DESC LIMIT ?
        ''', [top]
    )   
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close() 
    return items

def views(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            SUM(views) as sum,
            AVG(views) as avg,
            MIN(views) as min, 
            MAX(views) as max
        FROM table1
        '''
    )
    res = dict(res.fetchone())
    cursor.close()
    return res

def genreFreq(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM table1) as count,
            genre
        FROM table1
        GROUP BY genre
        '''
    )

    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))

    cursor.close()
    return stat_freq

def topRating(connection, rating = 3.5, top=80):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        WHERE rating >= ?
        ORDER BY author DESC LIMIT ?
        ''', [rating, top]
    )
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    
    return items


connection = connect(dbPath)


df = pd.read_csv('task_1_var_70_item.csv', delimiter=';')
data = df.to_dict(orient='records')

drop_table(connection)

create_table(connection)

insert_data(connection, data)

data = topPages(connection)
with open("result_1_top_pages.json", "w",encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

print("Просмотры: " + str(views(connection)))


print("Частота жанров: " + str(genreFreq(connection)))

data = topRating(connection)
with open("result_1_top_predicate_rating.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)
