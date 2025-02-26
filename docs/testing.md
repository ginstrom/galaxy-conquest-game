# Testing Guide

This document provides detailed information about testing the Galaxy Conquest game.

## Testing Philosophy

Our testing approach is built on the following principles:

1. **Hardware Independence**: Tests run without requiring specific hardware or display capabilities.
2. **High Coverage**: We aim for at least 80% code coverage across the codebase.
3. **Isolation**: Components are testable in isolation through dependency injection.
4. **Reproducibility**: Tests produce consistent results across different environments.
5. **Maintainability**: Tests are easy to understand, modify, and extend.

## Running Tests

The project uses pytest for testing. Tests are located in the `tests/` directory.

### Using the Makefile (Recommended)

The project includes a Makefile to simplify running tests:

```bash
# Run all tests
make test

# Run tests with coverage report
make coverage
```

### Manual Test Execution

If you prefer not to use the Makefile, you can run tests manually:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run a specific test file
python -m pytest tests/test_infopanel.py

# Run a specific test function
python -m pytest tests/test_infopanel.py::test_info_panel_initialization
```

### Coverage Testing

```bash
# Using Makefile (recommended)
make coverage
# This generates both a terminal report and an HTML report in the htmlcov/ directory
# and automatically opens the HTML report in your default browser

# Manual method
python -m pytest --cov=game tests/

# Generate only HTML coverage report
python -m pytest --cov=game --cov-report=html tests/
```

The HTML coverage report provides an interactive way to explore test coverage. The `make coverage` command automatically opens the report in your default browser. This allows you to:

- See overall coverage statistics
- Drill down into specific modules
- View line-by-line coverage with color coding
- Identify untested code sections

## Test Structure

### Unit Tests

Unit tests focus on testing individual components in isolation. Example:

```python
def test_info_panel_initialization():
    """Test that InfoPanel initializes with correct attributes."""
    game = MockGame()
    panel = InfoPanel(game)
    
    assert panel.game == game
    assert panel.font is not None
    assert panel.rect.width > 0
    assert panel.rect.height > 0
```

### Integration Tests

Integration tests verify that components work together correctly. Example:

```python
def test_view_panel_integration():
    """Test that GalaxyView correctly integrates with its InfoPanel."""
    game = MockGame()
    view = GalaxyView(game)
    
    # Verify panel initialization
    assert isinstance(view.panel, GalaxyViewInfoPanel)
    assert view.panel.game == game
    
    # Verify drawing integration
    screen = MockSurface((800, 600))
    view.draw(screen)
    
    # Verify panel was drawn
    assert screen.blit_called
```

## Mock Objects

The project uses mock objects to replace hardware-dependent components during testing:

### Key Mock Objects

- **MockSurface**: Replaces pygame.Surface for testing drawing operations
- **MockFont**: Replaces pygame.font.Font for testing text rendering
- **MockGame**: Provides a game context for testing components

Example usage:

```python
# Create a mock surface for testing drawing
surface = MockSurface((800, 600))
component.draw(surface)
assert surface.blit_called

# Create a mock game for testing components
game = MockGame()
view = SystemView(game)
assert view.game == game
```

## Dependency Injection

Components accept dependencies through their constructor, making them testable in isolation:

```python
# In production code
class PlanetView:
    def __init__(self, game, font_manager=None):
        self.game = game
        self.font_manager = font_manager or FontManager()
        
# In test code
def test_planet_view():
    game = MockGame()
    font_manager = MockFontManager()
    view = PlanetView(game, font_manager)
    # Test with mock dependencies
```

## Test Coverage Targets

- Overall project: 80%+
- Core game logic: 90%+
- UI components: 75%+

## Edge Case Testing

All components are tested with edge cases, including:

1. Initialization with minimal/default parameters
2. Boundary conditions (empty lists, zero values, etc.)
3. Error conditions (invalid inputs, resource failures)
4. State transitions (changing from one game state to another)

Example:

```python
def test_info_panel_with_no_selected_system():
    """Test InfoPanel behavior when no system is selected."""
    game = MockGame()
    game.selected_system = None
    panel = SystemViewInfoPanel(game)
    
    surface = MockSurface((800, 600))
    panel.draw(surface)
    
    # Verify appropriate "no system selected" message is displayed
    assert surface.blit_called
```

## Test Organization

Tests are organized to mirror the structure of the production code:

```
game/
  views/
    galaxy.py
    system.py
    
tests/
  test_views/
    test_galaxy.py
    test_system.py
```

## Best Practices

1. **Write tests first** when adding new features (Test-Driven Development)
2. **Keep tests simple and focused** on a single aspect of behavior
3. **Use descriptive test names** that explain what's being tested
4. **Add comments** to clarify test intent and complex assertions
5. **Avoid test interdependence** - tests should run in any order
6. **Clean up resources** after tests complete
7. **Use parameterized tests** for testing multiple similar cases
8. **Maintain test quality** - tests should be treated as production code

## Continuous Improvement

Our testing approach evolves with the project:

1. Regularly review test coverage reports
2. Identify and address areas with low coverage
3. Refactor tests as the codebase changes
4. Share testing patterns and techniques among the team

## Troubleshooting Tests

### Common Issues

#### Tests Failing Due to Pygame Initialization

If tests fail with errors related to Pygame initialization, ensure you're using the mock objects correctly:

```python
# Incorrect - tries to use actual Pygame
surface = pygame.Surface((800, 600))

# Correct - uses mock for testing
surface = MockSurface((800, 600))
```

#### Tests Failing Due to Random Values

If tests fail intermittently due to random values, use fixed seeds for testing:

```python
# In test setup
import random
random.seed(12345)  # Use a fixed seed for testing
```

#### Tests Taking Too Long

If tests are taking too long to run, identify and optimize slow tests:

```bash
# Identify slow tests
python -m pytest --durations=10
```
