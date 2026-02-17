# Mini Resume Management API

A REST API built using FastAPI to manage candidate resumes.

This application allows:

- Uploading candidate resumes (PDF/DOC/DOCX)
- Storing candidate metadata in memory (no database)
- Filtering and retrieving candidates via structured REST endpoints
- Deleting candidates and associated files

## Technology Stack

- Python 3.10
- FastAPI
- Uvicorn
- Pydantic
- python-multipart

## Project Structure

miniresume-risma-jasmine/
├── main.py #main FastAPI application
├── requirements.txt #python dependencies
└── README.md

##Installation steps

# 1️. Clone the Repository

bash:
git clone
cd

# 2. Create and activate a virtual environment

bash:
python -m venv venv

activate for windows:
bash:
venv\Scripts\activate

activate for mac/linux:
bash:
source venv/bin/activate

# 3. Install Dependencies:

bash:
pip install -r requirements.txt

## Run the Application:

bash:
uvicorn main:app --reload

Server will start at:
http://127.0.0.1:8000

## API Documentation

Swagger UI:
http://127.0.0.1:8000/docs

## Health Check

Endpoint
GET /health

Respone:
{
"status": "ok"
}

Status Code: 200 OK

## Create Candidate

Endpoint
POST /candidates

Form Data Required
Field Type
full_name string
dob string (YYYY-MM-DD)
contact_number string
contact_address string
education_qualification string
graduation_year integer
years_of_experience integer
skill_set string
resume file (PDF/DOC/DOCX)

Success Response:
{
"message": "Candidate created successfully",
"candidate_id": "uuid-value"
}

Status Code: 201 Created

## List Candidates

Endpoint
GET /candidates

Optional Query Parameters

skill

experience

graduation_year

Example:

/candidates?skill=python

Response:
[
{
"id": "uuid",
"full_name": "John Doe",
"dob": "2000-01-01",
"contact_number": "9876543210",
"contact_address": "Chennai",
"education_qualification": "MCA",
"graduation_year": 2024,
"years_of_experience": 1,
"skill_set": "Python, FastAPI"
}
]

Status Code: 200 OK

## Get Candidate by ID

Endpoint
GET /candidates/{candidate_id}

Success Response:
{
"id": "uuid",
"full_name": "John Doe",
...
}

Status Code: 200 OK

If not found:

{
"detail": "Candidate not found"
}

Status Code: 404 Not Found

## Delete Candidate

Endpoint
DELETE /candidates/{candidate_id}

Status Code: 204 No Content

## Validation Rules

All fields are mandatory

DOB must be in YYYY-MM-DD format

Experience cannot be negative

Graduation year cannot be in the future

Resume file must be PDF, DOC, or DOCX

Invalid inputs return appropriate HTTP status codes (400 / 422)

## Notes:

Uploaded resume files are saved to the uploads/ directory, which is created automatically on first run.
Each candidate is assigned a unique UUID on creation.
