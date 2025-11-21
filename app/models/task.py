from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    status = Column(String(20), default="todo", nullable=False)
    deadline = Column(Date, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="tasks")
