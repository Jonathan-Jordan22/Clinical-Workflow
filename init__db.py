from app.database import Base, engine
from app.db_models import PatientDB, TaskDB, AuditEventDB

Base.metadata.create_all(bind=engine)
print("Database initialized!")