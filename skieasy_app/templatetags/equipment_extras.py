from django.utils import timezone
from django import template
import pytz

register = template.Library()

@register.simple_tag
def overlap_generator(equipment, start_date, end_date):
    '''
    Generates the appropriate overlap for searched equipment.

    Assume equipment_listing intervals do NOT overlap.
    '''
    overlap_start = ""
    overlap_end = ""
    intervals = [(obj.start_date, obj.end_date) for obj in equipment.equipment_listings.all()]
    intervals = sorted(intervals, key=lambda x: x[0])
    if start_date and end_date:
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
        start_date = pytz.utc.localize(start_date)
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')
        end_date = pytz.utc.localize(end_date)
        for (start_int, end_int) in intervals:
            if start_int <= end_date and end_int >= start_date:
                overlap_start = max(start_int, start_date)
                overlap_end = min(end_int, end_date)
                break;
    elif start_date:
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
        start_date = pytz.utc.localize(start_date)
        for (start_int, end_int) in intervals:
            if end_int >= start_date and start_int <= start_date:
                overlap_start = max(start_int, start_date)
                overlap_end = end_int
                break;
    elif end_date:
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')
        end_date = pytz.utc.localize(end_date)
        for (start_int, end_int) in intervals:
            if end_int >= end_date and start_int <= end_date:
                overlap_start = start_int
                overlap_end = min(end_int, end_date)
    return (overlap_start, overlap_end)
