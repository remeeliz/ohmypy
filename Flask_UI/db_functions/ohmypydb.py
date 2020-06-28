##################################################
## FileName: ohmypydb.py
##################################################
## Author: RDinmore
## Date: 2020.06.27
## Purpose: database functions
## Libs: mysql
## Path: db/ohmypydb.py
##################################################

from mysql import connector
import pandas as pd

mydb = connector.connect(user='admin', password="ohmypycis4930",
                                   host="ohmypy.cdd0llcf03hp.us-east-1.rds.amazonaws.com", db="metadata")

def execute_query(query):
    mydb = mysql.connector.connect(user='admin', password="ohmypycis4930", host="ohmypy.cdd0llcf03hp.us-east-1.rds.amazonaws.com")
    mycursor = mydb.cursor()
    results = mycursor.execute(query)
    if results == None:
        return mycursor.fetchall()
    else:
        return 0


def create_database(database_name):
    query = "CREATE DATABASE IF NOT EXISTS "+database_name
    execute_query(query)

def get_face_id(face_vector, name_id):
    sql_select_Query = "SELECT MIN(face_id), count FROM face_data WHERE face_vector = '" + face_vector + "'"
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    face_id = records[0][0]
    if face_id != None:
        new_count = records[0][1] + 1
        sql_select_Query = "UPDATE face_data SET count = " + str(new_count) + " WHERE face_id = " + str(face_id) + ""
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query)
        mydb.commit()
        cursor.close()
        return face_id
    else:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO face_data (face_vector, name_id, count) VALUES ('" + face_vector + "',"+str(name_id)+", 1)")
        mydb.commit()
        cursor.close()
        return get_name_id(face_vector)

def get_face_id(face_vector, name_id):
    sql_select_Query = "SELECT MIN(face_id), count FROM face_data WHERE face_vector = '" + face_vector + "'"
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    face_id = records[0][0]
    if face_id != None:
        new_count = records[0][1] + 1
        sql_select_Query = "UPDATE face_data SET count = " + str(new_count) + " WHERE face_id = " + str(face_id) + ""
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query)
        mydb.commit()
        cursor.close()
        return face_id
    else:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO face_data (face_vector, name_id, count) VALUES ('" + face_vector + "',"+str(name_id)+", 1)")
        mydb.commit()
        cursor.close()
        return get_name_id(face_vector)

def get_name_id(name):
    sql_select_Query = "SELECT MIN(name_id) FROM name_data WHERE full_name = '"+name+"'"
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    name_id = records[0][0]
    if name_id != None:
        return name_id
    else:
        cursor = mydb.cursor()
        if len(name) > 100:
            t = input("hello")
        cursor.execute("INSERT INTO name_data (full_name) VALUES ('" + name + "')")
        mydb.commit()
        cursor.close()
        return get_name_id(name)

def insert_face(face_vector, name):
    name_id = get_name_id(str(name))
    face_id = get_face_id(str(face_vector), name_id)
    return 1

def get_data():
    sql_select_Query = "select n.full_name, f.face_vector, f.count from name_data n join face_data f on f.name_id = n.name_id;"

    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    df = pd.DataFrame(records)

    return df