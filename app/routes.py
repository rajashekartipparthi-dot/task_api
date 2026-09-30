from flask import Blueprint, jsonify, request

from .db import get_db

bp = Blueprint("tasks", __name__)


def row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
    }


def error(message, status):
    return jsonify({"error": message}), status


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/tasks")
def list_tasks():
    query = "SELECT * FROM tasks"
    params = []
    done = request.args.get("done")
    if done is not None:
        query += " WHERE done = ?"
        params.append(1 if done.lower() in ("1", "true") else 0)
    rows = get_db().execute(query + " ORDER BY id", params).fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@bp.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return error("'title' is required", 400)

    db = get_db()
    cur = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    row = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return error("task not found", 404)
    return jsonify(row_to_dict(row))


@bp.patch("/tasks/<int:task_id>")
def update_task(task_id):
    db = get_db()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return error("task not found", 404)

    data = request.get_json(silent=True) or {}
    title = str(data.get("title", row["title"])).strip()
    if not title:
        return error("'title' cannot be empty", 400)
    done = int(bool(data.get("done", row["done"])))

    db.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, task_id))
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return jsonify(row_to_dict(row))


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    if cur.rowcount == 0:
        return error("task not found", 404)
    return "", 204
