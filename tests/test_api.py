import os
import tempfile
import unittest

from app import create_app


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        self.fd, self.path = tempfile.mkstemp(suffix=".db")
        self.client = create_app({"DATABASE": self.path, "TESTING": True}).test_client()

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.path)

    def test_health(self):
        self.assertEqual(self.client.get("/health").json, {"status": "ok"})

    def test_create_and_get(self):
        res = self.client.post("/tasks", json={"title": "Write code"})
        self.assertEqual(res.status_code, 201)
        task_id = res.json["id"]
        got = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(got.json["title"], "Write code")
        self.assertFalse(got.json["done"])

    def test_create_requires_title(self):
        self.assertEqual(self.client.post("/tasks", json={}).status_code, 400)

    def test_update_and_filter(self):
        tid = self.client.post("/tasks", json={"title": "A"}).json["id"]
        self.client.post("/tasks", json={"title": "B"})
        res = self.client.patch(f"/tasks/{tid}", json={"done": True})
        self.assertTrue(res.json["done"])
        done = self.client.get("/tasks?done=true").json
        self.assertEqual([t["title"] for t in done], ["A"])

    def test_delete(self):
        tid = self.client.post("/tasks", json={"title": "A"}).json["id"]
        self.assertEqual(self.client.delete(f"/tasks/{tid}").status_code, 204)
        self.assertEqual(self.client.get(f"/tasks/{tid}").status_code, 404)


if __name__ == "__main__":
    unittest.main()
