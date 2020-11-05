import mysql.connector
from utils import hashPassword

cinemapp = mysql.connector.connect(user="root", database="cinemapp")
cursor = cinemapp.cursor()

def getUsersList():
    query = "SELECT * FROM user"
    cursor.execute(query)
    users = []
    for row in cursor.fetchall():
        user = {
            "id": row[0],
            "email": row[1],
            "password": row[2]
        }
        users.append(user)
    return users

def userExists(email):
    query = "SELECT COUNT(*) FROM user WHERE email = %s"
    cursor.execute(query, (email, ))
    return cursor.fetchone()[0] == 1

def createUser(email, password):
    if userExists(email):
        return False

    query = "INSERT INTO user(email, password) VALUES(%s, %s)"
    cursor.execute(query, (email, hashPassword(password, "sha256")))
    cinemapp.commit()

    return True

def validLogin(email, password):
    query = "SELECT id FROM user WHERE email = %s AND password = %s"
    cursor.execute(query, (email, hashPassword(password, "sha256")))
    id = cursor.fetchone()
    if id:
        return id[0], True
        
    return None, False
    