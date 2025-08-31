from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter(name='gnf')
def gnf(value):
    """
    Format a numeric value with thousand separators and zero decimals for GNF.
    Usage: {{ amount|gnf }} GNF
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
