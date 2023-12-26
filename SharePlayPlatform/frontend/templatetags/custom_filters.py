# frontend/templatetags/custom_filters.py

from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='hour_unavailable')
def hour_unavailable(hour, listed):
    """
    Check if the given hour is marked as unavailable in the listing.

    Parameters:
    - hour: The hour to check for availability.
    - listed: The game listing.

    Returns:
    - True if the hour is unavailable, False otherwise.
    """
    hour = int(hour)
    for time_range in listed.is_available:
        start_hour, _ = time_range['start'].split(':')
        end_hour, _ = time_range['end'].split(':')
        start_hour, end_hour = int(start_hour), int(end_hour)

        # Check if the hour falls within the range (inclusive)
        if start_hour <= hour <= end_hour:
            return True

    return False
