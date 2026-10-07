"""Console entry point for the Student Information System.

Run from the project root:  python -m src.main
"""
import logging

from src.services.student_service import (
    DuplicateStudentError, StudentNotFoundError, StudentService)
from src.utils.config import load_config
from src.utils.logger import setup_logger
from src.utils.validators import ValidationError

MENU = """
===== Student Information System =====
1. Add student
2. View all students
3. Update student
4. Delete student
5. Search students
6. Export to CSV
0. Exit
"""


def print_students(students) -> None:
    """Pretty-print a list of students."""
    if not students:
        print("No records found.")
        return
    print(f"{'ID':<10} {'Name':<22} {'Age':<4} {'Course':<18} Email")
    print("-" * 75)
    for s in students:
        print(s)


def add_student(service: StudentService) -> None:
    service.add_student(
        input("ID: "), input("Name: "), input("Age: "),
        input("Course: "), input("Email: "))
    print("Student added.")


def update_student(service: StudentService) -> None:
    sid = input("ID of student to update: ")
    current = service.get_student(sid)
    print(f"Editing: {current}\n(Leave blank to keep current value)")
    service.update_student(
        sid, name=input("New name: "), age=input("New age: "),
        course=input("New course: "), email=input("New email: "))
    print("Student updated.")


def delete_student(service: StudentService) -> None:
    sid = input("ID of student to delete: ")
    student = service.get_student(sid)
    if input(f"Delete {student.name}? (y/n): ").lower() == "y":
        service.delete_student(sid)
        print("Student deleted.")
    else:
        print("Cancelled.")


def main() -> None:
    config = load_config()
    logger = setup_logger(config["logging"])
    logger.info("Starting %s v%s", config["app_name"], config["version"])
    service = StudentService(config["data_file"])

    actions = {
        "1": lambda: add_student(service),
        "2": lambda: print_students(service.get_all()),
        "3": lambda: update_student(service),
        "4": lambda: delete_student(service),
        "5": lambda: print_students(service.search(input("Keyword: "))),
        "6": lambda: print(f"Exported to {service.export_csv(config['export_dir'])}"),
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            logger.info("Application exited.")
            print("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            print("Invalid option. Try again.")
            continue
        try:
            action()
        except (ValidationError, DuplicateStudentError,
                StudentNotFoundError, ValueError) as exc:
            print(f"Error: {exc}")
            logger.warning("User error: %s", exc)
        except OSError as exc:
            print(f"File error: {exc}")
            logger.error("File error: %s", exc)
        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            break
        except Exception:
            logger.exception("Unexpected error")
            print("Unexpected error occurred. See logs/app.log.")


if __name__ == "__main__":
    main()
