from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
import os



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
    description="REST API built using FastAPI to manage candidate resumes.",
    version="1.0",
    openapi_tags=tags_metadata
)


# In-Memory Storage
# ==============================

candidates = {}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Response Models
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
    resume: UploadFile = File(...)
):

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
    if graduation_year > current_year:
        raise HTTPException(status_code=400, detail="Invalid graduation year")

    # Validate File Type
    if not resume.filename.endswith((".pdf", ".doc", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF, DOC, DOCX files allowed")

    # Generate ID
    candidate_id = str(uuid4())

    # Save File
    file_path = os.path.join(UPLOAD_DIR, f"{candidate_id}_{resume.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(await resume.read())

    # Store in memory
    candidates[candidate_id] = {
        "id": candidate_id,
        "full_name": full_name,
        "dob": dob,
        "contact_number": contact_number,
        "contact_address": contact_address,
        "education_qualification": education_qualification,
        "graduation_year": graduation_year,
        "years_of_experience": years_of_experience,
        "skill_set": skill_set,
        "resume_file": file_path
    }

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
    description="Returns all candidates. Supports filtering by skill, experience and graduation year.",
    response_model=List[CandidateResponse],
    status_code=200
)
def list_candidates(
    skill: Optional[str] = Query(None),
    experience: Optional[int] = Query(None),
    graduation_year: Optional[int] = Query(None)
):

    result = []

    for candidate in candidates.values():

        if skill and skill.lower() not in candidate["skill_set"].lower():
            continue

        if experience is not None and candidate["years_of_experience"] != experience:
            continue

        if graduation_year is not None and candidate["graduation_year"] != graduation_year:
            continue

        result.append(candidate)

    return result

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
def get_candidate(candidate_id: str):

    if candidate_id not in candidates:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return candidates[candidate_id]


# Delete Candidate
# ==============================

@app.delete(
    "/candidates/{candidate_id}",
    tags=["Candidates"],
    summary="Delete Candidate",
    description="Deletes a candidate and their uploaded resume file.",
    status_code=204
)
def delete_candidate(candidate_id: str):

    if candidate_id not in candidates:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Remove file
    file_path = candidates[candidate_id]["resume_file"]
    if os.path.exists(file_path):
        os.remove(file_path)

    del candidates[candidate_id]

    return
