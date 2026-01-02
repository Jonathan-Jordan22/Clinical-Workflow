from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.state_machine import TaskStatus


class PatientCreate(BaseModel):
    name: str
    date_of_birth: str


class PatientResponse(BaseModel):
    id: str
    name: str
    date_of_birth: str


class TaskCreate(BaseModel):
    patient_id: str
    task_type: str


class TaskTransitionRequest(BaseModel):
    new_status: TaskStatus
    reason: str


class AuditEventResponse(BaseModel):
    previous_status: TaskStatus | None
    new_status: TaskStatus | None
    timestamp: datetime
    reason: str


class TaskResponse(BaseModel):
    id: str
    patient_id: str
    task_type: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    audit_log: List[AuditEventResponse]