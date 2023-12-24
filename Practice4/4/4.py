import os
import sqlite3
import json
import pickle

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB3")

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
                           UNIQUE
                           NOT NULL,
    name        TEXT (256) NOT NULL
                           UNIQUE,
    price       REAL       NOT NULL,
    quantity    INTEGER    NOT NULL,
    category    TEXT (256) NOT NULL,
    fromCity    TEXT (256) NOT NULL,
    isAvailable TEXT (256) NOT NULL,
    views       INTEGER    NOT NULL,
    upd_count INTEGER   DEFAULT (0) 
                           NOT NULL
)

''')
    
def insertData(connection, data):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table1 (name, price, quantity, category, fromCity, isAvailable, views) 
        VALUES(:name, :price, :quantity, :category, :fromCity, :isAvailable, :views)
        """, data
    )
    connection.commit()
    cursor.close()

def topUpd(connection, top=10):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        ORDER BY upd_count DESC LIMIT ?
        ''', [top]
    )   
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()  
    return items

def getStatQuantity(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            category,
            CAST(COUNT(*) as REAL) as count,
            SUM(quantity) as sum,
            AVG(quantity) as avg,
            MIN(quantity) as min, 
            MAX(quantity) as max
        FROM table1
        GROUP BY category
        '''
    )
    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))

    cursor.close()
    return stat_freq


def getStatPrice(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            category,
            CAST(COUNT(*) as REAL) as count,
            SUM(price) as sum,
            AVG(price) as avg,
            MIN(price) as min, 
            MAX(price) as max
        FROM table1
        GROUP BY category
        '''
    )
    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))
    cursor.close()
    return stat_freq


def topPredicateViews(connection, category="cosmetics", top=20):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        WHERE category = ?
        ORDER BY price DESC LIMIT ?
        ''', [category, top]
    )  
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()   
    return items

def remove(connection, name):
    cursor = connection.cursor()
    cursor.execute(
        '''
        DELETE FROM table1 
        WHERE name = ?
        ''', [name]
    )
    connection.commit()
    cursor.close()

def updPricePercent(connection, name, percent):
    cursor = connection.cursor()
    cursor.execute(
        '''
        UPDATE table1 
        SET price = ROUND((price * (1 + ?)), 2)
        WHERE name = ?
        ''', [percent, name]
    )
    cursor.execute(
        '''
        UPDATE table1 
        SET upd_count = upd_count + 1
        WHERE name = ?
        ''', [name]
    )
    connection.commit()
    cursor.close()

def updPriceAbs(connection, name, value):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        UPDATE table1 
        SET price = price + ?
        WHERE name = ? AND ((price + ?) > 0)
        ''', [value, name, value]
    )
    if res.rowcount > 0:
        cursor.execute(
            '''
            UPDATE table1 
            SET upd_count = upd_count + 1
            WHERE name = ?
            ''', [name]
        )
        connection.commit()
    cursor.close()


def availableUpd(connection, name, value):
    cursor = connection.cursor()
    cursor.execute(
        '''
        UPDATE table1 
        SET upd_count = upd_count + 1
        WHERE name = ?
        ''', [name]
    )
    connection.commit()
    cursor.close()

def quantityUpd(connection, name, value):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        UPDATE table1 
        SET quantity = quantity + ?
        WHERE name = ? AND ((quantity + ?) > 0)
        ''', [value, name, value]
    )
    if res.rowcount > 0:
        cursor.execute(
            '''
            UPDATE table1 
            SET upd_count = upd_count + 1
            WHERE name = ?
            ''', [name]
        )
        connection.commit()
    cursor.close()
    
def dbUpd(connection, item):
    if item["method"] == "remove":
        remove(connection, item["name"])
    elif item["method"] == "price_percent":
        updPricePercent(connection, item["name"], item["param"])
    elif item["method"] == "price_abs":
        updPriceAbs(connection, item["name"], item["param"])
    elif item["method"] == "available":
        availableUpd(connection, item["name"], item["param"])
    elif "quantity" in item["method"]:
        quantityUpd(connection, item["name"], item["param"])
    else:
        print("Wrong method")
    
connection = connect(dbPath)

with open("task_4_var_70_product_data.text", "r", encoding='utf_8') as file:
        data1 = []
        dct = {}
        unique_name = []
        is_same = False
        for st in file.readlines():
            if st == "=====\n":
                if is_same:
                    is_same = False
                else:
                    if 'category' not in dct:
                        dct['category'] = 'no'
                    data1.append(dct)     
                    unique_name.append(dct["name"])          
                dct = {}
                continue

            key, value = st.split("::")
            key, value = key.strip(), value.strip()
            if key == "name" and value in unique_name:
                is_same = True
            if key in ["quantity", "views"]:
                dct[key] = int(value)
            elif key == "price":
                dct[key] = float(value)
            else:    
                dct[key.strip()] = value.strip()

data2 = []
with open(file="task_4_var_70_update_data.pkl", mode="rb") as file:
    data2 = pickle.load(file)
    print(data2)

 
    
drop_table(connection)

create_table(connection)

insertData(connection, data1)

for elem in data2:
    dbUpd(connection, elem)

data = topUpd(connection)
with open("result_4_top_upd.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)
    

print("Статистика по стоимости: " + str(getStatPrice(connection)))

print("Статистика по количеству: " + str(getStatQuantity(connection)))

data = topPredicateViews(connection)
with open("t4_res_top_predicate_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)
