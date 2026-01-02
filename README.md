# Clinical Workflow Simulation System

This project models a simplified clinical task workflow, enforcing valid state transitions and maintaining a complete audit history for traceability and correctness.

## Core Concepts
- Explicit task lifecycle states
- Validated state transitions
- Mandatory audit logging for all changes

Further implementation details will be added as the system evolves.

## Persistence

Tasks, patients, and audit events are stored in a SQLite database with SQLAlchemy.
The system enforces referential integrity and audit tracking.