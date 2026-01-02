Clinical Workflow Simulation System

A Python-based simulation of a clinical task workflow, built with FastAPI, SQLAlchemy, and SQLite. This project demonstrates domain-driven design, state management, and audit logging in a persistent, testable API system.

Table of Contents

Project Overview

Architecture

Setup Instructions

Usage

Testing

Future Improvements

Project Overview

This project simulates a clinical workflow where tasks are created for patients and progress through defined statuses such as ORDERED, IN_PROGRESS, and COMPLETED. Every transition is validated and logged in an audit trail.

Key features:

Domain logic separated from database and API layers

Persistent storage using SQLite + SQLAlchemy

REST API built with FastAPI

Automatic input validation via Pydantic schemas

Interactive API documentation via Swagger UI (/docs)

Audit logging for every task transition

Architecture
1. Domain Layer

models.py — Core Python classes: Patient, ClinicalTask, AuditEvent

state_machine.py — Task statuses, valid transitions, and business rules

Responsibilities: enforce workflow rules, manage audit logs

2. Database Layer

database.py — SQLAlchemy engine and session setup

db_models.py — Tables for PatientDB, TaskDB, AuditEventDB

Responsibilities: persistence, referential integrity, database transactions

3. API Layer

main.py — FastAPI endpoints:

POST /patients → create a patient

POST /tasks → create a task

POST /tasks/{task_id}/transition → transition a task

GET /tasks/{task_id}/audit → view audit log

schemas.py — Pydantic models for input/output validation

Responsibilities: HTTP interface, input validation, translate domain exceptions to API errors

Setup Instructions

Clone the repository

git clone <your-repo-url>
cd clinical-workflow


Create virtual environment and install dependencies

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt


Initialize the database

python init_db.py


Run the FastAPI server

uvicorn app.main:app --reload


Access interactive API docs

http://127.0.0.1:8000/docs

Usage
Create a Patient
POST /patients
{
  "name": "Alice Smith",
  "date_of_birth": "2000-01-01"
}

Create a Task
POST /tasks
{
  "patient_id": "<patient-id>",
  "task_type": "Blood Test"
}

Transition a Task
POST /tasks/{task_id}/transition
{
  "new_status": "IN_PROGRESS",
  "reason": "Lab sample received"
}

View Audit Log
GET /tasks/{task_id}/audit


Returns all transitions for a task with timestamps and reasons

Testing

Domain tests: verify state transitions and business rules

API tests (planned): use pytest + FastAPI TestClient to validate endpoints

Example domain test snippet:

def test_valid_transition():
    task = ClinicalTask(patient_id="123", task_type="Blood Test")
    task.transition(TaskStatus.IN_PROGRESS, "Sample received")
    assert task.status == TaskStatus.IN_PROGRESS
    assert len(task.audit_log) == 1

Future Improvements

Add user roles and permissions

More advanced task queries (e.g., tasks by status, patient history)

Dockerize the project for easier deployment

Add continuous integration tests and coverage reports

Implement API-level tests to verify persistence and endpoints