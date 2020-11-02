import mysql.connector

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