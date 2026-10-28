# TaskFlow — To-Do App

**Roll number:** 24MIS0269  
**Course:** Agile and DevOps  
**Version:** V2 — Create Task and Mark as Complete

## Overview

TaskFlow is a small web application for keeping a simple list of tasks. V2 lets a user create tasks, mark tasks as complete, and return completed tasks to pending. It is intentionally built with a small Flask backend and a server-rendered HTML page.

## Implemented V1 and V2 scope

- Add a task with a title from 1 to 200 characters after trimming whitespace.
- Show the task list and the total task count.
- Show helpful validation feedback and an empty-state message.
- Render task text safely using Flask/Jinja's automatic HTML escaping.
- Mark a task as complete or return it to pending using a POST request.
- Visually distinguish completed tasks with a checkmark and strikethrough.

Task deletion, editing, authentication, and persistent storage are not implemented.

## Technology stack

- Python 3.9 or newer
- Flask
- HTML5 and CSS3
- Python's built-in `unittest` framework

## Project structure

```text
todo-devops-project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── tests/
│   └── test_app.py
├── Dockerfile
├── Jenkinsfile
└── k8s/
    ├── v1-deployment.yaml
    └── v1-service.yaml
```

## Prerequisites

- Python 3.9 or newer installed and available as `python` in PowerShell.
- PowerShell (included with Windows).

## Set up on Windows PowerShell

Run these commands from the project root:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents activation due to its execution policy, you can invoke the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the application

With the virtual environment activated:

```powershell
python app.py
```

Open [http://localhost:5000](http://localhost:5000/) in a browser. The development server listens on `0.0.0.0:5000` with debug mode disabled.

## Run automated tests

With the virtual environment activated, run the full test suite from the project root:

```powershell
python -m unittest discover -s tests -v
```

Tests use Flask's test client and reset the in-memory task list and ID counter before and after each test. The suite covers task creation, completion and returning to pending, validation, invalid task IDs and HTTP methods, and safe rendering.

## Known limitation

Tasks are stored only in application memory. They are lost when the application restarts, and this V1 storage is not shared between separate application processes.

## Planned future work

- **V3 — Delete Task:** planned; not implemented.

For V2, no changes have been made to the V1 Dockerfile, Jenkinsfile, or Kubernetes Deployment and Service. V2 Docker image publishing and separate Kubernetes deployment remain future DevOps steps.
