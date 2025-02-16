"""Tests for the BackgroundEffect class."""
import pytest
import pygame
from game.background import BackgroundEffect
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, NUM_BACKGROUND_STARS,
    NUM_NEBULAE, RED, BLUE, PURPLE, PINK
)

# Initialize pygame for testing
pygame.init()

@pytest.fixture
def background():
    """Create a background effect instance for testing."""
    return BackgroundEffect()

@pytest.fixture
def screen():
    """Create a pygame surface for testing."""
    return pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

def test_background_initialization(background):
    """Test that background effects are properly initialized."""
    # Test stars initialization
    assert len(background.stars) == NUM_BACKGROUND_STARS
    for star in background.stars:
        assert 0 <= star['x'] <= SCREEN_WIDTH
        assert 0 <= star['y'] <= SCREEN_HEIGHT
        assert 1 <= star['size'] <= 2
        assert isinstance(star['color'], tuple)
        assert len(star['color']) == 3
        assert all(100 <= c <= 180 for c in star['color'])
        assert 0 <= star['twinkle_offset'] <= 2 * 3.14159

    # Test nebulae initialization
    assert len(background.nebulae) == NUM_NEBULAE
    for nebula in background.nebulae:
        assert 0 <= nebula['x'] <= SCREEN_WIDTH
        assert 0 <= nebula['y'] <= SCREEN_HEIGHT
        assert 100 <= nebula['size'] <= 200
        assert isinstance(nebula['color'], tuple)
        assert len(nebula['color']) == 4  # RGBA
        assert len(nebula['particles']) == 40
        
        # Test particles
        for particle in nebula['particles']:
            assert isinstance(particle, dict)
            assert 'x' in particle
            assert 'y' in particle
            assert 'size' in particle
            assert 20 <= particle['size'] <= 35

def test_draw_galaxy_background(background, screen):
    """Test drawing the galaxy background."""
    # Get initial state at a few sample points
    initial_colors = []
    for nebula in background.nebulae:
        x, y = int(nebula['x']), int(nebula['y'])
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            initial_colors.append((x, y, screen.get_at((x, y))))
    
    # Draw background
    background.draw_galaxy_background(screen)
    
    # Verify changes were made
    changes_found = False
    for x, y, initial_color in initial_colors:
        final_color = screen.get_at((x, y))
        if final_color != initial_color:
            changes_found = True
            break
    assert changes_found, "No changes detected in galaxy background"

def test_draw_system_background(background, screen):
    """Test drawing the system background."""
    # Get initial state at star positions
    initial_colors = []
    for star in background.stars:
        x, y = int(star['x']), int(star['y'])
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            initial_colors.append((x, y, screen.get_at((x, y))))
    
    # Draw background
    background.draw_system_background(screen)
    
    # Verify that at least some stars were drawn
    changes_found = False
    for x, y, initial_color in initial_colors:
        final_color = screen.get_at((x, y))
        if final_color != initial_color:
            changes_found = True
            break
    assert changes_found, "No stars detected in system background"

def test_star_twinkling(background, screen):
    """Test that stars twinkle over time."""
    # Draw background and sample star colors
    background.draw_system_background(screen)
    first_colors = []
    for star in background.stars:
        x, y = int(star['x']), int(star['y'])
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            first_colors.append((x, y, screen.get_at((x, y))))
    
    # Simulate time passing
    pygame.time.set_timer(pygame.USEREVENT, 500)  # 500ms
    pygame.event.wait()  # Wait for the timer event
    
    # Clear and redraw
    screen.fill((0, 0, 0))
    background.draw_system_background(screen)
    
    # Check if any star colors changed
    changes_found = False
    for x, y, first_color in first_colors:
        second_color = screen.get_at((x, y))
        if second_color != first_color:
            changes_found = True
            break
    assert changes_found, "No twinkling effect detected"
