# frontend/utils.py
from datetime import datetime
def mark_time_range_unavailable(listing, selected_start, selected_end):
    unavailable_range = f"{selected_start} to {selected_end}"
    listing.is_available += f"{unavailable_range}, "
    listing.save()

def overlaps(range1, range2):
    start1, end1 = map(str.strip, range1.split(' to '))
    start2, end2 = map(str.strip, range2.split(' to '))
    start1, end1, start2, end2 = datetime.strptime(start1, "%Y-%m-%d %H:%M"), datetime.strptime(end1, "%Y-%m-%d %H:%M"), datetime.strptime(start2, "%Y-%m-%d %H:%M"), datetime.strptime(end2, "%Y-%m-%d %H:%M")

    return end1 > start2 and start1 < end2


# frontend/utils.py
from datetime import datetime, timedelta

def is_time_range_available(listing, start, end):
    """
    Check if the selected time range is available for the listing.

    Parameters:
    - listing: The game listing.
    - start: The start date of the selected range.
    - end: The end date of the selected range.

    Returns:
    - True if the time range is available, False otherwise.
    """
    selected_start = datetime.strptime(start, "%Y-%m-%d")
    selected_end = datetime.strptime(end, "%Y-%m-%d")

    # Iterate over each unavailable time range in the listing
    for unavailable_range in listing.is_available:
        range_start = datetime.strptime(unavailable_range['start'], "%Y-%m-%d")
        range_end = datetime.strptime(unavailable_range['end'], "%Y-%m-%d")

        # Check for overlap
        if is_overlap(selected_start, selected_end, range_start, range_end):
            return False  # Overlapping, not available

    # No overlap found, the time range is available
    return True


def is_overlap(start1, end1, start2, end2):
    """
    Check if two date ranges overlap.

    Parameters:
    - start1, end1: The first date range.
    - start2, end2: The second date range.

    Returns:
    - True if the date ranges overlap, False otherwise.
    """
    return start1 < end2 and start2 < end1
