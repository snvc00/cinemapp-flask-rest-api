from flask import Flask, jsonify, request
from cinemapp_db import getUsersList, createUser, validLogin, \
                        createMovie, getMovies, getMovieById, \
                        modifyMovie, deleteMovie, getUserMovies

enableDebug = True
app = Flask(__name__)

@app.route("/api/v1/users", methods=["GET", "POST"])
@app.route("/api/v1/users/<int:id>/movies", methods=["GET"])
def users(id=None):
    if request.method == "GET":
        if id is None:
            return jsonify(getUsersList())
        else:
            return jsonify(getUserMovies(id))
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            if createUser(data["email"], data["password"]):
                response = jsonify({"code": "ok"})
            else:
                response = jsonify({"code": "exists"})

        except:
            response = jsonify({"code": "error"})
    
        return response

@app.route("/api/v1/movies", methods=["GET", "POST"])
@app.route("/api/v1/movies/<int:id>", methods=["GET", "PATCH", "DELETE"])
def movies(id = None):
    if request.method == "GET":
        if id is None:
            return jsonify({"movies": getMovies()})
        else:
            return jsonify({"movie": getMovieById(id)})
    if request.method == "POST" and request.is_json:
        try:
            if createMovie(request.get_json()):
                return jsonify({"code": "ok"})
            
            return jsonify({"code": "invalid"})
        except:
            return jsonify({"code": "error"})
    if request.method == "PATCH" and id is not None and request.is_json:
        data = request.get_json()
        if modifyMovie(id, data["column"], data["value"]):
            return jsonify(code="ok")

        return jsonify(code="error")
    if request.method == "DELETE" and id is not None:
        if deleteMovie(id):
            return jsonify(code="ok")

        return jsonify(code="error")
        
@app.route("/api/v1/login", methods=["POST"])
def login():
    response = jsonify({"code": "undefined"})
    try:
        if request.method == "POST" and request.is_json:
            data = request.get_json()
            id, success = validLogin(data["email"], data["password"])

            if success:
                response = jsonify({"code": "ok", "id": id})  
            else:
                response = jsonify({"code": "notexist"})
                
    except:
        response = jsonify({"code": "error"})
    
    return response

app.run(debug=enableDebug)