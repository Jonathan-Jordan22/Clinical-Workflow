from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.state_machine import TaskStatus


class PatientDB(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)

    tasks = relationship("TaskDB", back_populates="patient")


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    task_type = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.ORDERED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("PatientDB", back_populates="tasks")
    audit_log = relationship("AuditEventDB", back_populates="task")


class AuditEventDB(Base):
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True)
    task_id = Column(String, ForeignKey("tasks.id"))
    previous_status = Column(Enum(TaskStatus))
    new_status = Column(Enum(TaskStatus))
    timestamp = Column(DateTime, default=datetime.utcnow)
    reason = Column(String)

    task = relationship("TaskDB", back_populates="audit_log")