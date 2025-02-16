"""
View transition system for smooth transitions between game views.

This module provides:
- Transition effects between views
- State preservation during transitions
- Visual feedback during view changes
"""

import pygame
from typing import Dict, Any, Optional


class ViewTransition:
    """
    Handles smooth transitions between views with fade effects.
    
    Args:
        duration_ms (int): Duration of transition effect in milliseconds
    """
    
    def __init__(self, duration_ms: int = 500):
        self.duration = duration_ms
        self.start_time = 0
        self.is_active = False
        self.from_view = None
        self.to_view = None

    def start(self, from_view: str, to_view: str) -> None:
        """
        Start a transition between views.
        
        Args:
            from_view: Name of view transitioning from
            to_view: Name of view transitioning to
        """
        self.is_active = True
        self.from_view = from_view
        self.to_view = to_view
        self.start_time = pygame.time.get_ticks()  # Must be set last to ensure accurate timing

    def draw(self, screen: pygame.Surface) -> bool:
        """
        Draw the transition effect.
        
        Args:
            screen: Pygame surface to draw on
            
        Returns:
            bool: True if transition is still active, False when complete
        """
        if not self.is_active:
            return False

        progress = (pygame.time.get_ticks() - self.start_time) / self.duration
        if progress >= 1.0:
            self.is_active = False
            return False

        # Fade effect
        alpha = int(255 * (1 - progress))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))
        return True


class ViewStateManager:
    """
    Manages state preservation between view transitions.
    
    Stores and retrieves view-specific state data to ensure smooth transitions
    and proper state restoration when switching between views.
    """
    
    def __init__(self):
        self.view_states: Dict[str, Any] = {}
        self.current_view: Optional[str] = None

    def store_state(self, view_name: str, state_data: Dict[str, Any]) -> None:
        """
        Store state data for a specific view.
        
        Args:
            view_name: Name of the view to store state for
            state_data: Dictionary containing view state data
        """
        self.view_states[view_name] = state_data

    def get_state(self, view_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve stored state data for a view.
        
        Args:
            view_name: Name of the view to get state for
            
        Returns:
            Dict containing view state data or None if not found
        """
        return self.view_states.get(view_name, None)

    def clear_state(self, view_name: str) -> None:
        """
        Remove stored state data for a view.
        
        Args:
            view_name: Name of the view to clear state for
        """
        if view_name in self.view_states:
            del self.view_states[view_name]
