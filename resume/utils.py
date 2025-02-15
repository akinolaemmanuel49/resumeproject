import re
from django.core.exceptions import ValidationError

def validate_month_year_format(date_str):
    """
    Validates that a given date string follows the 'MM/YYYY' format.
    Example of valid inputs: '02/2025', '12/1999'
    """
    if not re.match(r"^(0[1-9]|1[0-2])\/\d{4}$", date_str):
        raise ValidationError("Date must be in MM/YYYY format (e.g., 02/2025).")
    return date_str
