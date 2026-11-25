
# MAINTAINX
## Predictive Industrial Equipment Intelligence

MAINTAINX is a prototype predictive maintenance platform designed to demonstrate how industrial equipment telemetry can be transformed into actionable condition intelligence and integrated into an enterprise maintenance workflow.

The initial use case focuses on a mining cone crusher and the monitoring of countershaft bearing degradation.

## Project objectives

- Register and organise industrial equipment, components and sensors.
- Ingest and store equipment telemetry.
- Generate analytical features from sensor readings.
- Identify abnormal equipment behaviour using a rule-based condition assessment engine.
- Store assessment history and recommendations.
- Provide a REST API for enterprise integration.
- Demonstrate how predictive maintenance intelligence can be surfaced within Microsoft Dynamics 365 Business Central.

## Architecture

```text
                  MAINTAINX
                      |
        +-------------+-------------+
        |                           |
  Predictive Engine           Business Central
        |                      AL Extension
        |                           |
     FastAPI <----------------> API Client
        |                           |
   SQLAlchemy                 Synchronisation
        |                           |
    PostgreSQL                Equipment Records
        |                     Health Assessments
  Telemetry Data              Assessment Findings
  Feature Analysis
  Condition Engine
```

### Technology stack

| Layer | Technologies |
|---|---|
| Backend API | Python, FastAPI |
| Data processing | Pandas, NumPy |
| Database | PostgreSQL |
| ORM and migrations | SQLAlchemy, Alembic |
| Validation | Pydantic |
| Enterprise integration | Microsoft Dynamics 365 Business Central AL |
| Development tools | VS Code, Git, GitHub |

## Predictive maintenance workflow

1. Register industrial equipment.
2. Register equipment components and associated sensors.
3. Generate synthetic vibration and temperature telemetry.
4. Persist readings in PostgreSQL.
5. Calculate rolling statistical features.
6. Evaluate sensor behaviour using a rule-based condition engine.
7. Generate a condition assessment, findings and recommendations.
8. Expose assessment records through the FastAPI REST API.
9. Synchronise assessment information into the Business Central extension.

## Initial demonstration scenario

**Equipment:** Primary Cone Crusher  
**Component:** Countershaft Bearing  
**Sensors:**
- Vibration RMS (`mm/s`)
- Bearing temperature (`°C`)

The demonstration dataset contains 600 synthetic readings across vibration and temperature sensors. It represents normal, early-degradation and advanced-degradation phases.

The assessment engine evaluates rolling sensor features and produces condition classifications, findings and recommendations.

**Important:** The telemetry is synthetic and the assessment thresholds are illustrative development values. They are not validated OEM limits, calibrated failure probabilities, or predictions of remaining useful life. The prototype demonstrates the analytical workflow, not a validated industrial diagnostic model.

## Predictive Engine Setup

### Requirements

- Python 3.14 or a compatible Python environment
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Thube-Sithole/MAINTAINX.git
cd MAINTAINX
```

### 2. Create and activate a virtual environment

```powershell
cd predictive-engine
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the repository root:

```env
APP_NAME=MAINTAINX
APP_ENV=development
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=maintainx_db
```

Do not commit your `.env` file or database credentials.

### 5. Apply database migrations

From the `predictive-engine` directory:

```powershell
python -m alembic -c ..\alembic.ini upgrade head
```

### 6. Start the API

```powershell
python -m uvicorn app.main:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

Health endpoint:

`http://127.0.0.1:8000/health`

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/equipment/` | List registered equipment |
| GET | `/equipment/{equipment_id}` | Retrieve equipment |
| POST | `/equipment/{equipment_id}/assess` | Execute a condition assessment |
| GET | `/assessments/` | Retrieve assessment history |
| GET | `/assessments/{assessment_id}` | Retrieve an individual assessment |

Assessment history supports pagination through `limit` and `offset`.

## Business Central integration

The `business-central` directory contains the AL extension source for the MAINTAINX enterprise integration.

The extension includes:

- Equipment records and list/card pages.
- Health assessment records and list/card pages.
- Assessment finding records and a findings subpage.
- Equipment condition enumeration.
- API client codeunit.
- JSON parsing codeunit.
- Assessment synchronisation codeunit.
- Integration setup page and table.
- MAINTAINX Role Center and profile.

The intended integration allows Business Central users to view equipment records and synchronised predictive health assessments without duplicating the telemetry analytics engine inside the ERP.

### Integration status and verification

The AL source has been drafted, but compilation and deployment against a live Business Central environment have not been completed. A Business Central tenant and its application/system symbols are required to complete that verification.

The Python API and database workflows have been exercised independently. The Business Central integration should therefore be regarded as an implementation-stage prototype, not a deployed production integration.

## Current limitations and future development

- Replace synthetic telemetry with real industrial sensor data.
- Validate condition thresholds against OEM specifications and operational data.
- Develop and validate machine-learning models for anomaly detection and predictive maintenance.
- Investigate remaining-useful-life estimation using suitable labelled datasets.
- Add automated backend tests and broader input validation.
- Improve API authentication, authorisation and operational security.
- Complete AL compilation, Business Central deployment and end-to-end integration testing.
- Introduce secure cloud hosting and production monitoring.

## Author

**Thubelihle Sithole**

GitHub: https://github.com/Thube-Sithole

Project repository: https://github.com/Thube-Sithole/MAINTAINX
