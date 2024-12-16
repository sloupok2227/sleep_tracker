from django import template

register = template.Library()

@register.filter
def hours_from_seconds(seconds):
    """Преобразует секунды в часы с двумя знаками после запятой."""
    try:
        return round(float(seconds) / 3600, 2)
    except (TypeError, ValueError):
        return 0

@register.filter
def format_duration(timedelta_obj):
    if not timedelta_obj:
        return "0 ч 0 мин"
    hours = timedelta_obj.seconds // 3600
    minutes = (timedelta_obj.seconds // 60) % 60
    return f"{hours} ч {minutes} мин"