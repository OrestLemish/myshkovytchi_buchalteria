from django import template
import math

register = template.Library()

@register.filter
def abs(value):
    """
    Returns the absolute value of a number.
    
    Example usage: {{ value|abs }}
    """
    try:
        return math.fabs(float(value))
    except (ValueError, TypeError):
        return value

@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except (ValueError, TypeError):
        return 0