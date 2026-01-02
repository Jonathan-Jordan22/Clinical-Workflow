from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas import (
    PatientCreate,
    PatientResponse,
    TaskCreate,
    TaskResponse,
    TaskTransitionRequest,
)
from app.database import get_db
from app.services import (
    create_patient_db,
    create_task_db,
    transition_task_db,
)
from app.state_machine import InvalidTransitionError

app = FastAPI(title="Clinical Workflow Simulation System")


@app.get("/")
def root():
    return {
        "message": "Clinical Workflow API",
        "docs": "/docs",
        "endpoints": {
            "create_patient": "POST /patients",
            "create_task": "POST /tasks",
            "transition_task": "POST /tasks/{task_id}/transition"
        }
    }

# ------------------------
# Patient Endpoints
# ------------------------

@app.post("/patients", response_model=PatientResponse)
def create_patient_endpoint(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = create_patient_db(db, payload.name, payload.date_of_birth)
    return patient

# ------------------------
# Task Endpoints
# ------------------------

@app.post("/tasks", response_model=TaskResponse)
def create_task_endpoint(payload: TaskCreate, db: Session = Depends(get_db)):
    try:
        task = create_task_db(db, payload.patient_id, payload.task_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return task

@app.post("/tasks/{task_id}/transition", response_model=TaskResponse)
def transition_task_endpoint(
    task_id: str,
    payload: TaskTransitionRequest,
    db: Session = Depends(get_db)
):
    try:
        task = transition_task_db(db, task_id, payload.new_status, payload.reason)
    except InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return task

# ------------------------
# Audit Endpoint
# ------------------------

@app.get("/tasks/{task_id}/audit")
def get_task_audit(task_id: str, db: Session = Depends(get_db)):
    from app.db_models import TaskDB
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return [
        {
            "previous_status": event.previous_status,
            "new_status": event.new_status,
            "timestamp": event.timestamp,
            "reason": event.reason,
        }
        for event in task.audit_log
    ]