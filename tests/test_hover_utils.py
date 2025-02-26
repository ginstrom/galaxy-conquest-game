"""Tests for the hover utilities module."""

import pytest
import pygame
from unittest.mock import MagicMock

from game.views.hover_utils import check_hover, is_within_circle
from tests.mocks import MockSurface

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()

class TestCheckHover:
    """Tests for the check_hover function."""
    
    def test_check_hover_with_empty_objects_list(self):
        """Test check_hover with an empty list of objects."""
        mouse_pos = (100, 100)
        objects = []
        is_within_object_func = lambda pos, obj: False
        
        result = check_hover(mouse_pos, objects, is_within_object_func)
        
        assert result is None
    
    def test_check_hover_with_rect_check_function_failing(self):
        """Test check_hover with a rect check function that returns False."""
        mouse_pos = (100, 100)
        objects = [{'name': 'Object 1', 'x': 100, 'y': 100, 'size': 20}]
        is_within_object_func = lambda pos, obj: True
        rect_check_func = lambda pos: False
        
        result = check_hover(mouse_pos, objects, is_within_object_func, rect_check_func)
        
        assert result is None
    
    def test_check_hover_with_rect_check_function_passing(self):
        """Test check_hover with a rect check function that returns True."""
        mouse_pos = (100, 100)
        objects = [{'name': 'Object 1', 'x': 100, 'y': 100, 'size': 20}]
        is_within_object_func = lambda pos, obj: True
        rect_check_func = lambda pos: True
        
        result = check_hover(mouse_pos, objects, is_within_object_func, rect_check_func)
        
        assert result == objects[0]
    
    def test_check_hover_with_object_having_name_attribute(self):
        """Test check_hover with an object that has a name attribute."""
        mouse_pos = (100, 100)
        obj = MagicMock()
        obj.name = "Test Object"
        objects = [obj]
        is_within_object_func = lambda pos, obj: True
        
        result = check_hover(mouse_pos, objects, is_within_object_func)
        
        assert result == obj
    
    def test_check_hover_with_object_having_name_key(self):
        """Test check_hover with an object that has a name key."""
        mouse_pos = (100, 100)
        objects = [{'name': 'Object 1', 'x': 100, 'y': 100, 'size': 20}]
        is_within_object_func = lambda pos, obj: True
        
        result = check_hover(mouse_pos, objects, is_within_object_func)
        
        assert result == objects[0]
    
    def test_check_hover_with_no_hover(self):
        """Test check_hover when no object is hovered."""
        mouse_pos = (100, 100)
        objects = [{'name': 'Object 1', 'x': 200, 'y': 200, 'size': 20}]
        is_within_object_func = lambda pos, obj: False
        
        result = check_hover(mouse_pos, objects, is_within_object_func)
        
        assert result is None
    
    def test_check_hover_with_multiple_objects(self):
        """Test check_hover with multiple objects, where only one is hovered."""
        mouse_pos = (100, 100)
        objects = [
            {'name': 'Object 1', 'x': 200, 'y': 200, 'size': 20},
            {'name': 'Object 2', 'x': 100, 'y': 100, 'size': 20},
            {'name': 'Object 3', 'x': 300, 'y': 300, 'size': 20}
        ]
        
        def is_within_object_func(pos, obj):
            return obj['x'] == pos[0] and obj['y'] == pos[1]
        
        result = check_hover(mouse_pos, objects, is_within_object_func)
        
        assert result == objects[1]

class TestIsWithinCircle:
    """Tests for the is_within_circle function."""
    
    def test_is_within_circle_with_object_attributes(self):
        """Test is_within_circle with an object that has x, y, and size attributes."""
        mouse_pos = (100, 100)
        obj = MagicMock()
        obj.x = 100
        obj.y = 100
        obj.size = 20
        
        result = is_within_circle(mouse_pos, obj)
        
        assert result is True
    
    def test_is_within_circle_with_object_dict(self):
        """Test is_within_circle with an object that is a dictionary with x, y, and size keys."""
        mouse_pos = (100, 100)
        obj = {'x': 100, 'y': 100, 'size': 20}
        
        result = is_within_circle(mouse_pos, obj)
        
        assert result is True
    
    def test_is_within_circle_with_center_func(self):
        """Test is_within_circle with a center function."""
        mouse_pos = (100, 100)
        obj = {'center_x': 100, 'center_y': 100, 'size': 20}
        center_func = lambda obj: (obj['center_x'], obj['center_y'])
        
        result = is_within_circle(mouse_pos, obj, center_func)
        
        assert result is True
    
    def test_is_within_circle_with_radius_func(self):
        """Test is_within_circle with a radius function."""
        mouse_pos = (100, 100)
        obj = {'x': 100, 'y': 100, 'radius': 20}
        radius_func = lambda obj: obj['radius']
        
        result = is_within_circle(mouse_pos, obj, radius_func=radius_func)
        
        assert result is True
    
    def test_is_within_circle_with_both_funcs(self):
        """Test is_within_circle with both center and radius functions."""
        mouse_pos = (100, 100)
        obj = {'center_x': 100, 'center_y': 100, 'radius': 20}
        center_func = lambda obj: (obj['center_x'], obj['center_y'])
        radius_func = lambda obj: obj['radius']
        
        result = is_within_circle(mouse_pos, obj, center_func, radius_func)
        
        assert result is True
    
    def test_is_within_circle_outside_circle(self):
        """Test is_within_circle when the mouse is outside the circle."""
        mouse_pos = (150, 150)
        obj = {'x': 100, 'y': 100, 'size': 20}
        
        result = is_within_circle(mouse_pos, obj)
        
        assert result is False
    
    def test_is_within_circle_on_edge(self):
        """Test is_within_circle when the mouse is on the edge of the circle."""
        mouse_pos = (120, 100)
        obj = {'x': 100, 'y': 100, 'size': 20}
        
        result = is_within_circle(mouse_pos, obj)
        
        assert result is True
    
    def test_is_within_circle_missing_center(self):
        """Test is_within_circle when the object doesn't have center coordinates."""
        mouse_pos = (100, 100)
        obj = {'size': 20}
        
        result = is_within_circle(mouse_pos, obj)
        
        assert result is False
    
    def test_is_within_circle_missing_radius(self):
        """Test is_within_circle when the object doesn't have a size/radius."""
        mouse_pos = (100, 100)
        obj = {'x': 100, 'y': 100}
        
        result = is_within_circle(mouse_pos, obj)
        
        assert result is False
