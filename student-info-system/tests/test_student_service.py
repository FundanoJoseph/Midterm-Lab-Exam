"""Unit tests for StudentService. Run with: pytest"""
import json
import pytest

from src.services.student_service import (
    DuplicateStudentError, StudentNotFoundError, StudentService)
from src.utils.validators import ValidationError


@pytest.fixture
def service(tmp_path):
    return StudentService(str(tmp_path / "students.json"))


def add_sample(service, sid="S001"):
    return service.add_student(sid, "Juan Dela Cruz", 20, "BSIT", "juan@example.com")


def test_add_and_get(service):
    add_sample(service)
    assert service.get_student("S001").name == "Juan Dela Cruz"


def test_duplicate_id_rejected(service):
    add_sample(service)
    with pytest.raises(DuplicateStudentError):
        add_sample(service)


def test_update(service):
    add_sample(service)
    service.update_student("S001", course="BSCS", age="21")
    s = service.get_student("S001")
    assert s.course == "BSCS" and s.age == 21


def test_delete(service):
    add_sample(service)
    service.delete_student("S001")
    with pytest.raises(StudentNotFoundError):
        service.get_student("S001")


def test_validation(service):
    with pytest.raises(ValidationError):
        service.add_student("S002", "Ana", 200, "BSIT", "ana@example.com")
    with pytest.raises(ValidationError):
        service.add_student("S002", "Ana", 20, "BSIT", "not-an-email")


def test_persistence(tmp_path):
    path = str(tmp_path / "s.json")
    StudentService(path).add_student("S001", "Maria Clara", 19, "BSIT", "m@x.com")
    assert len(StudentService(path).get_all()) == 1


def test_search(service):
    add_sample(service)
    assert len(service.search("juan")) == 1
    assert service.search("zzz") == []


def test_corrupt_file_recovery(tmp_path):
    path = tmp_path / "s.json"
    path.write_text("{ not valid json")
    service = StudentService(str(path))
    assert service.get_all() == []
    assert (tmp_path / "s.json.corrupt").exists()


def test_export_csv(service, tmp_path):
    add_sample(service)
    out = service.export_csv(str(tmp_path / "exports"))
    assert "S001" in open(out, encoding="utf-8").read()
