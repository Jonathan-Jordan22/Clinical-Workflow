from fastapi import FastAPI, HTTPException

from app.models import Patient, ClinicalTask
from app.schemas import (
    PatientCreate,
    PatientResponse,
    TaskCreate,
    TaskTransitionRequest,
    TaskResponse,
)
from app.services import transition_task
from app.state_machine import InvalidTransitionError

app = FastAPI(title="Clinical Workflow Simulation System")

patients = {}
tasks = {}


@app.post("/patients", response_model=PatientResponse)
def create_patient(payload: PatientCreate):
    patient = Patient(
        name=payload.name,
        date_of_birth=payload.date_of_birth,
    )
    patients[patient.id] = patient
    return patient


@app.post("/tasks", response_model=TaskResponse)
def create_task(payload: TaskCreate):
    if payload.patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    task = ClinicalTask(
        patient_id=payload.patient_id,
        task_type=payload.task_type,
    )
    tasks[task.id] = task
    return task

@app.post("/tasks/{task_id}/transition", response_model=TaskResponse)
def transition_task_endpoint(task_id: str, payload: TaskTransitionRequest):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        transition_task(
            task=task,
            new_status=payload.new_status,
            reason=payload.reason,
        )
    except InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return task

@app.get("/tasks/{task_id}/audit")
def get_task_audit(task_id: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.audit_log