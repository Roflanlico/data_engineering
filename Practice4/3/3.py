import os
import sqlite3
import json
import csv
import msgpack
import pandas as pd

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB2")

def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def drop_table(connection):
    connection.execute('''DROP TABLE IF EXISTS table1; ''')
    
def create_table(connection):
    connection.execute('''
CREATE TABLE table1 (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT
                           NOT NULL
                           UNIQUE,
    artist      TEXT (256) NOT NULL,
    song        TEXT (256) NOT NULL,
    duration_ms INTEGER    NOT NULL,
    year        INTEGER    NOT NULL,
    tempo       REAL       NOT NULL,
    genre       TEXT (256) NOT NULL
    
);
''')
    
def insert_data(connection, data):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table1 (artist, song, duration_ms, year, tempo, genre) 
        VALUES(:artist, :song, :duration_ms, :year, :tempo, :genre)
        """, data
    )
    connection.commit()
    cursor.close()

def top_views(connection, top=80):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        ORDER BY year DESC LIMIT ?
        ''', [top]
    )
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    
    return items

def statDuration(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            SUM(table1.duration_ms) as sum,
            AVG(table1.duration_ms) as avg,
            MIN(table1.duration_ms) as min, 
            MAX(table1.duration_ms) as max
        FROM table1
        '''
    )
    res = dict(res.fetchone())
    cursor.close()
    return res

def compute_freq_genre(connection):
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

def top_predicate_views(connection, max_tempo=105, top=85):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        WHERE tempo >= ?
        ORDER BY year DESC LIMIT ?
        ''', [max_tempo, top]
    )
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    
    return items

connection = connect(dbPath)

df = pd.read_csv('task_3_var_70_part_1.csv', delimiter=';')
data1 = df.to_dict(orient='records')

for elem in data1:
    elem.pop('energy')
    elem.pop('key')
    elem.pop('loudness')

with open("task_3_var_70_part_2.msgpack", 'rb') as file:
    data2 = msgpack.unpack(file)
    

for elem in data2:
    elem.pop("mode")
    elem.pop("speechiness")
    elem.pop("acousticness")
    elem.pop("instrumentalness")

    
drop_table(connection)

create_table(connection)

insert_data(connection, data1)
insert_data(connection, data2)

data = top_views(connection)
with open("t3_res_top_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

print("Статистика по громкости: " + str(statDuration(connection)))

print("Статистика по жанрам: " + str(compute_freq_genre(connection)))

data = top_predicate_views(connection)
with open("t3_res_top_predicate_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)
