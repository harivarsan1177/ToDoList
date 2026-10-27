from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

tasks = []
next_task_id = 1
MAX_TASK_LENGTH = 200


@app.get("/")
def index():
    return render_template(
        "index.html",
        tasks=tasks,
        task_count=len(tasks),
        error_message=None,
        submitted_title="",
        task_added=request.args.get("added") == "1",
        max_task_length=MAX_TASK_LENGTH,
    )


@app.post("/tasks")
def add_task():
    global next_task_id

    submitted_title = request.form.get("task", "")
    title = submitted_title.strip()

    if not title:
        error_message = "Please enter a task before adding it."
    elif len(title) > MAX_TASK_LENGTH:
        error_message = (
            f"Task titles must be {MAX_TASK_LENGTH} characters or fewer."
        )
    else:
        tasks.append({"id": next_task_id, "title": title})
        next_task_id += 1
        return redirect(url_for("index", added="1"))

    return (
        render_template(
            "index.html",
            tasks=tasks,
            task_count=len(tasks),
            error_message=error_message,
            submitted_title=submitted_title,
            task_added=False,
            max_task_length=MAX_TASK_LENGTH,
        ),
        400,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
