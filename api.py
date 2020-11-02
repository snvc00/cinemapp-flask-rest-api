from flask import Flask, jsonify
from cinemapp_db import getUsersList

app = Flask(__name__)

@app.route("/api/v1/users")
def getUsers():
    return jsonify(getUsersList())

app.run()