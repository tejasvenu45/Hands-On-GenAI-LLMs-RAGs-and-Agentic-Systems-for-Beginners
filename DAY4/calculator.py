# import from libraries
from flask import Flask, jsonify, request
from flask_cors import CORS

# creating data structure for history, id of history elements
history = []
index = 1

# core logic (calculator, get_history, undo functions)
def calculator(operation, a, b):
    operation = operation.lower()
    global index, history
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = "Error: Division by zero" if b == 0 else a / b
    else:
        result = "Invalid operation"

    record = {
        "id": index,
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    }

    index += 1
    history.append(record)
    return result

def get_history():
    if not history:
        return []
    return history

def undo():
    if history:
        removed = history.pop()
        return removed
    else:
        return None

# flask app initialized
app = Flask(__name__)
CORS(app)

# GET- to show history, if history exists
@app.route("/history", methods=["GET"])
def api_get_history():
    return jsonify(get_history()), 200 # Request was successful.

# POST- to perform an operation and update the success/ failure of operation
@app.route("/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json()
    operation = data.get("operation")
    a = data.get("a")
    b = data.get("b")

    # checking if values are correct
    if operation is None or a is None or b is None:
        return jsonify({"error": "Missing required fields: operation, a, b"}), 400

    result = calculator(operation, a, b)
    return jsonify({"result": result, "history": history[-1]}), 201 # A new resource was created successfully.

# DELETE- for undo last operation
@app.route("/history", methods=["DELETE"])
def api_undo_last():
    removed = undo()
    if removed:
        return jsonify({"message": "Last calculation undone", "removed": removed}), 200
    else:
        return jsonify({"message": "Nothing to undo"}), 200

if __name__ == "__main__":
    app.run(debug=True)