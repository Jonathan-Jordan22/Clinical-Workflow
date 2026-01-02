from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4

from app.state_machine import TaskStatus


@dataclass
class Patient:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    date_of_birth: str = ""


@dataclass
class AuditEvent:
    id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    previous_status: TaskStatus | None = None
    new_status: TaskStatus | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reason: str = ""


@dataclass
class ClinicalTask:
    id: str = field(default_factory=lambda: str(uuid4()))
    patient_id: str = ""
    task_type: str = ""
    status: TaskStatus = TaskStatus.ORDERED
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    audit_log: List[AuditEvent] = field(default_factory=list)