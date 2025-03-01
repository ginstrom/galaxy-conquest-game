"""
Hover utilities module for handling hover detection across different game views.

This module provides common functions for detecting hover events on game objects
like planets and star systems, ensuring consistent behavior across the game.
"""

import pygame

def check_hover(mouse_pos, objects, is_within_object_func, rect_check_func=None, game=None):
    """
    Check if the mouse is hovering over any object in the provided list.
    
    This function provides a unified way to detect hover events across different
    types of game objects (planets, star systems, etc.).
    
    Args:
        mouse_pos (tuple): The (x, y) position of the mouse cursor
        objects (list): List of objects to check for hover
        is_within_object_func (callable): Function that determines if the mouse
            is within an object. Takes (mouse_pos, object) as arguments and
            returns a boolean.
        rect_check_func (callable, optional): Function to check if mouse is within
            a rectangular area before doing detailed collision detection.
            Takes (mouse_pos) as argument and returns a boolean.
            
    Returns:
        object or None: The hovered object, or None if no object is hovered
    """
    # If a rect check function is provided, use it to quickly filter out
    # mouse positions that are definitely not hovering any object
    if rect_check_func and not rect_check_func(mouse_pos):
        return None
        
    # Check each object for hover
    for obj in objects:
        if is_within_object_func(mouse_pos, obj):
            # For debugging
            if game and hasattr(obj, 'name'):
                game.debug.add(f"Hovering: {obj.name}")
            elif game and isinstance(obj, dict) and 'name' in obj:
                game.debug.add(f"Hovering: {obj['name']}")
            return obj
            
    return None

def is_within_circle(mouse_pos, obj, center_func=None, radius_func=None):
    """
    Check if the mouse position is within a circular object.
    
    Args:
        mouse_pos (tuple): The (x, y) position of the mouse cursor
        obj: The object to check
        center_func (callable, optional): Function to get the center coordinates
            of the object. Takes obj as argument and returns (x, y).
            If None, assumes obj has 'x' and 'y' attributes or keys.
        radius_func (callable, optional): Function to get the radius of the object.
            Takes obj as argument and returns radius.
            If None, assumes obj has a 'size' attribute or key.
            
    Returns:
        bool: True if mouse is within the circle, False otherwise
    """
    # Get center coordinates
    if center_func:
        x, y = center_func(obj)
    elif hasattr(obj, 'x') and hasattr(obj, 'y'):
        x, y = obj.x, obj.y
    elif isinstance(obj, dict) and 'x' in obj and 'y' in obj:
        x, y = obj['x'], obj['y']
    else:
        return False  # Can't determine center
        
    # Get radius
    if radius_func:
        radius = radius_func(obj)
    elif hasattr(obj, 'size'):
        radius = obj.size
    elif isinstance(obj, dict) and 'size' in obj:
        radius = obj['size']
    else:
        return False  # Can't determine radius
        
    # Check if coordinates are valid (not None)
    if x is None or y is None:
        return False
        
    # Check if mouse is within circle
    dx = mouse_pos[0] - x
    dy = mouse_pos[1] - y
    return dx * dx + dy * dy <= radius * radius
