from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.state_machine import validate_transition, TaskStatus, InvalidTransitionError
from app.db_models import PatientDB, TaskDB, AuditEventDB


# ------------------------
# Patient Services
# ------------------------

def create_patient_db(db: Session, name: str, date_of_birth: str) -> PatientDB:
    patient = PatientDB(
        id=str(uuid.uuid4()),
        name=name,
        date_of_birth=date_of_birth,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


# ------------------------
# Task Services
# ------------------------

def create_task_db(db: Session, patient_id: str, task_type: str) -> TaskDB:
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise ValueError("Patient not found")

    task = TaskDB(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        task_type=task_type,
        status=TaskStatus.ORDERED,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def transition_task_db(
    db: Session,
    task_id: str,
    new_status: TaskStatus,
    reason: str,
) -> TaskDB:
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise ValueError("Task not found")

    if not reason.strip():
        raise ValueError("Transition reason is required")

    # Validate business rule
    current_status: TaskStatus = task.status  # type: ignore[assignment]
    validate_transition(current_status, new_status)

    # Create audit event
    audit_event = AuditEventDB(
        id=str(uuid.uuid4()),
        task_id=task.id,
        previous_status=current_status,
        new_status=new_status,
        timestamp=datetime.utcnow(),
        reason=reason,
    )

    # Update task
    task.status = new_status  # type: ignore[assignment]
    task.updated_at = datetime.utcnow()  # type: ignore[assignment]
    task.audit_log.append(audit_event)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task