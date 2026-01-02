import pytest

from app.models import ClinicalTask
from app.services import transition_task
from app.state_machine import TaskStatus, InvalidTransitionError


def test_valid_transition():
    task = ClinicalTask()
    transition_task(task, TaskStatus.IN_PROGRESS, "Started work")

    assert task.status == TaskStatus.IN_PROGRESS
    assert len(task.audit_log) == 1
    assert task.audit_log[0].previous_status == TaskStatus.ORDERED
    assert task.audit_log[0].new_status == TaskStatus.IN_PROGRESS


def test_invalid_transition():
    task = ClinicalTask(status=TaskStatus.COMPLETED)

    with pytest.raises(InvalidTransitionError):
        transition_task(task, TaskStatus.IN_PROGRESS, "Invalid transition")


def test_reason_required():
    task = ClinicalTask()

    with pytest.raises(ValueError):
        transition_task(task, TaskStatus.IN_PROGRESS, "")