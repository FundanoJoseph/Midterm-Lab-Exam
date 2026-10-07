"""Input validation helpers (bonus: data validation)."""
import re

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def validate_student_id(value: str) -> str:
    value = (value or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9-]{3,15}", value):
        raise ValidationError("ID must be 3-15 letters, digits or hyphens.")
    return value


def validate_name(value: str) -> str:
    value = (value or "").strip()
    if len(value) < 2 or not re.fullmatch(r"[A-Za-z .'-]+", value):
        raise ValidationError("Name must be 2+ letters (letters, spaces, . ' - only).")
    return value


def validate_age(value) -> int:
    try:
        age = int(value)
    except (TypeError, ValueError):
        raise ValidationError("Age must be a whole number.")
    if not 5 <= age <= 100:
        raise ValidationError("Age must be between 5 and 100.")
    return age


def validate_course(value: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValidationError("Course cannot be empty.")
    return value


def validate_email(value: str) -> str:
    value = (value or "").strip()
    if not EMAIL_RE.match(value):
        raise ValidationError("Invalid email format.")
    return value
