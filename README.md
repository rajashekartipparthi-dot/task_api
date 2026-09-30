# Task API

A small REST API for managing tasks, built with Flask and SQLite.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The server runs at http://127.0.0.1:5000.

## Endpoints

| Method | Path            | Description                          |
|--------|-----------------|--------------------------------------|
| GET    | /health         | Health check                         |
| GET    | /tasks          | List tasks (`?done=true` to filter)  |
| POST   | /tasks          | Create a task: `{"title": "..."}`    |
| GET    | /tasks/<id>     | Get one task                         |
| PATCH  | /tasks/<id>     | Update `title` and/or `done`         |
| DELETE | /tasks/<id>     | Delete a task                        |

## Example

```bash
curl -X POST localhost:5000/tasks -H "Content-Type: application/json" -d '{"title": "Buy milk"}'
curl -X PATCH localhost:5000/tasks/1 -H "Content-Type: application/json" -d '{"done": true}'
```

## Tests

```bash
python -m unittest discover tests
```
