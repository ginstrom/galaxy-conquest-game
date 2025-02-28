"""
Test Suite for notifications.py

This module contains tests for the NotificationManager class in game/notifications.py.
"""

import pytest
import pygame
from unittest.mock import patch, MagicMock
from game.notifications import NotificationManager
from tests.mocks import MockSurface


@pytest.fixture
def notification_manager():
    """Create a NotificationManager instance with a mocked UI manager for testing."""
    ui_manager = MagicMock()
    return NotificationManager(ui_manager)


def test_notification_manager_init(notification_manager):
    """Test the initialization of the NotificationManager class."""
    assert notification_manager.save_notification_time == 0
    assert notification_manager.save_notification_duration == 2000
    assert notification_manager.save_notification_label is None


def test_show_save_notification(notification_manager, monkeypatch):
    """Test the show_save_notification method."""
    # Mock pygame.time.get_ticks to return a predictable value
    monkeypatch.setattr('pygame.time.get_ticks', lambda: 1000)
    
    notification_manager.show_save_notification()
    
    assert notification_manager.save_notification_time == 1000


def test_draw_save_notification_show(notification_manager, monkeypatch):
    """Test drawing the save notification when it should be shown."""
    # Mock pygame.time.get_ticks to return a predictable value
    current_time = 1000
    monkeypatch.setattr('pygame.time.get_ticks', lambda: current_time)
    
    # Set up the notification time to be recent
    notification_manager.save_notification_time = current_time - 500  # 500ms ago
    
    # Mock the UILabel class
    mock_label = MagicMock()
    with patch('pygame_gui.elements.UILabel', return_value=mock_label) as mock_label_class:
        # Create a mock surface to draw on
        screen = MockSurface((800, 600))
        
        # Test the method
        notification_manager.draw_save_notification(screen)
        
        # Verify that a UILabel was created with the correct parameters
        mock_label_class.assert_called_once()
        args, kwargs = mock_label_class.call_args
        assert kwargs['text'] == "Game Saved!"
        assert kwargs['manager'] == notification_manager.ui_manager
        
        # Verify that the label attribute was set
        assert notification_manager.save_notification_label == mock_label


def test_draw_save_notification_hide(notification_manager, monkeypatch):
    """Test drawing the save notification when it should be hidden."""
    # Mock pygame.time.get_ticks to return a predictable value
    current_time = 1000
    monkeypatch.setattr('pygame.time.get_ticks', lambda: current_time)
    
    # Set up the notification time to be expired
    notification_manager.save_notification_time = current_time - 3000  # 3 seconds ago
    
    # Create a mock label
    mock_label = MagicMock()
    notification_manager.save_notification_label = mock_label
    
    # Create a mock surface to draw on
    screen = MockSurface((800, 600))
    
    # Test the method
    notification_manager.draw_save_notification(screen)
    
    # Verify that the existing label was killed
    assert mock_label.kill.called
    
    # Verify that the label attribute was set to None
    assert notification_manager.save_notification_label is None


def test_draw_save_notification_no_existing_label(notification_manager, monkeypatch):
    """Test drawing the save notification when no label exists yet."""
    # Mock pygame.time.get_ticks to return a predictable value
    current_time = 1000
    monkeypatch.setattr('pygame.time.get_ticks', lambda: current_time)
    
    # Set up the notification time to be recent
    notification_manager.save_notification_time = current_time - 500  # 500ms ago
    
    # Ensure no label exists
    notification_manager.save_notification_label = None
    
    # Mock the UILabel class
    mock_label = MagicMock()
    with patch('pygame_gui.elements.UILabel', return_value=mock_label) as mock_label_class:
        # Create a mock surface to draw on
        screen = MockSurface((800, 600))
        
        # Test the method
        notification_manager.draw_save_notification(screen)
        
        # Verify that a UILabel was created
        mock_label_class.assert_called_once()
        
        # Verify that the label attribute was set
        assert notification_manager.save_notification_label == mock_label


def test_draw_save_notification_existing_label(notification_manager, monkeypatch):
    """Test drawing the save notification when a label already exists."""
    # Mock pygame.time.get_ticks to return a predictable value
    current_time = 1000
    monkeypatch.setattr('pygame.time.get_ticks', lambda: current_time)
    
    # Set up the notification time to be recent
    notification_manager.save_notification_time = current_time - 500  # 500ms ago
    
    # Create a mock label
    mock_label = MagicMock()
    notification_manager.save_notification_label = mock_label
    
    # Mock the UILabel class
    with patch('pygame_gui.elements.UILabel', return_value=MagicMock()) as mock_label_class:
        # Create a mock surface to draw on
        screen = MockSurface((800, 600))
        
        # Test the method
        notification_manager.draw_save_notification(screen)
        
        # Verify that no new UILabel was created
        mock_label_class.assert_not_called()
        
        # Verify that the existing label was not killed
        assert not mock_label.kill.called
        
        # Verify that the label attribute was not changed
        assert notification_manager.save_notification_label == mock_label
