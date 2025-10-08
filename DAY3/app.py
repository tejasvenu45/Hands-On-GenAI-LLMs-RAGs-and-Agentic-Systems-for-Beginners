from flask import Flask, jsonify, request 
from flask_cors import CORS

app= Flask(__name__)
CORS(app)

db = [{"Movie":"Baasha"},{"Movie":"Guntur Karram"},{"Movie":"KGF"}]
counter = 1

@app.route("/movie",methods=["GET"])
def get_movies():
    return jsonify(db), 200

@app.route("/movie",methods=["POST"])
def add_movie():
    data = request.get_json()
    db.append(data)
    return jsonify({"Success":"Added new movie"}), 200

@app.route("/movie",methods={"PUT"})
def update_movie():
    data = request.get_json()
    for items in db:
        if(data["Movie1"]==items["Movie"]):
            items["Movie"] = data["Movie2"]
            return jsonify({"Success":"Party"}), 200
    return jsonify({"Failure":"Item not found"}), 200



app.run(debug=True)