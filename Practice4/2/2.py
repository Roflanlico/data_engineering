import os
import sqlite3
import json
import pickle

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB1")

def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def drop_table(connection):
    connection.execute('''DROP TABLE IF EXISTS table2; ''')
    
def create_table(connection):
    connection.execute('''
CREATE TABLE table2 (
    id            INTEGER    UNIQUE
                             PRIMARY KEY AUTOINCREMENT
                             NOT NULL,
    id_table1     INTEGER    REFERENCES table1 (id) 
                             NOT NULL,
    price      INTEGER    NOT NULL,
    place   TEXT(256)    NOT NULL,
    date      TEXT(256)    NOT NULL
);

''')
    
def insert_data(connection, data):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table2 (id_table1, price, place, date) 
        VALUES(
            (SELECT id FROM table1 WHERE title = :title),
            :price, :place, :date)
        """, data
    )
    connection.commit()
    cursor.close()

def q1(connection, genre="детская литература"):
    cursor = connection.cursor()
    res = cursor.execute(
    '''
        SELECT table2.* 
        FROM table2, table1
        WHERE table2.id_table1 = table1.id AND table1.genre = ?              
    ''', [genre])
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    return items   

def stat_price(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            SUM(table2.price) as sum,
            AVG(table2.price) as avg,
            MIN(table2.price) as min, 
            MAX(table2.price) as max
        FROM table2, table1
        WHERE table2.id_table1 = table1.id
        '''
    )
    res = dict(res.fetchone())
    cursor.close()
    return res

def q3(connection, min_pages=200, max_pages=300):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT table2.*
        FROM table2, table1
        WHERE table2.id_table1 = table1.id AND table1.pages > ? AND table1.pages < ? 
        ''', [min_pages, max_pages]
    )

    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))

    cursor.close()
    return stat_freq

connection = connect(dbPath)

        
with open("task_2_var_70_subitem.pkl", 'rb') as file:
    data = pickle.load(file)

drop_table(connection)

create_table(connection)

insert_data(connection, data)

data = q1(connection)
with open("result_2_q1.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

print("Cтатистика по ценам: " + str(stat_price(connection)))

data = q3(connection)
with open("result_2_q3.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)
