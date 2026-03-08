from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session
import os

from database import get_db, init_db, engine
from models import Candidate
import models

# OpenAPI Tags Metadata
# ==============================

tags_metadata = [
    {
        "name": "Candidates",
        "description": "Operations related to candidate resume management."
    }
]


# FastAPI App Configuration
# ==============================

app = FastAPI(
    title="Mini Resume Management API",
    description="REST API built using FastAPI to manage candidate resumes with database persistence.",
    version="1.0",
    openapi_tags=tags_metadata
)


# File Upload Directory
# ==============================

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Response Models (Pydantic)
# ==============================

class CandidateCreateResponse(BaseModel):
    message: str
    candidate_id: str


class CandidateResponse(BaseModel):
    id: str
    full_name: str
    dob: str
    contact_number: str
    contact_address: str
    education_qualification: str
    graduation_year: int
    years_of_experience: int
    skill_set: str

    class Config:
        from_attributes = True


# Application Startup Event
# ==============================

@app.on_event("startup")
def startup_event():
    """
    Initialize database tables on application startup.
    """
    init_db()
    print("✓ Database initialized successfully")


# ==============================
# Health Check Endpoint
# ==============================

@app.get(
    "/health",
    summary="Health Check",
    description="Checks if the API service is running.",
    status_code=200
)
def health_check():
    return {"status": "ok"}


# ==============================
# Create Candidate
# ==============================

@app.post(
    "/candidates",
    tags=["Candidates"],
    summary="Create Candidate",
    description="Registers a new candidate and uploads resume file.",
    response_model=CandidateCreateResponse,
    status_code=201
)
async def create_candidate(
    full_name: str = Form(...),
    dob: str = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education_qualification: str = Form(...),
    graduation_year: int = Form(...),
    years_of_experience: int = Form(...),
    skill_set: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Create a new candidate with resume upload.
    
    - **full_name**: Candidate's full name
    - **dob**: Date of birth (YYYY-MM-DD format)
    - **contact_number**: Contact phone number
    - **contact_address**: Residential address
    - **education_qualification**: Degree/qualification
    - **graduation_year**: Year of graduation
    - **years_of_experience**: Years of professional experience
    - **skill_set**: Comma-separated skills
    - **resume**: PDF/DOC/DOCX file
    """

    # Validate DOB format
    try:
        datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="DOB must be in YYYY-MM-DD format")

    # Validate Experience
    if years_of_experience < 0:
        raise HTTPException(status_code=400, detail="Experience cannot be negative")

    # Validate Graduation Year
    current_year = datetime.now().year
    if graduation_year < 1900 or graduation_year > current_year:
        raise HTTPException(status_code=400, detail="Graduation year must be between 1900 and current year")

    # Validate Contact Number (10-15 digits only)
    if not contact_number.isdigit():
        raise HTTPException(status_code=400, detail="Contact number must contain only digits")
    if len(contact_number) < 10 or len(contact_number) > 15:
        raise HTTPException(status_code=400, detail="Contact number must be 10-15 digits")

    # Validate File Type
    if not resume.filename.endswith((".pdf", ".doc", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF, DOC, DOCX files allowed")

    # Generate ID
    candidate_id = str(uuid4())

    # Save File
    file_path = os.path.join(UPLOAD_DIR, f"{candidate_id}_{resume.filename}")
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await resume.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save resume file: {str(e)}")

    # Create candidate record in database
    try:
        db_candidate = Candidate(
            id=candidate_id,
            full_name=full_name,
            dob=dob,
            contact_number=contact_number,
            contact_address=contact_address,
            education_qualification=education_qualification,
            graduation_year=graduation_year,
            years_of_experience=years_of_experience,
            skill_set=skill_set,
            resume_file=resume.filename 
        )
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
    except Exception as e:
        db.rollback()
        # Delete the uploaded file if database save fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to save candidate: {str(e)}")

    return {
        "message": "Candidate created successfully",
        "candidate_id": candidate_id
    }


# ==============================
# List Candidates (With Filters)
# ==============================

@app.get(
    "/candidates",
    tags=["Candidates"],
    summary="List Candidates",
    description="Returns all candidates with optional filtering by skill, experience, and graduation year.",
    response_model=List[CandidateResponse],
    status_code=200
)
def list_candidates(
    skill: Optional[str] = Query(None, description="Filter by skill (case-insensitive substring match)"),
    experience: Optional[int] = Query(None, description="Filter by exact years of experience"),
    graduation_year: Optional[int] = Query(None, description="Filter by graduation year"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all candidates with optional filters.
    
    Query Parameters:
    - **skill**: Filter candidates containing this skill (e.g., ?skill=python)
    - **experience**: Filter by exact years of experience (e.g., ?experience=5)
    - **graduation_year**: Filter by graduation year (e.g., ?graduation_year=2023)
    """
    query = db.query(Candidate)

    # Apply filters
    if skill:
        query = query.filter(Candidate.skill_set.ilike(f"%{skill}%"))

    if experience is not None:
        query = query.filter(Candidate.years_of_experience == experience)

    if graduation_year is not None:
        query = query.filter(Candidate.graduation_year == graduation_year)

    candidates = query.all()
    return candidates


# ==============================
# Get Candidate By ID
# ==============================

@app.get(
    "/candidates/{candidate_id}",
    tags=["Candidates"],
    summary="Get Candidate By ID",
    description="Fetches details of a specific candidate using their unique ID.",
    response_model=CandidateResponse,
    status_code=200
)
def get_candidate(candidate_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific candidate by their ID.
    
    - **candidate_id**: Unique UUID of the candidate
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return candidate


# ==============================
# Delete Candidate
# ==============================

@app.delete(
    "/candidates/{candidate_id}",
    tags=["Candidates"],
    summary="Delete Candidate",
    description="Deletes a candidate and their uploaded resume file.",
    status_code=204
)
def delete_candidate(candidate_id: str, db: Session = Depends(get_db)):
    """
    Delete a candidate and associated resume file.
    
    - **candidate_id**: Unique UUID of the candidate
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Remove file if it exists
    if os.path.exists(candidate.resume_file):
        try:
            os.remove(candidate.resume_file)
        except Exception as e:
            print(f"Warning: Failed to delete resume file: {str(e)}")

    # Delete from database
    try:
        db.delete(candidate)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete candidate: {str(e)}")

    return

@app.get(
    "/download-resume/{candidate_id}",
    tags=["Candidates"],
    summary="Download Candidate Resume",
    description="Download the uploaded resume file for a candidate."
)
def download_resume(candidate_id: str, db: Session = Depends(get_db)):

    # Get candidate from database
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Rebuild file path
    file_path = os.path.join(UPLOAD_DIR, f"{candidate_id}_{candidate.resume_file}")

    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume file not found")

    # Return file
    return FileResponse(
        path=file_path,
        filename=candidate.resume_file,
        media_type='application/octet-stream'
    )