#  Feedback Report Generator

A Django-based API service to generate student feedback reports in PDF or HTML format. The project is containerized with Docker for easy deployment.

---

## Getting Started

### Prerequisites

- Docker & Docker Compose installed
- Python 3.9+ (if running locally without Docker)
- Git (to clone the repository)

---

###  Local Setup (Using Docker Compose)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ghiri35/feedback-report-generator.git
   cd feedback-report-generator
   ```

2. **Start Docker containers**:
   ```bash
   docker compose up --build
   ```

3. **Apply migrations and create tables**:
   ```bash
   docker compose exec django python manage.py migrate
   ```

4. **Access the app**:
   Navigate to `http://localhost:8000` (or `http://0.0.0.0:8000`)

---

##  API Endpoints

### `POST /assignment/html`
**Generates an HTML report.**

- **Input (JSON)**:
  ```json
  {
    "student_id": "123",
    "event_order": "E1",
    "content_type": "HTML"
  }
  ```

- **Output**:
  - Returns a URL pointing to the generated HTML file inside `/media/reports`.

---

### `POST /assignment/pdf`
**Generates a PDF report.**

- **Input (JSON)**:
  ```json
  {
    "student_id": "123",
    "event_order": "E1",
    "content_type": "PDF"
  }
  ```

- **Output**:
  - Returns a URL pointing to the generated PDF file inside `/media/reports`.

---

##  Project Structure

- `core/` — Django app code
- `media/reports/` — Output folder for generated reports
- `Dockerfile` — Image build instructions for Django app
- `Dockerfile.celery` — Optional Celery configuration (if used)
- `docker-compose.yml` — Multi-container orchestration
- `report/` — Template or generation logic (assumed)
- `wait-for-it.sh` — Ensures DB is ready before Django starts

---

## Assumptions & Design Decisions

- Static files and reports are stored in `/media/reports` and served locally for development.
- File generation uses `reportlab` for PDFs and Django templates for HTML.
- Only two report types are currently supported (`PDF`, `HTML`).
- The app runs inside Docker using a separate service for the database (PostgreSQL or SQLite assumed).
- Environment configuration and secret management are expected via `.env` (not included here).

---

## To Do / Improvements

- Add authentication for report generation
- Implement Celery for async report creation
- Add error logging and retry mechanisms
- Add automated tests

---

## Contact

Made with ❤️ by [ghiri](https://github.com/ghiri35)
