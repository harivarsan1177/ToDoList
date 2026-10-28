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
        self.assertEqual(
            todo_app.tasks,
            [{"id": 1, "title": "Read chapter one", "completed": False}],
        )

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
                {"id": 1, "title": "First task", "completed": False},
                {"id": 2, "title": "Second task", "completed": False},
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

    def test_new_task_is_pending_and_has_completion_control(self):
        self.client.post("/tasks", data={"task": "Submit report"})

        response = self.client.get("/")

        self.assertFalse(todo_app.tasks[0]["completed"])
        self.assertIn(b"Mark Submit report as completed", response.data)
        self.assertNotIn(b"task-item-completed", response.data)

    def test_task_can_be_marked_completed_and_is_rendered_as_completed(self):
        self.client.post("/tasks", data={"task": "Submit report"})

        response = self.client.post(
            "/tasks/1/toggle",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(todo_app.tasks[0]["completed"])
        self.assertIn(b"task-item-completed", response.data)
        self.assertIn(b'aria-label="Completed"', response.data)
        self.assertIn(b"Mark Submit report as pending", response.data)
        self.assertIn(b"1 task", response.data)

    def test_completed_task_can_be_marked_pending_again(self):
        self.client.post("/tasks", data={"task": "Submit report"})
        self.client.post("/tasks/1/toggle")

        response = self.client.post(
            "/tasks/1/toggle",
            follow_redirects=True,
        )

        self.assertFalse(todo_app.tasks[0]["completed"])
        self.assertNotIn(b"task-item-completed", response.data)
        self.assertIn(b"Mark Submit report as completed", response.data)

    def test_toggle_preserves_task_id_title_and_total_count(self):
        self.client.post("/tasks", data={"task": "First task"})
        self.client.post("/tasks", data={"task": "Second task"})
        self.client.post("/tasks/2/toggle")

        response = self.client.get("/")

        self.assertEqual(
            todo_app.tasks[1],
            {"id": 2, "title": "Second task", "completed": True},
        )
        self.assertIn(b"2 tasks", response.data)
        self.assertIn(b"First task", response.data)
        self.assertIn(b"Second task", response.data)

    def test_toggle_of_unknown_task_returns_not_found(self):
        response = self.client.post("/tasks/999/toggle")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(todo_app.tasks, [])

    def test_toggle_of_non_integer_task_id_returns_not_found(self):
        response = self.client.post("/tasks/not-a-number/toggle")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(todo_app.tasks, [])

    def test_toggle_rejects_get_requests(self):
        self.client.post("/tasks", data={"task": "Keep pending"})

        response = self.client.get("/tasks/1/toggle")

        self.assertEqual(response.status_code, 405)
        self.assertFalse(todo_app.tasks[0]["completed"])


if __name__ == "__main__":
    unittest.main()
