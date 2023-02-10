from flask import Flask, jsonify, request, send_from_directory, abort
import os
from waitress import serve
from flask_cors import CORS
from tasks import createSomeAsyncTask
from store import createTasksTable, insertTask, getTaskById, doesIdExists

from celery.result import AsyncResult

app = Flask(__name__)
CORS(app)

createTasksTable()

@app.route('/')
def index():
    return jsonify({"status":"alive" }), 202

@app.route("/create-task/<id>", methods=["GET"])
def createSomeTaskFunc(id):
    task = doesIdExists(id)
    _id = task.get("id", "")
    if _id:
        return jsonify({"task_id": task.get("taskId", ""), "exists": 1}), 202
    task = createSomeAsyncTask.delay(int(id))
    taskDetails = {
        "id": id,
        "taskId": task.id
    }
    insertTask(taskDetails);
    return jsonify({"task_id": task.id}), 202

@app.route("/fetch-task-progress/<taskId>", methods=["GET"])
def fetchTaskProgress(taskId):
    task_result = AsyncResult(taskId)
    task = getTaskById(taskId)
    id = task.get("id", "")
    result = {}
    if task_result.state == 'PROGRESS':
        result = {
            "id": id,
            "task_status": task_result.status,
            "progress": task_result.result['x'],
        }
    elif task_result.state == 'SUCCESS':
        result = {
            "id": id,
            "task_status": task_result.status,
            "progress": task_result.result['x'],
        }
    return jsonify(result), 200

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=os.getenv("PORT", default=5000))