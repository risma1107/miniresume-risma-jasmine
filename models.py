from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class Candidate(Base):
    """
    SQLAlchemy model for storing candidate resume information.
    """
    __tablename__ = "candidates"

    id = Column(String(36), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    dob = Column(String(10), nullable=False)  # YYYY-MM-DD format
    contact_number = Column(String(20), nullable=False)
    contact_address = Column(String(500), nullable=False)
    education_qualification = Column(String(255), nullable=False)
    graduation_year = Column(Integer, nullable=False, index=True)
    years_of_experience = Column(Integer, nullable=False, index=True)
    skill_set = Column(String(1000), nullable=False, index=True)
    resume_file = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Candidate(id='{self.id}', full_name='{self.full_name}')>"