# app for a todo manager, solution to todo.txt assignment
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Example structure of the todos list:
# todos = [
#     {"id": 1, "title": "Buy groceries", "completed": False},
#     {"id": 2, "title": "Learn Flask", "completed": True},
#     {"id": 3, "title": "Exercise", "completed": False}
# ]

todos = [{"id": 1, "title": "Buy groceries", "completed": False}]
next_id = 1

# 1. GET     /todos           -> Return all todos
@app.route("/todos", methods=["GET"])
def display_all_todos():
    if todos:
        return jsonify(todos), 200
    return jsonify({"Message": "Add a todo to display!"}), 200

# 2. GET     /todos/<identifier>      -> Return a specific todo
@app.route("/todos/<int:identifier>", methods=["GET"])
def display_specific_todo(identifier):
    if todos:
        for todo in todos:
            if todo["id"] == identifier:
                return jsonify(todo), 200
        return jsonify({"Message": f"Specific todo with ID {identifier} not found."}), 404
    return jsonify({"Message": "Add a todo to display!"}), 200

# 3. POST    /todos           -> Add a new todo
@app.route("/todos", methods=["POST"])
def add_new_todo():
    data = request.get_json()
    if "title" in data and "completed" in data:
        global next_id
        new_todo = {
            "id": next_id,
            "title": data["title"],
            "completed": data["completed"]
        }
        next_id += 1
        todos.append(new_todo)
        return jsonify({"Message": f"Added new todo: {new_todo}"}), 201
    else:
        return jsonify({"Message": "Format of request body is incorrect."}), 400

# 4. PUT     /todos/<identifier>      -> Update a todo (title or completed)
@app.route("/todos/<int:identifier>", methods=["PUT"])
def update_todo(identifier):
    data = request.get_json()
    if "title" in data and "completed" in data:    
        if todos:
            for todo in todos:
                if identifier == todo["id"]:
                    todo["title"] = data["title"]
                    todo["completed"] = data["completed"]
                    return jsonify({"Message": f"Updated todo {identifier}."}), 200
            return jsonify({"Message": f"Specific todo with ID {identifier} not found."}), 404
        else:
            return jsonify({"Message": "Add a todo to update!"}), 200
    else:
        return jsonify({"Message": "Format of request body is incorrect."}), 400

# 5. DELETE  /todos/<id>      -> Delete a specific todo
@app.route("/todos/<int:identifier>", methods=["DELETE"])
def delete_todo(identifier):
    data = request.get_json()
    if todos:
        for todo in todos:
            if identifier == todo["id"]:
                todos.remove(todo)
                return jsonify({"Message": f"Deleted todo {identifier}."}), 200
        return jsonify({"Message": f"Specific todo with ID {identifier} not found."}), 404
    else:
        return jsonify({"Message": "Todo list empty!"}), 200

if __name__ == "__main__":
    app.run(debug=True)