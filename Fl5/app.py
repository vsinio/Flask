from flask import Flask, request, jsonify, abort
from pydantic import ValidationError
from models import TaskBase, TaskCreate, TaskUpdate, TaskInResponse
import json
import os

app = Flask(__name__)

# Инициализация "базы данных"
tasks = []
task_id_counter = 1


def read_tasks_from_file():
    global tasks, task_id_counter
    if not os.path.isfile('data.json'):
        tasks = []
        task_id_counter = 1
        print("No data.json file found. Initializing empty task list.")
        return

    try:
        with open('data.json', 'r') as file:
            data = file.read().strip()
            if not data:
                tasks = []
                task_id_counter = 1
                print("data.json is empty. Initializing empty task list.")
            else:
                data = json.loads(data)
                tasks = [TaskInResponse(**task) for task in data]
                if tasks:
                    task_id_counter = max(task.id for task in tasks) + 1
                else:
                    task_id_counter = 1
                print("Tasks loaded successfully.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file. Initializing empty task list.")
        tasks = []
        task_id_counter = 1


def write_tasks_to_file():
    with open('data.json', 'w') as file:
        json.dump([task.dict() for task in tasks], file, indent=4)
    print("Tasks saved to file.")


read_tasks_from_file()


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.dict() for task in tasks]), 200


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((t for t in tasks if t.id == id), None)
    if task is None:
        abort(404, description="Task not found")
    return jsonify(task.dict()), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    try:
        task_data = TaskCreate(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    task = TaskInResponse(id=task_id_counter, **task_data.dict())
    tasks.append(task)
    task_id_counter += 1
    write_tasks_to_file()
    return jsonify(task.dict()), 201


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        task_data = TaskUpdate(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    task = next((t for t in tasks if t.id == id), None)
    if task is None:
        abort(404, description="Task not found")

    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    write_tasks_to_file()
    return jsonify(task.dict()), 200


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    task = next((t for t in tasks if t.id == id), None)
    if task is None:
        abort(404, description="Task not found")

    tasks = [t for t in tasks if t.id != id]
    write_tasks_to_file()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
