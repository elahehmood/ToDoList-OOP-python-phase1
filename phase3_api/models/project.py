from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from phase3_api.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)
    description = Column(String(150), nullable=True)

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
    )
