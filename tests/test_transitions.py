import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.services import create_patient_db, create_task_db, transition_task_db
from app.state_machine import TaskStatus, InvalidTransitionError


# Setup test database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_valid_transition(db):
    patient = create_patient_db(db, "John Doe", "1990-01-01")
    task = create_task_db(db, patient.id, "lab_test")  # type: ignore[arg-type]
    
    transition_task_db(db, task.id, TaskStatus.IN_PROGRESS, "Started work")  # type: ignore[arg-type]
    
    db.refresh(task)
    assert task.status == TaskStatus.IN_PROGRESS  # type: ignore[comparison-overlap]
    assert len(task.audit_log) == 1
    assert task.audit_log[0].previous_status == TaskStatus.ORDERED
    assert task.audit_log[0].new_status == TaskStatus.IN_PROGRESS


def test_invalid_transition(db):
    patient = create_patient_db(db, "Jane Doe", "1985-05-15")
    task = create_task_db(db, patient.id, "imaging")  # type: ignore[arg-type]
    
    # Complete the task first
    transition_task_db(db, task.id, TaskStatus.IN_PROGRESS, "Started")  # type: ignore[arg-type]
    transition_task_db(db, task.id, TaskStatus.COMPLETED, "Finished")  # type: ignore[arg-type]

    with pytest.raises(InvalidTransitionError):
        transition_task_db(db, task.id, TaskStatus.IN_PROGRESS, "Invalid transition")  # type: ignore[arg-type]


def test_reason_required(db):
    patient = create_patient_db(db, "Bob Smith", "1975-03-20")
    task = create_task_db(db, patient.id, "consultation")  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        transition_task_db(db, task.id, TaskStatus.IN_PROGRESS, "")  # type: ignore[arg-type]