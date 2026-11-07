from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory task storage
tasks = []
next_id = 1


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks."""
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    global next_id

    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({
            "error": "A task title is required."
        }), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    """Mark a task as complete."""

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return jsonify(task), 200

    return jsonify({
        "error": "Task not found."
    }), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return "", 204

    return jsonify({
        "error": "Task not found."
    }), 404


if __name__ == "__main__":
    app.run(debug=True)