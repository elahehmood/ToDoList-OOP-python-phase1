from datetime import date, datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from phase3_api.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(20), default="todo", nullable=False)

    # Optional deadline: can be NULL
    deadline = Column(Date, nullable=True)

    # When the task is actually finished (status becomes "done")
    closed_at = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="tasks")

    @property
    def is_overdue(self) -> bool:
        """Return True if the task is late compared to its deadline."""
        if self.deadline is None:
            return False

        # Not closed yet → compare today's date with the deadline
        if self.closed_at is None:
            return date.today() > self.deadline

        # Closed → compare close date with the deadline
        return self.closed_at.date() > self.deadline

    @property
    def remaining_days(self) -> int | None:
        """Number of days remaining until deadline (negative if overdue)."""
        if self.deadline is None:
            return None
        return (self.deadline - date.today()).days
