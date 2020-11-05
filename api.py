from flask import Flask, jsonify, request
from cinemapp_db import getUsersList, createUser, validLogin

enableDebug = False
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