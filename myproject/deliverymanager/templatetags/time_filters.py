from django import template

register = template.Library()

@register.filter
def seconds_to_min_sec(value):
    try:
        total_seconds = int(value)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
    except (ValueError, TypeError):
        return value