from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter(name='fcfa0')
def fcfa0(value):
    """
    Format a numeric value with thousand separators and zero decimals for FCFA.
    Usage: {{ amount|fcfa0 }} FCFA
    """
    if value is None:
        return '0'
    try:
        d = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return '0'
    # Format with comma separators, no decimals, then replace commas by spaces for French-style grouping
    s = f"{d:,.0f}"
    return s.replace(',', ' ')
