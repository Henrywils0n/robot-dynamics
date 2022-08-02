from flask import Flask, request, jsonify, url_for, redirect
import json
import atexit


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
        if id > 0 and id <= len(data["agents"]):
            return jsonify(data["agents"][id-1])
    if request.method == "PUT":
        if id > 0 and id <= len(data["agents"]):
            data["agents"][id-1] = request.json
            return jsonify(data["agents"][id-1])


# robot position estimate route


@app.route("/agentsLocal/<id>", methods=["GET", "PUT"])
def agentsLocalReq(id):
    id = int(id)
    if request.method == "GET":
        if id > 0 and id <= len(data["agentsLocal"]):
            return jsonify(data["agentsLocal"][id-1])
    if request.method == "PUT":
        if id > 0 and id <= len(data["agentsLocal"]):
            data["agentsLocal"][id-1] = request.json
            return jsonify(data["agentsLocal"][id-1])

# agent ready route with id


@app.route("/agentReady/<id>", methods=["GET", "PUT"])
def agentReadyReq(id):
    id = int(id)
    print(id)
    if request.method == "GET":
        if id > 0 and id <= len(data["agentReady"]):
            return jsonify(data["agentReady"][id-1])
    if request.method == "PUT":
        if id > 0 and id <= len(data["agentReady"]):
            data["agentReady"][id-1] = request.json
            return jsonify(data["agentReady"][id-1])

# agent ready route without id


@app.route("/agentReady", methods=["GET"])
def agentReadyNoIDReq():
    return jsonify(data["agentReady"])

# agentGo route with id 1


@app.route("/agentGo/<id>", methods=["GET", "PUT"])
def agentGoReq(id):
    id = int(id)
    if request.method == "GET":
        if id == 1:
            return jsonify(data["agentGo"][id-1])
    if request.method == "PUT":
        if id == 1:
            data["agentGo"][id-1] = request.json
            return jsonify(data["agentGo"][id-1])

# goal1 route with id


@app.route("/goal1/<id>", methods=["GET", "PUT", "DELETE", "POST", "HEAD"])
def goal1Req(id):
    id = int(id)
    if request.method == "GET":
        if id > 0 and id <= len(data["goal1"]):
            return jsonify(data["goal1"][id-1])
    if request.method == "PUT":
        if id > 0 and id <= len(data["goal1"]):
            data["goal1"][id-1] = request.json
            return jsonify(data["goal1"][id-1])
        else:
            data["goal1"].append(request.json)
            return jsonify(data["goal1"][-1])
    if request.method == "DELETE":
        if id > 0 and id <= len(data["goal1"]):
            data["goal1"].pop(id-1)
            return jsonify(data["goal1"])
        else:
            # 404
            return "", 404
    if request.method == "POST":
        if id > 0:
            data["goal1"].append(request.json)
            return jsonify(data["goal1"][id-1])
    if request.method == "HEAD":
        if id > 0 and id <= len(data["goal1"]):
            return jsonify(data["goal1"][id-1])
        else:
            # return a 404 error
            return "", 404

# route for goal2 with id


@app.route("/goal2/<id>", methods=["GET", "PUT", "DELETE", "POST", "HEAD"])
def goal2Req(id):
    id = int(id)
    if request.method == "GET":
        if id > 0 and id <= len(data["goal2"]):
            return jsonify(data["goal2"][id-1])
    if request.method == "PUT":
        if id > 0 and id <= len(data["goal2"]):
            data["goal2"][id-1] = request.json
            return jsonify(data["goal2"][id-1])
        else:
            data["goal2"].append(request.json)
            return jsonify(data["goal2"][-1])
    if request.method == "DELETE":
        if id > 0 and id <= len(data["goal2"]):
            data["goal2"].pop(id-1)
            return jsonify(data["goal2"])
        else:
            # return a 404 error
            return "", 404
    if request.method == "POST":
        if id > 0:
            data["goal2"].append(request.json)
            return jsonify(data["goal2"][id-1])
    if request.method == "HEAD":
        if id > 0 and id <= len(data["goal2"]):
            return jsonify(data["goal2"][id-1])
        else:
            # return a 404 error
            return "", 404

# route for goal3 with id


@app.route("/goal3/<id>", methods=["GET", "PUT", "DELETE", "POST", "HEAD"])
def goal3Req(id):
    id = int(id)
    if request.method == "GET":
        if id > 0 and id <= len(data["goal3"]):
            return jsonify(data["goal3"][id-1])
    if request.method == "PUT":
        if id > 0 and id <= len(data["goal3"]):
            data["goal3"][id-1] = request.json
            return jsonify(data["goal3"][id-1])
        else:
            data["goal3"].append(request.json)
            return jsonify(data["goal3"][-1])
    if request.method == "DELETE":
        if id > 0 and id <= len(data["goal3"]):
            data["goal3"].pop(id-1)
            return jsonify(data["goal3"])
        else:
            return "", 404
    if request.method == "POST":
        if id > 0:
            data["goal3"].append(request.json)
            return jsonify(data["goal3"][id-1])
    if request.method == "HEAD":
        if id > 0 and id <= len(data["goal3"]):
            return jsonify(data["goal3"][id-1])
        else:
            # return a 404 error
            return "", 404


app.run(host="192.168.0.100", port=3000, debug=False)
