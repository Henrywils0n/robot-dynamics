from flask import Flask, request, jsonify, url_for, redirect
import json
import atexit
from waitress import serve
import numpy as np
import logging

app = Flask(__name__)
app.config["DEBUG"] = False

# open import and close db.json
readFile = open("db.json", 'r')
data = json.load(readFile)
readFile.close()


# adding exit routine to save the db.json file with the current states (not really necessary but is nice for debugging)
def exit_routine():
    print("Terminating server")
    writeFile = open("db.json", "w")
    writeFile.write(json.dumps(data, indent=4, sort_keys=True))
    writeFile.close()


atexit.register(exit_routine)


# default route
@app.route("/", methods=["GET"])
def home():
    return "Hello, World!"


# agent position route
@app.route("/agents/<id>", methods=["GET", "PUT"])
def agentsReq(id):
    id = int(id)
    if request.method == "GET":
        if 0 < id <= len(data["agents"]):
            return jsonify(data["agents"][id - 1])
    if request.method == "PUT":
        if 0 < id <= len(data["agents"]):
            data["agents"][id - 1] = request.json
            return jsonify(data["agents"][id - 1])


# robot position estimate route
@app.route("/agentsLocal/<id>", methods=["GET", "PUT"])
def agentsLocalReq(id):
    id = int(id)
    if request.method == "GET":
        if 0 < id <= len(data["agentsLocal"]):
            return jsonify(data["agentsLocal"][id - 1])
    if request.method == "PUT":
        if 0 < id <= len(data["agentsLocal"]):
            data["agentsLocal"][id - 1] = request.json
            return jsonify(data["agentsLocal"][id - 1])


# agent ready route with id
@app.route("/agentReady/<id>", methods=["GET", "PUT"])
def agentReadyReq(id):
    id = int(id)
    if request.method == "GET":
        if 0 < id <= len(data["agentReady"]):
            return jsonify(data["agentReady"][id - 1])
    if request.method == "PUT":
        if 0 < id <= len(data["agentReady"]):
            data["agentReady"][id - 1] = request.json
            return jsonify(data["agentReady"][id - 1])


# agent ready route without id
@app.route("/agentReady", methods=["GET"])
def agentReadyNoIDReq():
    return jsonify(data["agentReady"])


# agentGo route with id 1
@app.route("/agentGo/<id>", methods=["GET", "PUT"])
def agentGoReq(id):
    id = int(id)
    if request.method == "GET":
        if 0 < id < 4:
            return jsonify(data["agentGo"][id - 1])
    if request.method == "PUT":
        if 0 < id < 4:
            data["agentGo"][id - 1] = request.json
            return jsonify(data["agentGo"][id - 1])


# goal1 route with id
@app.route("/<goal>/<id>", methods=["GET", "PUT", "DELETE", "POST", "HEAD"])
def goalReq(goal, id):
    id = int(id)
    if request.method == "GET":
        if 0 < id <= len(data[goal]):
            return jsonify(data[goal][id - 1])
    if request.method == "PUT":
        if 0 < id <= len(data[goal]):
            data[goal][id - 1] = request.json
            return jsonify(data[goal][id - 1])
        else:
            data[goal].append(request.json)
            return jsonify(data[goal][-1])
    if request.method == "DELETE":
        if 0 < id <= len(data[goal]):
            data[goal].pop(id - 1)
            return jsonify(data[goal])
        else:
            # 404
            return "", 404
    if request.method == "POST":
        if id > 0:
            data[goal].append(request.json)
            return jsonify(data[goal][id - 1])
    if request.method == "HEAD":
        if 0 < id <= len(data[goal]):
            return jsonify(data[goal][id - 1])
        else:
            # return a 404 error
            return "", 404


# route for accepting 3 by 3 position array and splitting it to the 3 agents
@app.route("/allPos/1", methods=["PUT"])
def allPos():
    data["allPos"] = request.json
    pos = np.array(request.json["pos"])
    for i in range(3):
        data["agents"][i]["position"] = pos[i, :].tolist()
    return jsonify(data["allPos"])


# use this for debugging (if you need to print the requests) (not as fast as using waitress)
# app.run(host="192.168.0.100", port=3000, debug=False, threaded=False, processes=3)
serve(app, host="192.168.0.100", port=3000, threads=4)
