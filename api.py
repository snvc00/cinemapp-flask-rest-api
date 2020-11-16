from flask import Flask, jsonify, request
from flask import json
from cinemapp_db import getUsersList, createUser, validLogin, \
                        createMovie, getMovies, getMovieById

enableDebug = True
app = Flask(__name__)

@app.route("/api/v1/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return jsonify(getUsersList())
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
@app.route("/api/v1/movies/<int:id>", methods=["GET"])
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
        

@app.route("/api/v1/login", methods=["POST"])
def login():
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