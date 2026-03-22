from django import template

register = template.Library()

@register.filter
def meters_to_kilometer_meter(value):
    try:
        total_meters = int(value)
        kilometers = total_meters // 1000
        meters = total_meters % 1000
        return f"{kilometers}.{meters}"
    except (ValueError, TypeError):
        return value