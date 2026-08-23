# Notice Board API

## 1. Project Overview

Notice Board API is a RESTful web application developed using Python and FastAPI.

The system allows users to create, view, update, search, archive, restore and export notices. SQLite is used as the database, while JSON, CSV and TXT formats are supported for exporting notice data.

The project also demonstrates advanced Python programming concepts such as decorators, iterators, generators, context managers, comprehensions, asynchronous programming, environment variables and automated testing.

---

## 2. Objectives

The main objectives of the project are:

- To develop a RESTful API using FastAPI.
- To implement CRUD operations for notices.
- To store notice information using SQLite.
- To implement notice searching and filtering.
- To provide archive and restore functionality.
- To export notice data into JSON, CSV and TXT formats.
- To demonstrate advanced Python programming concepts.
- To implement input validation using Pydantic.
- To implement automated testing using Pytest.
- To provide interactive API documentation using Swagger UI.

---

## 3. Features

### Notice Management

- Create a notice
- View all notices
- View a notice by ID
- Update a notice
- Delete/archive a notice
- Restore an archived notice
- Search notices

### Data Export

Notices can be exported into:

- JSON
- CSV
- TXT

### Validation

Pydantic models are used to validate incoming request data.

Validation includes:

- Required fields
- Minimum field length
- Maximum field length
- Optional expiry date

### Database

SQLite is used for persistent storage.

The notice table contains:

- ID
- Title
- Description
- Category
- Created date/time
- Expiry date
- Status
- Deleted date/time

---

## 4. Technologies Used

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- Python-dotenv
- Pytest
- HTTPX
- JSON
- CSV

---

## 5. Advanced Python Concepts Used

### 5.1 Context Manager

The `contextmanager` decorator from Python's `contextlib` module is used for database connection management.

It ensures that:

- Database connections are opened safely.
- Transactions are committed when successful.
- Transactions are rolled back when an exception occurs.
- Connections are closed after use.

---

### 5.2 Decorator

A custom decorator named `log_execution_time` is implemented.

It measures the execution time of asynchronous functions and prints the execution time to the console.

This demonstrates the use of:

- Functions as objects
- Decorators
- `functools.wraps`
- `time.perf_counter()`
- Async functions

---

### 5.3 Custom Iterator

A `NoticeIterator` class is implemented to traverse notices one at a time.

It implements:

- `__iter__()`
- `__next__()`

When there are no more notices, `StopIteration` is raised.

---

### 5.4 Generator

A `notice_generator()` function uses the `yield` keyword to return notices one at a time.

Generators provide lazy evaluation and avoid loading all processing results at once.

---

### 5.5 File Handling

The project uses Python file handling to export notice information.

Supported formats:

- JSON
- CSV
- TXT

The `with open()` statement is used to safely manage files.

---

### 5.6 Environment Variables

The project uses a `.env` file and `python-dotenv` to load configuration values.

Examples include:

- Application name
- Application version
- Debug mode
- Database path

---

### 5.7 Pydantic Validation

Pydantic models are used to validate API input.

The project contains schemas for:

- Creating notices
- Updating notices

---

### 5.8 Asynchronous Programming

FastAPI asynchronous endpoints are used where appropriate.

The project also demonstrates asynchronous function handling through the execution-time decorator.

---

### 5.9 Comprehensions and Functional Programming

Python comprehensions and functional programming techniques are used where appropriate for processing and filtering notice data.

---

## 6. Project Structure

```text
NoticeBoardAPI/
│
├── app/
│   ├── main.py
│   ├── dependencies.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── data/
│   └── notice_board.db
│
├── exports/
│   ├── notices.json
│   ├── notices.csv
│   └── notices.txt
│
├── tests/
│   └── test_notices.py
│
├── .env
├── requirements.txt
└── README.md