from django import template

register = template.Library()

@register.filter
def split(value, delimiter=","):
    """
    Splits a string into a list using the given delimiter.
    """
    if isinstance(value, str):  # Ensure it's a string
        return value.split(delimiter)
    return value  # If not a string, return as-is
from django import template
import ast  # To safely parse the string into a list

register = template.Library()
@register.filter
def parse_subjects(value):
    """
    Converts a string representation of a list into an actual list.
    Usage: {{ value|parse_subjects }}
    """
    try:
        # Safely evaluate the string to a Python list
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value  # Return the original value if parsing fails
    
