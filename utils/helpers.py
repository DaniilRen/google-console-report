from config import CURRENT_THEME

def get_theme_color(key):
    return CURRENT_THEME.get(key, '#374151')

def get_status_color(is_good):
    if is_good:
        return '#10B981'
    return '#EF4444'