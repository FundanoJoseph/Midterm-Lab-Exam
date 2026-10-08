# Student Information System

A console-based, **cloud-ready** Student Information System written in Python.
It supports full CRUD management of student records stored in JSON, with
configuration management, logging, validation, search and CSV export.

**Repository:** https://github.com/FundanoJoseph/Midterm-Lab-Exam
(the project lives in the `student-info-system/` folder of this repository)

## Features Implemented

| # | Feature | Rubric Area |
|---|---------|-------------|
| 1 | Add new students (with validation) | CRUD – Create |
| 2 | View all student records | CRUD – Read |
| 3 | Update student information (partial updates) | CRUD – Update |
| 4 | Delete students (with confirmation) | CRUD – Delete |
| 5 | JSON data storage with atomic saves (XML export supported) | Data Persistence |
| 6 | Clear interactive menu system | User Interface |
| 7 | Modular code structure (models / services / utils) | Cloud Architecture |
| 8 | External configuration file + env-var overrides | Configuration Management |
| 9 | Comprehensive error handling & corrupt-file recovery | Error Handling |
| 10 | Rotating logging system (`logs/app.log`) | Logging |
| 11 | Unit tests with pytest (9 tests) | Bonus |
| 12 | Data validation (ID, name, age, course, email) | Bonus |
| 13 | Search by ID, name, course or email | Bonus |
| 14 | Data export to CSV **and XML** | Bonus + JSON/XML storage |
| 15 | Advanced error recovery (corrupt data backup) | Bonus |
| 16 | GitHub Actions CI workflow (`.github/workflows/ci.yml`) | GitHub Integration |

## Project Structure
```
student-info-system/
├── src/
│   ├── models/student.py           # Student dataclass
│   ├── services/student_service.py # CRUD, search, export, persistence
│   ├── utils/                      # config, logger, validators
│   └── main.py                     # Console menu (entry point)
├── data/students.json              # Data store (JSON)
├── config/config.json              # Settings
├── logs/                           # Log output (gitignored)
├── tests/                          # Unit tests
├── docs/git_commands.sh            # Git workflow cheat sheet
├── requirements.txt
└── README.md
```

## Getting Started
```bash
git clone https://github.com/FundanoJoseph/Midterm-Lab-Exam.git
cd Midterm-Lab-Exam/student-info-system
python -m src.main
```
Requires Python 3.8+. No third-party packages are needed to run the app
(standard library only).

### Run the tests
```bash
pip install -r requirements.txt
pytest
```

## Configuration
Edit `config/config.json`:

| Key | Description |
|-----|-------------|
| `data_file` | Path of the JSON data store |
| `export_dir` | Folder for CSV exports |
| `logging.level` | DEBUG, INFO, WARNING, ERROR |
| `logging.file` | Log file path |
| `logging.max_bytes` / `backup_count` | Log rotation settings |

Environment overrides (cloud-friendly): `SIS_DATA_FILE`, `SIS_LOG_LEVEL`.

## Sample Data Format
Records are **stored** in JSON (`data/students.json`) and can be **exported**
to CSV or XML (`data/exports/`):

```json
[
  {"student_id": "S001", "name": "Juan Dela Cruz", "age": 20,
   "course": "BSIT", "email": "juan.delacruz@example.com"}
]
```

```xml
<?xml version='1.0' encoding='utf-8'?>
<students>
  <student>
    <student_id>S001</student_id>
    <name>Juan Dela Cruz</name>
    <age>20</age>
    <course>BSIT</course>
    <email>juan.delacruz@example.com</email>
  </student>
</students>
```

## Cloud-Ready Design
- **Modular layers** (model / service / utils) with clear separation of concerns
- **External configuration**, overridable through environment variables —
  the same image can run in dev, staging or production
- **Structured logging** suitable for log aggregation (e.g. CloudWatch, ELK)
- **Stateless app logic**: the storage path is configurable so it can point
  to a mounted cloud volume or object-sync folder
- **Atomic file writes** (temp file + `os.replace`) prevent data loss on crash
- **Error recovery**: a corrupt data file is backed up to
  `students.json.corrupt` and replaced with a fresh store instead of crashing

## Git Workflow
- Work is committed on the feature branch `arena/8a623f42-midterm-lab-exam`
  with a logical, meaningful commit history (conventional-commit style:
  `feat:`, `fix:`, `test:`, `docs:`, `chore:`)
- The branch is pushed to GitHub and merged into `main` through a
  **pull request** so every change is reviewed
- A suggested feature-branch workflow is documented in
  `docs/git_commands.sh`
- **GitHub Actions** runs the test suite automatically on every push
  (`.github/workflows/ci.yml`)

## Challenges Faced
1. **Externally-managed Python environment (PEP 668)** — `pip install`
   was blocked system-wide; solved by testing inside a virtual environment
   and keeping the app itself standard-library-only.
2. **Data integrity on crash** — a plain `json.dump` can leave a truncated
   file; solved with atomic writes (write to temp file, then `os.replace`).
3. **Corrupt data recovery** — a hand-edited/broken `students.json` used to
   crash the app; solved by backing up the bad file and starting fresh.
4. **Keeping the menu UI clean** — logging to the console interfered with
   the interactive menu; solved by sending only ERROR+ to console and
   everything to the rotating log file.
5. **Duplicate handler bug** — re-initializing the logger added duplicate
   handlers; solved with a guard in `setup_logger`.

## Author
**Joseph Fundano** — BS Information Technology, Pan Pacific University
GitHub: [@FundanoJoseph](https://github.com/FundanoJoseph)
