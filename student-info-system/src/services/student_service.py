"""Student service: business logic + JSON persistence (CRUD, search, export)."""
import csv
import json
import logging
import os
import tempfile
import xml.etree.ElementTree as ET
from typing import List, Optional

from src.models.student import Student
from src.utils import validators as v

logger = logging.getLogger("sis.service")


class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(Exception):
    """Raised when adding a student whose ID already exists."""


class StudentService:
    """Manages student records stored in a JSON file."""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.students: List[Student] = []
        self._load()

    # ---------- persistence ----------
    def _load(self) -> None:
        """Load students from disk, recovering gracefully from bad data."""
        if not os.path.exists(self.data_file):
            logger.warning("Data file %s not found; starting empty.", self.data_file)
            self.students = []
            self._save()
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.students = [Student.from_dict(item) for item in raw]
            logger.info("Loaded %d students.", len(self.students))
        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
            # Advanced error recovery: back up the corrupt file, start fresh.
            backup = self.data_file + ".corrupt"
            os.replace(self.data_file, backup)
            logger.error("Corrupt data file (%s). Backed up to %s.", exc, backup)
            self.students = []
            self._save()

    def _save(self) -> None:
        """Atomically write students to disk (temp file + replace)."""
        folder = os.path.dirname(self.data_file) or "."
        os.makedirs(folder, exist_ok=True)
        try:
            fd, tmp = tempfile.mkstemp(dir=folder, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in self.students], f, indent=2)
            os.replace(tmp, self.data_file)
        except OSError:
            logger.exception("Failed to save data file.")
            raise

    # ---------- CRUD ----------
    def add_student(self, student_id, name, age, course, email) -> Student:
        """Validate input and add a new student."""
        student = Student(
            student_id=v.validate_student_id(student_id),
            name=v.validate_name(name),
            age=v.validate_age(age),
            course=v.validate_course(course),
            email=v.validate_email(email),
        )
        if self._find(student.student_id):
            raise DuplicateStudentError(f"ID '{student.student_id}' already exists.")
        self.students.append(student)
        self._save()
        logger.info("Added student %s", student.student_id)
        return student

    def get_all(self) -> List[Student]:
        return list(self.students)

    def get_student(self, student_id: str) -> Student:
        student = self._find(student_id)
        if not student:
            raise StudentNotFoundError(f"No student with ID '{student_id}'.")
        return student

    def update_student(self, student_id: str, **fields) -> Student:
        """Update only the provided (non-empty) fields."""
        student = self.get_student(student_id)
        validators = {"name": v.validate_name, "age": v.validate_age,
                      "course": v.validate_course, "email": v.validate_email}
        for key, value in fields.items():
            if value in (None, ""):
                continue
            if key not in validators:
                raise ValueError(f"Cannot update field '{key}'.")
            setattr(student, key, validators[key](value))
        self._save()
        logger.info("Updated student %s", student_id)
        return student

    def delete_student(self, student_id: str) -> None:
        student = self.get_student(student_id)
        self.students.remove(student)
        self._save()
        logger.info("Deleted student %s", student_id)

    # ---------- bonus ----------
    def search(self, keyword: str) -> List[Student]:
        """Case-insensitive search across ID, name, course and email."""
        kw = keyword.strip().lower()
        return [s for s in self.students
                if kw in " ".join(str(x) for x in s.to_dict().values()).lower()]

    def export_csv(self, export_dir: str, filename: Optional[str] = None) -> str:
        """Export all records to CSV and return the file path."""
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir, filename or "students_export.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["student_id", "name", "age", "course", "email"])
            writer.writeheader()
            writer.writerows(s.to_dict() for s in self.students)
        logger.info("Exported %d students to %s", len(self.students), path)
        return path

    def export_xml(self, export_dir: str, filename: Optional[str] = None) -> str:
        """Export all records to XML and return the file path.

        Complements the JSON data store so records can be consumed by
        XML-based systems (the exam requires JSON/XML storage support).
        """
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir, filename or "students_export.xml")
        root = ET.Element("students")
        for s in self.students:
            record = ET.SubElement(root, "student")
            for key, value in s.to_dict().items():
                child = ET.SubElement(record, key)
                child.text = str(value)
        tree = ET.ElementTree(root)
        if hasattr(ET, "indent"):        # pretty-print on Python 3.9+
            ET.indent(tree, space="  ")
        tree.write(path, encoding="utf-8", xml_declaration=True)
        logger.info("Exported %d students to %s", len(self.students), path)
        return path

    # ---------- helpers ----------
    def _find(self, student_id: str) -> Optional[Student]:
        sid = str(student_id).strip().lower()
        return next((s for s in self.students
                     if s.student_id.lower() == sid), None)
