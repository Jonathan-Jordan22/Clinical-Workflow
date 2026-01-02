from enum import Enum


class TaskStatus(str, Enum):
    ORDERED = "ORDERED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


ALLOWED_TRANSITIONS = {
    TaskStatus.ORDERED: {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
    TaskStatus.IN_PROGRESS: {TaskStatus.COMPLETED, TaskStatus.CANCELLED},
    TaskStatus.COMPLETED: set(),
    TaskStatus.CANCELLED: set(),
}


class InvalidTransitionError(Exception):
    pass


def validate_transition(current_status: TaskStatus, new_status: TaskStatus):
    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise InvalidTransitionError(
            f"Cannot transition from {current_status} to {new_status}"
        )