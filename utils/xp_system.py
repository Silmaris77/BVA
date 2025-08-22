"""
XP and Level Calculation Utilities
Handles user experience points, level calculations, and progress tracking.
"""

from config.settings import XP_LEVELS


def calculate_xp_progress(user_data):
    """Calculate XP progress and dynamically determine the user's level"""
    # Dynamically determine the user's level based on XP
    for level, xp_threshold in sorted(XP_LEVELS.items(), reverse=True):
        if user_data['xp'] >= xp_threshold:
            user_data['level'] = level
            break

    # Calculate progress to the next level
    next_level = user_data['level'] + 1
    if next_level in XP_LEVELS:
        current_level_xp = XP_LEVELS[user_data['level']]
        next_level_xp = XP_LEVELS[next_level]
        xp_needed = next_level_xp - current_level_xp
        xp_progress = user_data['xp'] - current_level_xp
        xp_percentage = min(100, int((xp_progress / xp_needed) * 100))
        return xp_percentage, xp_needed - xp_progress

    return 100, 0


def get_user_level(xp):
    """Get the user's level based on XP"""
    for level, xp_threshold in sorted(XP_LEVELS.items(), reverse=True):
        if xp >= xp_threshold:
            return level
    return 1  # Default to level 1


def get_xp_for_level(level):
    """Get the XP required for a specific level"""
    return XP_LEVELS.get(level, 0)


def get_next_level_info(user_data):
    """Get information about the next level"""
    current_level = user_data.get('level', 1)
    next_level = current_level + 1
    
    if next_level in XP_LEVELS:
        current_level_xp = XP_LEVELS[current_level]
        next_level_xp = XP_LEVELS[next_level]
        xp_needed = next_level_xp - user_data['xp']
        return {
            'next_level': next_level,
            'xp_needed': xp_needed,
            'next_level_xp': next_level_xp,
            'current_level_xp': current_level_xp
        }
    
    return None  # Already at max level


def get_level_xp_range(level):
    """Get the XP range for a specific level"""
    current_level_xp = XP_LEVELS.get(level, 0)
    next_level_xp = XP_LEVELS.get(level + 1, None)
    
    return {
        'current_level_xp': current_level_xp,
        'next_level_xp': next_level_xp
    }
