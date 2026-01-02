from datetime import datetime

from app.models import ClinicalTask, AuditEvent
from app.state_machine import validate_transition, TaskStatus


def transition_task(
    task: ClinicalTask,
    new_status: TaskStatus,
    reason: str,
) -> None:
    if not reason or not reason.strip():
        raise ValueError("Transition reason is required")

    validate_transition(task.status, new_status)

    audit_event = AuditEvent(
        task_id=task.id,
        previous_status=task.status,
        new_status=new_status,
        reason=reason,
    )

    task.status = new_status
    task.updated_at = datetime.utcnow()
    task.audit_log.append(audit_event)