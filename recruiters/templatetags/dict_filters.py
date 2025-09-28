
# jobs/templatetags/dict_filters.py
from django import template

register = template.Library()

@register.filter
def get(dict_data, key):
    """Return dict value for a given key, or empty list if not found."""
    return dict_data.get(key, [])
