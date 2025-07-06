import os
from datetime import datetime, timezone
from sqlalchemy import (
    create_engine, Column, String, Text, Float, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker

# Use DATABASE_URL from environment for PostgreSQL fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///namulundu.db")

Base = declarative_base()

class MemoryRecord(Base):
    __tablename__ = 'memories'
    id = Column(String, primary_key=True)
    book_id = Column(String)
    name = Column(String)
    condition = Column(String)
    content = Column(Text)
    book_balance = Column(Float, default=0.0)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    book_contact = Column(Text)         # NEW FIELD
    doctor = Column(String)               # NEW FIELD
    doctor_contact = Column(String)       # NEW FIELD

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create the table(s)
Base.metadata.create_all(engine)

# Session factory
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_memory_entry(memory):
    with SessionLocal() as db:
        record = MemoryRecord(
            id=memory["id"],
            timestamp=memory["timestamp"],
            book_id=memory["book_id"],
            name=memory["name"],
            condition=memory["condition"],
            content=memory["content"],
            book_balance=memory.get("book_balance", 0.0),
            book_contact=memory["book_contact"],         # NEW FIELD
            doctor=memory.get("doctor"),                     # NEW FIELD
            doctor_contact=memory.get("doctor_contact")     # NEW FIELD
        )
        db.merge(record)
        db.commit()

def load_all_memories():
    with SessionLocal() as db:
        records = db.query(MemoryRecord).all()
        return [
            {
                "id": r.id,
                "timestamp": r.timestamp,
                "book_id": r.book_id,
                "name": r.name,
                "condition": r.condition,
                "content": r.content,
                "book_balance": r.book_balance,
                "book_contact": r.book_contact,         # NEW FIELD
                "doctor": r.doctor,                     # NEW FIELD
                "doctor_contact": r.doctor_contact      # NEW FIELD
            }
            for r in records
        ]

def update_memory_entry(memory):
    with SessionLocal() as db:
        record = db.query(MemoryRecord).filter(MemoryRecord.id == memory["id"]).first()
        if record:
            record.timestamp = memory["timestamp"]
            record.book_id = memory["book_id"]
            record.name = memory["name"]
            record.condition = memory["condition"]
            record.content = memory["content"]
            record.book_balance = memory.get("book_balance", 0.0)
            record.book_contact = memory["book_contact"]         # NEW FIELD
            record.doctor = memory.get("doctor")                     # NEW FIELD
            record.doctor_contact = memory.get("doctor_contact")     # NEW FIELD
            db.commit()

def get_memory_by_id(memory_id):
    with SessionLocal() as db:
        record = db.query(MemoryRecord).filter(MemoryRecord.id == memory_id).first()
        if record:
            return {
                "id": record.id,
                "timestamp": record.timestamp,
                "book_id": record.book_id,
                "name": record.name,
                "condition": record.condition,
                "content": record.content,
                "book_balance": record.book_balance,
                "book_contact": record.book_contact,         # NEW FIELD
                "doctor": record.doctor,                     # NEW FIELD
                "doctor_contact": record.doctor_contact      # NEW FIELD
            }
        return None

def get_latest_book_balance(book_id):
    with SessionLocal() as db:
        record = (
            db.query(MemoryRecord)
            .filter(MemoryRecord.book_id == book_id)
            .order_by(MemoryRecord.timestamp.desc())
            .first()
        )
        if record and record.book_balance is not None:
            return record.book_balance
        return 0.0
