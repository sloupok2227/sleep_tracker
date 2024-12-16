from datetime import timedelta

from django import template

register = template.Library()

@register.filter
def format_duration(duration):
    """
    Преобразует timedelta в строку вида 'X ч Y мин'.
    """
    if not isinstance(duration, timedelta):
        return "Неверный формат"
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours} ч {minutes} мин"
