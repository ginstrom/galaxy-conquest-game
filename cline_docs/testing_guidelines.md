# Galaxy Conquest Testing Guidelines

## Testing Philosophy

Our testing approach is built on the following principles:

1. **Hardware Independence**: Tests should run without requiring specific hardware or display capabilities.
2. **High Coverage**: We aim for at least 80% code coverage across the codebase.
3. **Isolation**: Components should be testable in isolation through dependency injection.
4. **Reproducibility**: Tests should produce consistent results across different environments.
5. **Maintainability**: Tests should be easy to understand, modify, and extend.

## Testing Structure

### Unit Tests

Unit tests focus on testing individual components in isolation. They should:

- Test a single function, method, or class
- Mock all external dependencies
- Cover both normal operation and edge cases
- Be fast and deterministic

Example of a good unit test:

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

Integration tests verify that components work together correctly. They should:

- Test interactions between multiple components
- Use minimal mocking, focusing on external dependencies
- Verify end-to-end functionality
- Cover key user scenarios

Example of a good integration test:

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

We use mock objects to replace hardware-dependent components during testing. Key mock objects include:

### MockSurface

Used to replace pygame.Surface for testing drawing operations:

```python
surface = MockSurface((800, 600))
component.draw(surface)
assert surface.blit_called
```

### MockFont

Used to replace pygame.font.Font for testing text rendering:

```python
font = MockFont(size=24)
text_surface = font.render("Test Text", True, (255, 255, 255))
assert isinstance(text_surface, MockSurface)
```

### MockGame

Used to provide a game context for testing components:

```python
game = MockGame()
view = SystemView(game)
assert view.game == game
```

## Dependency Injection

We use dependency injection to make components testable in isolation:

1. Components should accept dependencies through their constructor
2. Default implementations can be provided for normal operation
3. Tests can provide mock implementations for testing

Example:

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

## Test Coverage

We use pytest-cov to track test coverage:

```bash
pytest --cov=game tests/
```

Coverage targets:
- Overall project: 80%+
- Core game logic: 90%+
- UI components: 75%+

When adding new features, tests should be written to maintain or improve these coverage targets.

## Edge Case Testing

All components should be tested with edge cases, including:

1. **Initialization with minimal/default parameters**
2. **Boundary conditions** (empty lists, zero values, etc.)
3. **Error conditions** (invalid inputs, resource failures)
4. **State transitions** (changing from one game state to another)

Example edge case test:

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

Tests should be organized to mirror the structure of the production code:

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

Each test file should focus on a single production module, and test functions should be named descriptively to indicate what they're testing.

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

Our testing approach should evolve with the project:

1. Regularly review test coverage reports
2. Identify and address areas with low coverage
3. Refactor tests as the codebase changes
4. Share testing patterns and techniques among the team
5. Update these guidelines as new best practices emerge
