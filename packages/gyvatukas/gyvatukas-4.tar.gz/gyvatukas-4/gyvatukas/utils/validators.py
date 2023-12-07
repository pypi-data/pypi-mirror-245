import logging

from email_validator import validate_email, EmailNotValidError

_logger = logging.getLogger("gyvatukas")


def is_email_valid(email: str, check_deliverability: bool = False) -> tuple[bool, str]:
    """Check if email is valid. If check_deliverability is True, will also check if email is deliverable.
    If email is valid, returns normalized email, otherwise returns the original email.

    🚨 check_deliverability performs external request!

    Uses https://github.com/JoshData/python-email-validator lib.
    """
    _logger.debug(f"validating email `%s", email)
    try:
        validation_result = validate_email(email, check_deliverability=check_deliverability)
    except EmailNotValidError:
        _logger.exception(f"email `{email}` validation failed!")
        return False, email

    return True, validation_result.normalized
