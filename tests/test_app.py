import unittest

import app as todo_app


class TaskFlowTests(unittest.TestCase):
    def setUp(self):
        todo_app.tasks.clear()
        todo_app.next_task_id = 1
        todo_app.app.config["TESTING"] = True
        self.client = todo_app.app.test_client()

    def tearDown(self):
        todo_app.tasks.clear()
        todo_app.next_task_id = 1

    def test_home_page_returns_success(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_empty_state_is_displayed_without_tasks(self):
        response = self.client.get("/")

        self.assertIn(b"Your list is clear", response.data)
        self.assertIn(b"0 tasks", response.data)

    def test_valid_task_can_be_created(self):
        response = self.client.post("/tasks", data={"task": "Read chapter one"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(todo_app.tasks, [{"id": 1, "title": "Read chapter one"}])

    def test_created_task_appears_on_the_page(self):
        self.client.post("/tasks", data={"task": "Prepare slides"})

        response = self.client.get("/")

        self.assertIn(b"Prepare slides", response.data)
        self.assertIn(b"1 task", response.data)

    def test_multiple_tasks_are_preserved(self):
        self.client.post("/tasks", data={"task": "First task"})
        self.client.post("/tasks", data={"task": "Second task"})

        response = self.client.get("/")

        self.assertEqual(
            todo_app.tasks,
            [
                {"id": 1, "title": "First task"},
                {"id": 2, "title": "Second task"},
            ],
        )
        self.assertIn(b"2 tasks", response.data)

    def test_empty_task_is_rejected(self):
        response = self.client.post("/tasks", data={"task": ""})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a task", response.data)
        self.assertEqual(todo_app.tasks, [])

    def test_whitespace_only_task_is_rejected(self):
        response = self.client.post("/tasks", data={"task": " \t\n "})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a task", response.data)
        self.assertEqual(todo_app.tasks, [])

    def test_leading_and_trailing_whitespace_is_removed(self):
        self.client.post("/tasks", data={"task": "  Review notes  "})

        self.assertEqual(todo_app.tasks[0]["title"], "Review notes")

    def test_task_longer_than_200_characters_is_rejected(self):
        response = self.client.post("/tasks", data={"task": "x" * 201})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"200 characters or fewer", response.data)
        self.assertEqual(todo_app.tasks, [])

    def test_html_like_task_text_is_escaped(self):
        submitted_title = "<script>alert('hello')</script>"
        response = self.client.post(
            "/tasks",
            data={"task": submitted_title},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"&lt;script&gt;alert(&#39;hello&#39;)&lt;/script&gt;", response.data)
        self.assertNotIn(submitted_title.encode(), response.data)

    def test_task_ids_increment_from_one(self):
        self.client.post("/tasks", data={"task": "First"})
        self.client.post("/tasks", data={"task": "Second"})

        self.assertEqual([task["id"] for task in todo_app.tasks], [1, 2])


if __name__ == "__main__":
    unittest.main()
