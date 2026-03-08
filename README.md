# Mini Resume Management API

A REST API built using FastAPI to manage candidate resumes with persistent database storage, comprehensive validation, and resume download capabilities.

# This application allows:

- Uploading candidate resumes (PDF/DOC/DOCX)
- Storing candidate data in Sqlite database
- Filtering and retrieving candidates via structured REST endpoints
- Deleting candidates and associated files

## Technology Stack

- Python 3.12.4
- FastAPI 0.129.0
- Uvicorn 0.40.0
- Pydantic 2.12.5
- python-multipart 0.0.22
- sqlalchemy 2.0.23

## Project Structure

```
miniresume-risma-jasmine/
├── main.py                   #main FastAPI application
├── requirements.txt          #python dependencies
├── database.py               # Database configuration
├── models.py                 # SQLAlchemy data models
├── .gitignore
└── README.md
```

## Installation steps

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

# 1️. Clone the Repository

```bash
git clone <repository-url>
cd miniresume-risma-jasmine
```

# 2. Create and activate a virtual environment

```bash
python -m venv venv
```

# 3. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

# 4. Install Dependencies:

```bash
pip install -r requirements.txt
```

# 5. Run the Application:

```bash
uvicorn main:app --reload
```

You should see:

```
✓ Database initialized successfully
INFO: Uvicorn running on http://127.0.0.1:8000
```

## 6. API Documentation

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

You'll see the **Swagger UI** with all available endpoints!

---

## API Endpoinks

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Checks if the API service is running.

**Response:**

```json
{
  "status": "ok"
}
```

**Status Code:** `200 OK`

---

### 2. Create Candidate

**Endpoint:** `POST /candidates`

**Description:** Register a new candidate and upload their resume.

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

**Success Response:**

```json
{
  "message": "Candidate created successfully",
  "candidate_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Status Code:** `201 Created`

**Error Responses:**

| Status Code | Reason         | Example                                                 |
| ----------- | -------------- | ------------------------------------------------------- |
| `400`       | Invalid input  | "Contact number must be 10-15 digits"                   |
| `400`       | Invalid format | "DOB must be in YYYY-MM-DD format"                      |
| `400`       | Invalid year   | "Graduation year must be between 1900 and current year" |
| `400`       | Invalid file   | "Only PDF, DOC, DOCX files allowed"                     |
| `422`       | Missing field  | Field is required                                       |

---

### 3. List All Candidates

**Endpoint:** `GET /candidates`

**Description:** Retrieve all candidates with optional filtering.

**Query Parameters (All Optional):**

| Parameter         | Type    | Description                        | Example                 |
| ----------------- | ------- | ---------------------------------- | ----------------------- |
| `skill`           | string  | Filter by skill (case-insensitive) | `?skill=Python`         |
| `experience`      | integer | Filter by exact years              | `?experience=5`         |
| `graduation_year` | integer | Filter by year                     | `?graduation_year=2020` |

**Examples:**

```bash
# Get all candidates (no filters)
GET /candidates

# Filter by skill
GET /candidates?skill=Python

# Filter by experience
GET /candidates?experience=5

# Filter by graduation year
GET /candidates?graduation_year=2020

# Multiple filters (all must match)
GET /candidates?skill=Python&experience=3&graduation_year=2020
```

**Response:**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "Jake Smith",
    "dob": "2002-07-11",
    "contact_number": "9876543210",
    "contact_address": "New York",
    "education_qualification": "MCA",
    "graduation_year": 2020,
    "years_of_experience": 2,
    "skill_set": "Python, FastAPI, SQLAlchemy"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "full_name": "Jane Doe",
    "dob": "1999-05-20",
    "contact_number": "8765432109",
    "contact_address": "Boston",
    "education_qualification": "B.Tech",
    "graduation_year": 2021,
    "years_of_experience": 3,
    "skill_set": "Java, Spring Boot"
  }
]
```

**Status Code:** `200 OK`

---

### 4. Get Candidate by ID

**Endpoint:** `GET /candidates/{candidate_id}`

**Description:** Fetch details of a specific candidate.

**Path Parameters:**

| Parameter      | Type   | Description           |
| -------------- | ------ | --------------------- |
| `candidate_id` | string | UUID of the candidate |

**Example:**

```bash
GET /candidates/550e8400-e29b-41d4-a716-446655440000
```

**Success Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "full_name": "Jake Smith",
  "dob": "2002-07-11",
  "contact_number": "9876543210",
  "contact_address": "New York",
  "education_qualification": "MCA",
  "graduation_year": 2020,
  "years_of_experience": 2,
  "skill_set": "Python, FastAPI, SQLAlchemy"
}
```

**Status Code:** `200 OK`

**Error Response (if not found):**

```json
{
  "detail": "Candidate not found"
}
```

**Status Code:** `404 Not Found`

---

### 5. Download Resume

**Endpoint:** `GET /candidates/{candidate_id}/download-resume`

**Description:** Download a candidate's resume file.

**Path Parameters:**

| Parameter      | Type   | Description           |
| -------------- | ------ | --------------------- |
| `candidate_id` | string | UUID of the candidate |

**Success Response:** Binary file (PDF/DOC/DOCX) for download

**Status Code:** `200 OK`

**Error Response (if not found):**

```json
{
  "detail": "Candidate not found"
}
```

**Status Code:** `404 Not Found`

---

### 6. Delete Candidate

**Endpoint:** `DELETE /candidates/{candidate_id}`

**Description:** Delete a candidate and their uploaded resume file.

**Path Parameters:**

| Parameter      | Type   | Description           |
| -------------- | ------ | --------------------- |
| `candidate_id` | string | UUID of the candidate |

**Example:**

```bash
DELETE /candidates/550e8400-e29b-41d4-a716-446655440000
```

**Status Code:** `204 No Content`

**Error Response (if not found):**

```json
{
  "detail": "Candidate not found"
}
```

**Status Code:** `404 Not Found`

---

## Validation Rules

All fields are mandatory

DOB must be in YYYY-MM-DD format

Contact number must contain only 10–15 digits.

Experience cannot be negative

Graduation year cannot be in the future and must be a 4-digit year between 1900

Resume file must be PDF, DOC, or DOCX

### Validation Error Examples:

**Invalid Contact Number:**

```json
{
  "detail": "Contact number must be 10-15 digits"
}
```

**Invalid Graduation Year:**

```json
{
  "detail": "Graduation year must be between 1900 and current year"
}
```

**Invalid Date Format:**

```json
{
  "detail": "DOB must be in YYYY-MM-DD format"
}
```

**Invalid File Type:**

```json
{
  "detail": "Only PDF, DOC, DOCX files allowed"
}
```

---

## 🗄️ Database

### SQLite (Default)

Database file: `candidates.db`

Located in your project root directory. No external database server needed!

**Table Structure:**

```sql
candidates
├── id (VARCHAR 36)              Primary Key, UUID
├── full_name (VARCHAR 255)      Indexed for fast search
├── dob (VARCHAR 10)             Date of birth (YYYY-MM-DD)
├── contact_number (VARCHAR 20)  Phone number
├── contact_address (VARCHAR 500) Residential address
├── education_qualification (VARCHAR 255) Degree/qualification
├── graduation_year (INTEGER)    Indexed for filtering
├── years_of_experience (INTEGER) Indexed for filtering
├── skill_set (VARCHAR 1000)     Indexed for searching
├── resume_file (VARCHAR 500)    File path on disk
├── created_at (DATETIME)        Auto-timestamp on create
└── updated_at (DATETIME)        Auto-updated on modify
```

### View Database Contents

#### Method 1: SQLite Extension in VS Code (Easiest!) ⭐

**Install the extension:**

1. Open VS Code
2. Go to Extensions (Ctrl + Shift + X)
3. Search for "SQLite" or "SQLite Viewer"
4. Install the SQLite extension by alexcvzz or similar
5. Reload VS Code

**View your database:**

1. Right-click on `candidates.db` file in Explorer
2. Select "Open Database"
3. You'll see tables in the Explorer sidebar
4. Right-click `candidates` table → "Show Table"
5. **View data in a beautiful table structure!** 📊

**Benefits:**

- ✅ View data in table format (no coding needed)
- ✅ Run SQL queries directly in VS Code
- ✅ See table structure visually
- ✅ Edit data directly if needed
- ✅ No command line required

---

## 🗄️ Database

### SQLite (Default)

Database file: `candidates.db`

Located in your project root directory. No external database server needed!

**Table Structure:**

```sql
candidates
├── id (VARCHAR 36)              Primary Key, UUID
├── full_name (VARCHAR 255)      Indexed for fast search
├── dob (VARCHAR 10)             Date of birth (YYYY-MM-DD)
├── contact_number (VARCHAR 20)  Phone number
├── contact_address (VARCHAR 500) Residential address
├── education_qualification (VARCHAR 255) Degree/qualification
├── graduation_year (INTEGER)    Indexed for filtering
├── years_of_experience (INTEGER) Indexed for filtering
├── skill_set (VARCHAR 1000)     Indexed for searching
├── resume_file (VARCHAR 500)    File path on disk
├── created_at (DATETIME)        Auto-timestamp on create
└── updated_at (DATETIME)        Auto-updated on modify
```

### View Database Contents

# SQLite Extension in VS Code (Easiest!) ⭐

**Install the extension:**

1. Open VS Code
2. Go to Extensions (Ctrl + Shift + X)
3. Search for "free SQLite"
4. Install the SQLite extension
5. Reload VS Code

**View your database:**

1. Right-click on `candidates.db` file in Explorer
2. Select "Open Database"
3. You'll see tables in the Explorer sidebar
4. Right-click `candidates` table → "Show Table"
5. **View data in a beautiful table structure!** 📊

**Benefits:**

- ✅ View data in table format (no coding needed)
- ✅ Run SQL queries directly in VS Code
- ✅ See table structure visually
- ✅ Edit data directly if needed
- ✅ No command line required

---
