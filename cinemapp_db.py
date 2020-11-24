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

def createMovie(movie):
    query = "INSERT INTO movie \
            (title, view_date, image, director, year, userId) \
            VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, 
    (movie["title"], movie["view_date"],  movie["image"], movie["director"], movie["year"], movie["userId"]))
    cinemapp.commit()
    if cursor.rowcount:
        return True;
    
    return False;

def getMovies():
    query = "SELECT id, title, view_date, image, director, year, userId FROM movie";
    cursor.execute(query)
    movies = []
    for row in cursor.fetchall():
        movie = {
            "id": row[0],
            "title": row[1],
            "view_date": row[2],
            "image": row[3],
            "director": row[4],
            "year": row[5],
            "userdId": row[6]
        }
        movies.append(movie)
    
    return movies

def getMovieById(id):
    query = "SELECT * FROM movie WHERE id = %s"
    cursor.execute(query, (id,))
    movie = {}

    row = cursor.fetchone()
    if row:
        movie["id"] = row[0] 
        movie["title"] = row[1] 
        movie["view_date"] = row[2] 
        movie["image"] = row[3] 
        movie["director"] = row[4] 
        movie["year"] = row[5] 
        movie["rate"] = row[6] 
        movie["favorite"] = row[7] 
        movie["review"] = row[8] 
        movie["shared"] = row[9] 
    
    return movie

def modifyMovie(id, column, newValue):
    query = f"UPDATE movie SET {column} = %s WHERE id = %s"
    cursor.execute(query, (newValue, id))
    cinemapp.commit()

    return bool(cursor.rowcount)

def deleteMovie(id):
    query = f"DELETE FROM movie WHERE id = %s"
    cursor.execute(query, (id,))
    cinemapp.commit()

    return bool(cursor.rowcount)

def getUserMovies(id):
    query = "SELECT * FROM movie WHERE userId = %s"
    cursor.execute(query, (id,))
    movies = []
    for row in cursor.fetchall():
        movie = {
            "id": row[0], 
            "title": row[1],
            "view_date": row[2], 
            "image": row[3],
            "director": row[4], 
            "year": row[5],
            "rate": row[6],
            "favorite": row[7],
            "review": row[8], 
            "shared": row[9] 
        }
        movies.append(movie)
    
    return movies